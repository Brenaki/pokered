#!/usr/bin/env python3
"""Generate the controlled NPC and AI behavior document from RGBDS sources."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/003-2026-08-01-Funcionamento-das-IAs-Pokemon.md"
BASELINE_COMMIT = "51079046aab46619f2ac5d9127ecf5be70e9a5e8"


@dataclass(frozen=True)
class ObjectEvent:
    map_name: str
    line: int
    x: str
    y: str
    sprite: str
    movement: str
    constraint: str
    text_id: str
    extra1: str = ""
    extra2: str = ""

    @property
    def category(self) -> str:
        if self.extra2 and self.extra1.startswith("OPP_"):
            return "Treinador"
        if self.extra2:
            return "Pokemon estatico"
        if self.extra1:
            return "Item/objeto coletavel"
        if self.sprite == "SPRITE_BOULDER":
            return "Obstaculo empurravel"
        if self.sprite in {"SPRITE_MONSTER", "SPRITE_BIRD", "SPRITE_FAIRY"}:
            return "Pokemon/cenario interativo"
        if self.sprite in {"SPRITE_POKE_BALL", "SPRITE_FOSSIL"}:
            return "Objeto interativo"
        return "NPC/interacao"

    @property
    def target(self) -> str:
        if self.extra2:
            return f"{self.extra1}; conjunto/nivel {self.extra2}"
        return self.extra1 or "-"

    @property
    def source(self) -> str:
        return f"data/maps/objects/{self.map_name}.asm:{self.line}"


@dataclass(frozen=True)
class TrainerHeader:
    map_name: str
    line: int
    event: str
    view_range: str
    before: str
    end: str
    after: str

    @property
    def source(self) -> str:
        return f"scripts/{self.map_name}.asm:{self.line}"


@dataclass(frozen=True)
class ScriptState:
    map_name: str
    line: int
    handler: str
    state: str

    @property
    def source(self) -> str:
        return f"scripts/{self.map_name}.asm:{self.line}"


@dataclass(frozen=True)
class MovementCallsite:
    source: str
    owner: str
    operation: str
    instruction: str


def split_args(line: str, macro: str) -> list[str]:
    code = line.split(";", 1)[0].strip()
    payload = code[len(macro) :].strip()
    return [part.strip() for part in payload.split(",")]


def parse_object_events() -> list[ObjectEvent]:
    events: list[ObjectEvent] = []
    for path in sorted((ROOT / "data/maps/objects").glob("*.asm")):
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not re.match(r"^\s*object_event\s+", raw):
                continue
            args = split_args(raw, "object_event")
            assert 6 <= len(args) <= 8, f"Unexpected object_event at {path}:{line_no}: {args}"
            args += [""] * (8 - len(args))
            events.append(ObjectEvent(path.stem, line_no, *args[:8]))
    return events


def parse_trainer_headers() -> list[TrainerHeader]:
    headers: list[TrainerHeader] = []
    for path in sorted((ROOT / "scripts").glob("*.asm")):
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not re.match(r"^\s*trainer\s+", raw):
                continue
            args = split_args(raw, "trainer")
            assert len(args) == 5, f"Unexpected trainer header at {path}:{line_no}: {args}"
            headers.append(TrainerHeader(path.stem, line_no, *args))
    return headers


def parse_script_states() -> list[ScriptState]:
    states: list[ScriptState] = []
    pattern = re.compile(
        r"^\s*dw_const\s+([A-Za-z0-9_.]*Script[A-Za-z0-9_.]*),\s*(SCRIPT_[A-Z0-9_]+)"
    )
    for path in sorted((ROOT / "scripts").glob("*.asm")):
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = pattern.match(raw)
            if match:
                states.append(ScriptState(path.stem, line_no, match.group(1), match.group(2)))
    return states


def nearest_label(lines: list[str], index: int) -> str:
    for raw in reversed(lines[: index + 1]):
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*):{1,2}\s*$", raw)
        if match:
            return match.group(1)
    return "(arquivo)"


def parse_movement_callsites() -> list[MovementCallsite]:
    operations = {
        "MoveSprite",
        "MoveSprite_",
        "StartSimulatingJoypadStates",
        "DecodeRLEList",
        "FindPathToPlayer",
    }
    pattern = re.compile(
        r"^\s*(call|jp|farcall|farjp|predef|predef_jump)\s+([A-Za-z_][A-Za-z0-9_]*)"
    )
    paths = sorted((ROOT / "scripts").glob("*.asm"))
    paths += sorted((ROOT / "engine/events").glob("*.asm"))
    calls: list[MovementCallsite] = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, raw in enumerate(lines):
            match = pattern.match(raw)
            if not match or match.group(2) not in operations:
                continue
            calls.append(
                MovementCallsite(
                    f"{path.relative_to(ROOT)}:{index + 1}",
                    nearest_label(lines, index),
                    match.group(2),
                    match.group(1),
                )
            )
    return calls


def parse_trainer_classes() -> list[str]:
    classes: list[str] = []
    pattern = re.compile(r"^\s*trainer_const\s+([A-Z0-9_]+)")
    for raw in (ROOT / "constants/trainer_constants.asm").read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw)
        if match and match.group(1) != "NOBODY":
            classes.append(match.group(1))
    return classes


def parse_ai_actions() -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    pattern = re.compile(r"^\s*dbw\s+(\d+),\s*([A-Za-z0-9_]+)\s*;\s*([A-Z0-9_]+)")
    for raw in (ROOT / "data/trainers/ai_pointers.asm").read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw)
        if match:
            result[match.group(3)] = (match.group(1), match.group(2))
    return result


def parse_move_layers() -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r"^\s*move_choices(?:\s+([^;]+?))?\s*;\s*([A-Z0-9_]+)\s*$")
    for raw in (ROOT / "data/trainers/move_choices.asm").read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw)
        if match:
            choices = (match.group(1) or "").replace(" ", "")
            result[match.group(2)] = choices or "nenhuma"
    return result


def validate(
    objects: list[ObjectEvent],
    headers: list[TrainerHeader],
    states: list[ScriptState],
    classes: list[str],
    ai_actions: dict[str, tuple[str, str]],
    move_layers: dict[str, str],
) -> None:
    assert len(objects) == 918, f"Expected 918 object events, found {len(objects)}"
    assert len(headers) == 322, f"Expected 322 trainer headers, found {len(headers)}"
    assert len(states) == 199, f"Expected 199 script states, found {len(states)}"
    assert len(classes) == 47, f"Expected 47 trainer classes, found {len(classes)}"
    assert set(classes) == set(ai_actions) == set(move_layers)
    assert sum(event.category == "Treinador" for event in objects) == 334
    assert sum(event.category == "Pokemon estatico" for event in objects) == 12


def md_escape(value: str) -> str:
    return value.replace("|", "\\|")


def grouped(items, key):
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return groups


def build_document() -> str:
    objects = parse_object_events()
    headers = parse_trainer_headers()
    states = parse_script_states()
    calls = parse_movement_callsites()
    classes = parse_trainer_classes()
    ai_actions = parse_ai_actions()
    move_layers = parse_move_layers()
    validate(objects, headers, states, classes, ai_actions, move_layers)

    category_counts = Counter(event.category for event in objects)
    movement_counts = Counter(event.movement for event in objects)
    constraint_counts = Counter(event.constraint for event in objects)
    object_maps = len({event.map_name for event in objects})
    trainer_maps = len({header.map_name for header in headers})
    state_maps = len({state.map_name for state in states})

    out: list[str] = []
    out.append(f"""# Funcionamento das IAs e dos NPCs de Pokemon Red/Blue

## Controle do documento

| Campo | Valor |
|---|---|
| Identificacao | AI-NPC-003 |
| Arquivo | `003-2026-08-01-Funcionamento-das-IAs-Pokemon.md` |
| Revisao | 1.0 |
| Data de emissao | 2026-08-01 |
| Situacao | Emitido para revisao e uso tecnico interno |
| Responsavel pelo processo | Equipe de reescrita ASM para C |
| Elaborado por | Gerador deterministico, Graphify e verificacao direta do codigo-fonte |
| Aprovador | Pendente de designacao |
| Baseline do codigo | commit `{BASELINE_COMMIT}` |
| Abrangencia | IA de batalha, movimento, percepcao, interacao e scripts de NPC da ROM Red/Blue |
| Classificacao | Informacao documentada interna |

### Historico de revisoes

| Revisao | Data | Alteracao | Autor | Aprovacao |
|---|---|---|---|---|
| 1.0 | 2026-08-01 | Emissao inicial da especificacao e dos inventarios completos | Codex | Pendente |

## 1. Finalidade e relacao com a ISO 9001

Este documento controla o conhecimento sobre os algoritmos que tomam decisoes por
treinadores, criaturas e objetos de mapa. Ele e um contrato de caracterizacao para
a reescrita incremental em C e uma base para testes, analise de risco, aprovacao e
melhoria posterior.

A estrutura usa abordagem de processo, pensamento baseado em risco, criterios de
aceitacao, rastreabilidade, evidencia e controle de informacao documentada
inspirados na ISO 9001. Isso **nao** declara certificacao nem conformidade formal do
repositorio, do produto ou deste documento. Na data de emissao, a referencia
publicada aplicavel e a [ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html),
enquanto a [proxima edicao esta em desenvolvimento](https://www.iso.org/standard/88464.html).
O formato tambem considera a orientacao oficial da ISO sobre
[informacao documentada da ISO 9001:2015](https://www.iso.org/files/live/sites/isoorg/files/standards/docs/en/iso_9001_2015_guidance_documented_information.pdf)
e a [ISO 10013:2021](https://www.iso.org/standard/75736.html).

## 2. Escopo

### 2.1 Incluido

- escolha de golpes, itens e trocas pela IA de treinadores;
- comportamento de oponentes selvagens e batalhas por link;
- tabelas, estado em RAM, RNG, comparacoes, limites e defeitos conhecidos;
- atualizacao, movimento aleatorio, direcao, atraso, animacao e colisao de sprites;
- visao de treinadores, aproximacao, interrupcao do jogador e inicio de conversa/batalha;
- movimento roteirizado, simulacao de joypad, RLE e busca de caminho existente;
- despacho de dialogo, servicos de NPC, flags de evento e maquinas de estado dos mapas;
- inventario dos {len(objects)} `object_event` em {object_maps} mapas, {len(headers)}
  cabecalhos de treinador e {len(states)} estados nomeados de script;
- recomendacoes para uma implementacao fiel e para um modo melhorado capaz de
  modelar o estilo do jogador, navegar e iniciar interacoes.

### 2.2 Excluido

- transcricao integral de todos os dialogos, que continuam controlados em `text/`;
- IA ou regras de Pokemon Yellow e geracoes posteriores;
- classificacao narrativa subjetiva de cada personagem;
- afirmacao de intencao original quando o codigo apenas permite observar o efeito;
- qualquer uso de aprendizado no modo fiel sem uma decisao formal de produto.

## 3. Objetivos e criterios da qualidade

| ID | Objetivo | Criterio verificavel |
|---|---|---|
| AI-Q01 | Cobertura | 47 classes, 918 objetos, 322 cabecalhos e 199 estados de script inventariados. |
| AI-Q02 | Fidelidade | Mesmas entradas, bytes de RNG e estado produzem a mesma acao no modo `GEN1_FIDELITY`. |
| AI-Q03 | Rastreabilidade | Cada algoritmo e tabela aponta para arquivo, simbolo ou linha de origem. |
| AI-Q04 | Separacao de melhoria | Comportamento novo existe somente em `ENHANCED` e nao altera saves/replays fieis. |
| AI-Q05 | Testabilidade | RNG, relogio, input, mapa e persistencia sao portas injetaveis. |
| AI-Q06 | Manutencao | Mudancas relevantes regeneram este arquivo e atualizam Graphify. |

## 4. Conclusao executiva

Nao ha perceptron, rede neural, aprendizado de maquina, modelo estatistico treinado,
minimax, Monte Carlo ou behavior tree nesta ROM. O comportamento e composto por:

1. **regras deterministicas e tabelas**, como flags, classes, tipos e ponteiros;
2. **heuristicas de pontuacao**, que alteram quatro notas de golpe e preservam apenas
   as menores;
3. **sorteios pseudoaleatorios**, usados para desempate, movimento e chance de itens;
4. **maquinas de estado**, selecionadas por indices de script e bytes do sprite;
5. **sequencias predefinidas**, muitas vezes comprimidas por RLE;
6. **uma busca gulosa Manhattan**, usada apenas em eventos especificos para montar
   uma sequencia ate o jogador.

Portanto, o jogo e deterministico quando estado inicial, input, temporizacao do
registrador `rDIV` e sequencia aleatoria sao fixados. Ele nao registra como o jogador
luta, nao aprende preferencias, nao muda pesos e nao transfere conhecimento entre
batalhas. A aparente inteligencia emerge de regras pequenas, dados de classe e RNG.

## 5. Visao arquitetural

```mermaid
flowchart LR
    Loop[Loop do overworld] --> MapScript[Maquina de estado do mapa]
    Loop --> Sprites[Atualizacao de sprites]
    Sprites --> Movimento[Politica WALK/STAY/script]
    Movimento --> Colisao[Tiles, tela e outros sprites]
    MapScript --> Visao[Visao de treinador]
    Visao --> Aproxima[Sequencia ate o jogador]
    Aproxima --> Dialogo[Texto e evento]
    Dialogo --> Batalha[Inicio de batalha]
    Batalha --> AcaoAI[Item ou troca por classe]
    Batalha --> GolpeAI[Pontuacao de golpes]
    RNG[RNG] --> Movimento
    RNG --> AcaoAI
    RNG --> GolpeAI
```

| Processo | Fonte principal | Simbolos |
|---|---|---|
| Atualizacao de sprites | `home/update_sprites.asm`, `engine/overworld/sprite_collisions.asm` | `UpdateSprites`, `_UpdateSprites` |
| Movimento autonomo | `engine/overworld/movement.asm` | `UpdateNPCSprite`, `TryWalking`, `CanWalkOntoTile` |
| Movimento coordenado | `home/npc_movement.asm`, `engine/overworld/auto_movement.asm` | `RunNPCMovementScript`, tabelas Pallet/Pewter |
| Caminho ate jogador | `engine/overworld/pathfinding.asm` | `CalcPositionOfPlayerRelativeToNPC`, `FindPathToPlayer` |
| Visao e aproximacao | `engine/overworld/trainer_sight.asm`, `home/trainers.asm` | `TrainerEngage`, `TrainerWalkUpToPlayer` |
| Scripts e dialogos | `scripts/*.asm`, `home/text_script.asm`, `home/text.asm` | `CallFunctionInTable`, `DisplayTextID`, `TextCommandProcessor` |
| IA de acao | `engine/battle/trainer_ai.asm`, `data/trainers/ai_pointers.asm` | `TrainerAI`, `TrainerAIPointers` |
| IA de golpe | `engine/battle/trainer_ai.asm`, `data/trainers/move_choices.asm` | `AIEnemyTrainerChooseMoves`, modificadores 1-4 |
| Dados de batalha | `data/moves/moves.asm`, `data/types/type_matchups.asm` | `Moves`, `TypeEffects` |
| Estado | `ram/wram.asm`, `ram/hram.asm` | `wSpriteStateData*`, `wAICount`, `wBuffer`, `hFindPath*` |

## 6. Aleatoriedade e reprodutibilidade

`Random` chama `Random_`. Esta rotina le duas vezes o registrador de divisao de
hardware `rDIV`, soma uma leitura a `hRandomAdd` com carry e subtrai outra de
`hRandomSub` com borrow. O byte normalmente consumido pela logica de NPC e
`hRandomAdd`. Em batalha, `BattleRandom` deve ser usado; batalhas por link consomem
uma lista sincronizada entre os dois aparelhos.

Isto nao e aleatoriedade criptografica e tambem nao e uma decisao aprendida. Para a
reescrita, o contrato de RNG deve expor `next_overworld_byte()` e
`next_battle_byte()`, permitir seed/trace injetavel e preservar a ordem de consumo.
Alterar uma chamada aparentemente irrelevante pode mudar todas as decisoes seguintes.

## 7. IA de batalha

### 7.1 Ordem das decisoes

1. `SelectEnemyMove` elimina estados em que nao se pode escolher: recharge, Rage,
   charge, Thrash, sono, congelamento, trapping e Bide.
2. Oponente selvagem recebe o conjunto original; treinador chama
   `AIEnemyTrainerChooseMoves`.
3. A selecao escolhe um dos quatro slots por faixas de aproximadamente 25%; slot
   vazio ou disabled repete o sorteio.
4. No turno da acao adversaria, `TrainerAI` pode substituir o golpe por item ou troca.
5. Se a rotina retorna carry, a acao especial consumiu o turno; caso contrario o
   golpe escolhido e executado.

Oponentes nao-link tem PP ilimitado: os valores sao carregados, mas a execucao nao
os decrementa. A selecao normal tambem nao exclui PP zero. Em link, a decisao vem do
outro jogador e as regras normais de PP pertencem ao lado humano remoto.

### 7.2 Pontuacao dos quatro golpes

O vetor `wBuffer` inicia como `[10, 10, 10, 10]`. O slot disabled recebe `80`.
Cada camada configurada para a classe altera as notas; ao final, somente os slots
com a **menor nota** sobrevivem. Todos os sobreviventes continuam equiprovaveis no
sorteio por slot. Nao ha softmax ou soma ponderada de probabilidades.

| Camada | Regra | Alteracao |
|---|---|---:|
| 1 | Se o jogador ja tem status, golpe sem dano cujo efeito esta em `StatusAilmentMoveEffects` | `+5` (desencoraja fortemente) |
| 2 | Apenas quando `wAILayer2Encouragement == 1`; favorece faixas numericas de efeitos de stat/status | `-1` |
| 3 | Compara tipo do golpe com `TypeEffects`; super efetivo | `-1` |
| 3 | Resistente/imune e existe outro golpe considerado melhor | `+1` |
| 4 | Rotina vazia e nao usada por classe alguma | `0` |

A camada 2 ocorre nominalmente apenas na segunda oportunidade apos o Pokemon entrar:
o contador comeca em zero e e incrementado no inicio da execucao adversaria. Ela
compara **intervalos de IDs de efeito**, nao utilidade real no estado atual.

### 7.3 Comparacao de tipos

`AIGetTypeEffectiveness` consulta `TypeEffects` com o tipo do golpe e os dois tipos
do jogador. A neutralidade interna e `$10` hexadecimal; as entradas usam 20, 10 ou
0. A rotina para na primeira correspondencia e nao combina os dois tipos. Assim, nao
calcula fraqueza 4x, resistencia 1/4 ou cancelamento entre tipos. A camada ainda pode
favorecer golpe sem dano porque nao exige `power > 0` no caminho super efetivo.

Ao procurar alternativa para um golpe resistido, considera melhores `Super Fang`,
golpes de dano especial fixo, `Fly` e qualquer golpe de **outro tipo** com poder
nao zero; nao estima dano, STAB, accuracy, velocidade, KO, status, setup ou resposta
do jogador.

### 7.4 Acoes especiais por treinador

`wAICount` inicia em `$ff` ao enviar um Pokemon. Na primeira avaliacao, recebe o
limite da classe. Somente uma acao efetivamente usada decrementa o contador; trocar
e enviar outro Pokemon reinicializa o limite para esse novo ativo. `GenericAI` nunca
age. Limiares exatos usam um byte `[0,255]` e o macro `percent = *255/100`.

| Rotina | Probabilidade exata por avaliacao | Condicao e acao |
|---|---:|---|
| `JugglerAI` | 64/256 = 25% | Troca se houver pelo menos dois Pokemon nao desmaiados. |
| `BlackbeltAI` | 32/256 = 12,5% | Usa X Attack. |
| `GiovanniAI` | 64/256 = 25% | Usa Guard Spec. |
| `CooltrainerMAI` | 64/256 = 25% | Usa X Attack. |
| `CooltrainerFAI` | efetivamente 100% sob limiar de HP | Bug: o `ret nc` da intencao de 25% esta comentado; Hyper Potion abaixo de 1/10, senao troca abaixo de 1/5. |
| `BrockAI` | deterministica | Full Heal se o ativo tiver qualquer status. |
| `MistyAI` | 64/256 = 25% | X Defend. |
| `LtSurgeAI` | 64/256 = 25% | X Speed. |
| `ErikaAI` | 128/256 = 50% | Super Potion somente abaixo de 1/10 do HP maximo. |
| `KogaAI` | 64/256 = 25% | X Attack. |
| `BlaineAI` | 64/256 = 25% | Super Potion sem verificar HP, inclusive cheio. |
| `SabrinaAI` | 64/256 = 25% | Hyper Potion abaixo de 1/10. |
| `Rival2AI` | 32/256 = 12,5% | Potion abaixo de 1/5. |
| `Rival3AI` | 32/256 = 12,5% | Full Restore abaixo de 1/5. |
| `LoreleiAI` | 128/256 = 50% | Super Potion abaixo de 1/5. |
| `BrunoAI` | 64/256 = 25% | X Defend. |
| `AgathaAI` | 20/256 = 7,8125% para troca | Se RNG <20 tenta troca; com HP abaixo de 1/4, RNG 20..127 usa Super Potion (42,1875%); demais casos nao agem. |
| `LanceAI` | 128/256 = 50% | Hyper Potion abaixo de 1/5. |
| `GenericAI` | 0% | Retorna sem usar acao. |

`AISwitchIfEnoughMons` apenas conta vivos. `EnemySendOut` escolhe o primeiro membro
vivo, em ordem de equipe, que nao seja o atual. Nao ha comparacao de tipos, golpes,
HP relativo ou matchup para escolher a troca.

### 7.5 Itens implementados

- Potion cura 20 HP; Super Potion 50; Hyper Potion 200.
- Full Restore restaura HP maximo e limpa status; Full Heal limpa status.
- X Attack, X Defend e X Speed chamam o mesmo mecanismo dos modificadores de stat.
- Guard Spec ativa protecao equivalente a Mist.
- X Accuracy, Dire Hit e X Special tem rotinas, mas nao sao apontados pela tabela de
  classes atual.
- Itens de cura limitam ao MaxHP. A IA nao consulta inventario nem dinheiro.

### 7.6 Golpes especiais dos times

`LoneMoves` injeta Bide, BubbleBeam, Thunderbolt, Mega Drain, Toxic, Psywave,
Fire Blast e Fissure em indices definidos por scripts de lider. `TeamMoves` injeta
Blizzard para Lorelei, Fissure para Bruno, Toxic para Agatha e Barrier para Lance.
Isso altera o conjunto disponivel, nao o algoritmo de decisao.

### 7.7 Tabela completa por classe

Camadas: 1=status redundante; 2=efeitos favorecidos; 3=tipo. O limite e o numero
maximo de acoes especiais efetivamente usadas por Pokemon ativo.

| Classe | Limite | Rotina de acao | Camadas de golpe |
|---|---:|---|---|
""".rstrip())

    for trainer_class in classes:
        count, routine = ai_actions[trainer_class]
        out.append(f"| `{trainer_class}` | {count} | `{routine}` | {move_layers[trainer_class]} |")

    out.append(f"""

## 8. Comportamento dos NPCs no mapa

### 8.1 Modelo de dados

Cada `object_event` declara coordenadas, sprite, `WALK`/`STAY`, restricao de direcao,
ID de texto e, quando aplicavel, item ou oponente. O mapa corrente materializa ate
`MAX_OBJECT_EVENTS = 16`; existem 16 pares de estruturas `wSpriteStateData1` e
`wSpriteStateData2`, incluindo o jogador.

`StateData1` contem imagem, estado de movimento, vetores por pixel, posicao de tela,
frames, direcao e bits de colisao. `StateData2` contem deslocamento acumulado,
coordenada no mapa, byte de politica/script, prioridade na grama, atraso, direcao
original, picture ID e slot de VRAM. `wMapSpriteData` guarda restricao/texto e
`wMapSpriteExtraData` guarda classe/item e conjunto/nivel.

### 8.2 Maquina de estados de movimento

| Estado | Valor/bit | Comportamento |
|---|---|---|
| Nao inicializado | status `0` | Inicializa como pronto e imagem invisivel ate posicionamento. |
| Pronto | status `1` | Pode escolher direcao quando jogador nao esta andando e fonte nao esta aberta. |
| Atrasado | status `2` | Decrementa `MOVEMENTDELAY`; ao chegar a zero volta a pronto. |
| Andando | status `3` | Move 1 pixel por tick durante 16 ticks e avanca frame a cada 4. |
| Face player | bit 7 | Ao conversar, gira para o jogador, salvo excecao do capitao da S.S. Anne. |
| Script local | byte 1 `< WALK` | Consome `wNPCMovementDirections` ate sentinela `$ff`. |
| Coordenado | sprite offset selecionado | `DoScriptedNPCMovement` move NPC em sincronia de 2 pixels com o jogador. |

### 8.3 WALK, STAY e direcoes

Ha {movement_counts['WALK']} objetos `WALK` e {movement_counts['STAY']} objetos
`STAY`. Para ambos, a engine sorteia um byte. Os dois bits superiores dividem as
quatro direcoes em faixas de 64 resultados:

- `ANY_DIR`: Down, Up, Left e Right com 25% nominal cada;
- `UP_DOWN`: Up ou Down com 50% cada;
- `LEFT_RIGHT`: Left ou Right com 50% cada;
- `DOWN`, `UP`, `LEFT`, `RIGHT`: direcao fixa;
- `NONE`: sem restricao adicional, mas normalmente combinado com `STAY`;
- `BOULDER_MOVEMENT_BYTE_2`: tratamento de objeto empurravel.

`STAY` ainda escolhe uma direcao e pode virar, mas `CanWalkOntoTile` impede o passo.
`WALK` tenta deslocar. Depois de andar ou falhar, o atraso recebe `RNG & $7f`, faixa
0..127; zero sofre underflow e dura 256 ticks. O resultado e vagar local sem destino,
memoria, perseguicao ou agenda.

Distribuicao declarada no corpus:

| Restricao | Objetos |
|---|---:|
""".rstrip())
    for constraint, count in sorted(constraint_counts.items(), key=lambda item: (-item[1], item[0])):
        out.append(f"| `{constraint}` | {count} |")

    out.append(f"""

### 8.4 Passabilidade e colisao

Para movimento autonomo, `CanWalkOntoTile` compara o tile destino com a lista de
colisao do tileset apontada por `wTilesetCollisionPtr`, impede sair da regiao de
tela, chama `DetectCollisionBetweenSprites` e verifica deslocamentos acumulados.
Movimento roteirizado (`byte 1 < WALK`) e aceito antes dessas verificacoes, pois os
scripts assumem trajetos validos.

`DetectCollisionBetweenSprites` percorre os 16 slots, descarta slot vazio ou
offscreen, ajusta coordenadas em 7/9 pixels conforme o vetor e grava direcoes de
colisao e uma mascara de quais sprites colidiram. Nao ha steering, reserva global de
rota, negociacao de passagem ou desvio local.

Defeitos relevantes para compatibilidade:

- o teste vertical de deslocamento pode prender um sprite apos andar cinco passos
  para cima, enquanto o equivalente horizontal compara sem desvio condicional;
- atraso zero representa 256 ticks por underflow;
- um byte `WALK` encontrado dentro da lista de movimento local segue um indice
  aparentemente incorreto (`$fe`), marcado como bug no fonte;
- scripts locais ignoram a passabilidade normal e podem atravessar geometria se os
  dados estiverem errados.

### 8.5 Visao de treinador e interrupcao do jogador

O jogo **ja implementa** NPC que detecta, para e aborda o jogador:

1. `CheckForEngagingTrainers` percorre cabecalhos ainda nao derrotados.
2. `TrainerEngage` exige sprite visivel, alinhamento exato no mesmo X ou Y, distancia
   dentro do alcance e jogador a frente da direcao atual.
3. Nao existe ray cast por todos os tiles entre ambos; a logica e geometrica e os
   mapas posicionam treinadores para que o corredor seja valido.
4. Ao detectar, define `BIT_SEEN_BY_TRAINER`, carrega classe/conjunto, toca musica,
   mostra a exclamacao e bloqueia o fluxo normal.
5. `TrainerWalkUpToPlayer` escreve N-1 passos retos ate ficar adjacente.
6. O texto pre-batalha e exibido e a batalha inicia. A flag persistente impede nova
   abordagem depois da derrota.

`view_range` do macro `trainer` e armazenado como `valor << 4`, portanto cada unidade
representa 16 pixels/um passo de grade. Alcance zero desativa deteccao automatica,
mas o treinador ainda pode ser acionado ao conversar.

### 8.6 Busca de caminho existente

`FindPathToPlayer` nao e A*. Primeiro, `CalcPositionOfPlayerRelativeToNPC` calcula
distancias absolutas em passos de 16 pixels e flags de quadrante. A busca entao:

1. calcula quanto falta em X e Y;
2. reduz o eixo com maior distancia;
3. em empate, reduz X;
4. grava uma direcao por passo em `wNPCMovementDirections2`;
5. encerra com `$ff`.

E um caminho Manhattan guloso, sem mapa, custo, fila, visitados ou obstaculos. E
usado para Oak em Pallet e para o rival no laboratorio. Como a sequencia posterior
e tratada como script, a seguranca depende do evento e do layout conhecidos.

### 8.7 Movimento roteirizado

Existem dois mecanismos:

- `MoveSprite` copia uma lista terminada em `$ff` para `wNPCMovementDirections` e
  bloqueia input; `UpdateNPCSprite` consome uma entrada por passo.
- movimento coordenado decodifica listas RLE para o jogador e o NPC, simula joypad e
  atualiza o NPC em passos de 2 pixels para manter sincronismo. As tabelas globais
  cobrem Oak em Pallet e os guias de Pewter; muitos mapas possuem sequencias locais.

RLE armazena pares `<byte, repeticoes>` e sentinela `$ff`. Este mecanismo conduz
entradas de sala, empurra o jogador em portoes, move rivais/Rockets, executa pisos de
seta e sincroniza cenas. Ele e uma cutscene deterministica, nao navegacao autonoma.

### 8.8 Dialogo, servicos e eventos

Ao pressionar A diante de um objeto, a engine identifica o sprite, marca o bit para
encarar o jogador, resolve seu text ID e executa o ponteiro do mapa. `text_asm`
permite que um dialogo execute codigo e altere estado. Ao fechar, as direcoes
originais sao restauradas e os sprites recarregados.

O primeiro byte do texto possui despachos globais para Mart, enfermeira, PCs,
vending machine, prize vendor e Cable Club. Outros servicos sao scripts de mapa:

| Arquetipo | Comportamento | Fonte principal |
|---|---|---|
| Mart | Carrega lista de itens, menu, preco, dinheiro e inventario | `engine/events/pokemart.asm`, `data/items/marts.asm` |
| Centro Pokemon | Pergunta, cura equipe, animacao e retorno | `engine/events/pokecenter.asm` |
| Cable Club | Estados de recepcao, espera e link | `engine/link/cable_club_npc.asm` |
| Troca NPC | Valida especie, confirma, cria recebido e roda sequencia | `engine/events/in_game_trades.asm`, `data/events/trades.asm` |
| Day Care | Deposito, experiencia por passos, custo e retirada | `scripts/Daycare.asm`, `engine/overworld/daycare_exp.asm` |
| Name Rater | Valida propriedade e executa naming screen | `scripts/NameRatersHouse.asm` |
| Fosil | Recebe fossil, usa evento/tempo e entrega especie | `scripts/CinnabarLabFossilRoom.asm`, `engine/events/cinnabar_lab.asm` |
| Prize vendor | Valida Coin Case, saldo, equipe/box e concede premio | `engine/events/prize_menu.asm`, `data/events/prizes.asm` |
| Bike Shop | Condiciona preco/voucher e entrega bicicleta | `scripts/BikeShop.asm` |
| Safari gate | Entrada, taxa, Balls, passos e saida automatica | `scripts/SafariZoneGate.asm`, `engine/events/hidden_events/safari_game.asm` |
| Oak's aides | Conta especies capturadas e concede item por limiar | `engine/events/oaks_aide.asm` |
| Treinador | Antes/fim/depois, flag persistente, classe e conjunto | `home/trainers.asm`, `scripts/*.asm` |

Todos esses fluxos sao regras de negocio deterministicas sobre flags, inventario,
dinheiro, party, coordenadas e respostas do jogador. Nenhum adapta a conversa ao
historico alem dos estados explicitamente salvos.

## 9. Tabelas e comparacoes utilizadas

| Tabela/estado | Chave comparada | Resultado |
|---|---|---|
| `TrainerAIPointers` | `wTrainerClass` | limite de uso e rotina de item/troca |
| `TrainerClassMoveChoiceModifications` | `wTrainerClass` | lista de camadas 1-4 |
| `AIMoveChoiceModificationFunctionPointers` | ID da camada | funcao de pontuacao |
| `StatusAilmentMoveEffects` | efeito do golpe | identifica status redundante |
| `Moves` | ID do golpe | efeito, poder, tipo, accuracy e PP |
| `TypeEffects` | tipo atacante/defensor | 20, 10 ou 0 para a heuristica |
| `TrainerDataPointers`/parties | classe e `wTrainerNo` | equipe e niveis |
| `LoneMoves`/`TeamMoves` | indice/classe | golpe especial injetado |
| `TrainerAIPointers` RNG | byte contra limiar | usar item, trocar ou nao agir |
| cabecalho `trainer` | flag, alcance, textos | visao, repeticao e dialogos |
| `wEventFlags` | bit de evento | ramo de script e persistencia |
| tabelas `*ScriptPointers` | indice `w*CurScript` | proximo estado do mapa |
| `object_event` | sprite ID/text ID | movimento, interacao, item ou oponente |
| collision list do tileset | tile destino | passo autonomo permitido |
| `SpriteCollisionBitTable` | indice do outro sprite | mascara de colisao |
| `NPCMovementDirectionsToJoypadMasksTable` | direcao NPC | input simulado equivalente |
| tabelas RLE/movimento | byte e repeticoes | sequencia de cutscene |
| ponteiros de texto do mapa | text ID | texto simples ou `text_asm` |
| despachos `TX_SCRIPT_*` | primeiro byte | servico global de NPC |

## 10. Classificacao dos algoritmos

| Mecanismo | Classe tecnica | Aprende? | Planeja? | Usa RNG? |
|---|---|---:|---:|---:|
| Escolha de golpe de treinador | utility scoring discreto + filtro argmin | Nao | Nao | Sim, desempate |
| Item/troca de treinador | regras probabilisticas por classe | Nao | Nao | Sim |
| Golpe selvagem | escolha uniforme por slot valido | Nao | Nao | Sim |
| Movimento WALK | random walk restrito | Nao | Nao | Sim |
| Visao de treinador | linha cardinal + alcance + facing | Nao | Nao | Nao |
| Aproximacao de treinador | sequencia reta | Nao | Nao | Nao |
| `FindPathToPlayer` | guloso Manhattan | Nao | Um caminho sem obstaculos | Nao |
| Scripts de mapa | maquina de estados/tabela de funcoes | Nao | Sequencia predefinida | Ocasional |
| Dialogos/servicos | regras e transacoes | Nao | Nao | Ocasional |

Um perceptron exigiria vetor de features, pesos, produto escalar, limiar e, para
aprender, regra de atualizacao. Nenhum desses elementos existe aqui. As notas de
golpe podem parecer pesos, mas sao constantes temporarias reiniciadas a cada decisao
e ajustadas por `if`s; nao constituem perceptron.

## 11. Recomendacao para a reescrita fiel

### 11.1 Dois modos obrigatorios

```c
typedef enum {{
    GEN1_FIDELITY,
    ENHANCED
}} BehaviorMode;
```

`GEN1_FIDELITY` e criterio de aceitacao da migracao. Deve reproduzir tabelas,
ordem de comparacoes, overflow/underflow relevantes, bugs catalogados e consumo de
RNG. `ENHANCED` deve ser opt-in, versionado e testado separadamente. Misturar
melhorias na traducao impede provar equivalencia.

### 11.2 Limites DDD

| Bounded context | Responsabilidade |
|---|---|
| `BattleDecision` | observacao de batalha, pontuacao, item, troca e acao |
| `OverworldActors` | estado, percepcao, movimento, colisao e animacao de NPC |
| `Navigation` | grid, consulta de passabilidade, path e reserva de destino |
| `ScriptedEvents` | estado de mapa, flags, comandos, cutscenes e dialogos |
| `NpcServices` | mart, heal, trade, daycare, premios e demais transacoes |
| `PlayerModel` | historico agregado e previsao, inexistente no modo fiel |
| `Runtime` | RNG, input, relogio, bancos/memoria, audio e video |

### 11.3 SOLID pragmatico em C

- `BattleDecisionPolicy` recebe uma observacao imutavel e devolve uma intencao; nao
  executa animacao nem altera RAM diretamente.
- `MovementPolicy` decide destino; `CollisionQuery` valida; `ActorExecutor` aplica.
- `PerceptionPolicy` detecta jogador e emite evento; dialogo e batalha sao consumidores.
- `ScriptVM` interpreta comandos e depende de portas para mapa, texto, inventario e batalha.
- RNG entra por interface pequena; fixtures fornecem bytes exatos.
- tabelas sao dados tipados e validados, nao `switch` duplicado em varios modulos.

### 11.4 Refactoring incremental

1. caracterizar rotina ASM com snapshot de RAM e trace de RNG;
2. extrair leitores C das tabelas sem mudar formato;
3. implementar funcao pura equivalente;
4. executar diferencial ASM/C para milhares de estados;
5. substituir uma chamada por vez;
6. somente depois separar nomes, structs e estrategias;
7. ativar melhorias atras de `BehaviorMode`.

## 12. Melhorias possiveis no modo ENHANCED

### 12.1 IA de batalha mais forte e explicavel

Use utility AI deterministica, nao uma rede neural como primeiro passo. Para cada
acao legal, estime dano esperado, chance de KO, risco recebido, valor de status,
setup, accuracy, STAB, matchup, HP, velocidade, PP e custo de troca. Perfis de
treinador alteram pesos e tolerancia a risco. Empates usam RNG injetavel.

Uma busca curta de 1-2 turnos pode ser adicionada para chefes, com limite fixo de
nos e avaliacao reproduzivel. Isso e mais auditavel e mais facil de testar que um
modelo opaco, mantendo a personalidade controlada por dados.

### 12.2 Aprender como o jogador joga

E possivel, mas nao pertence ao modo fiel. Recomenda-se um `PlayerModel` local,
limitado e interpretavel:

- contadores com decaimento exponencial para Fight/Item/Switch/Run;
- frequencia por faixa de HP e vantagem de tipo;
- repeticao do ultimo golpe/tipo;
- tendencia a trocar diante de status ou matchup ruim;
- uso de cura e preferencia ofensiva/defensiva;
- janela limitada ou decaimento para nao eternizar comportamento antigo.

O modelo pode prever a proxima **categoria de acao** por distribuicao condicional.
Um perceptron multiclasses simples e tecnicamente possivel, mas so deve entrar apos
uma baseline de contadores: exige normalizacao, taxa de aprendizado, pesos no save,
controle de overflow, versionamento e testes de estabilidade. Ele nao e necessario
para produzir adaptacao convincente.

Primeiro execute em `shadow mode`: registra previsao e acerto, mas a IA continua
fiel. Depois, no modo melhorado, use a previsao apenas como um termo limitado da
utility, com clamp, para evitar que uma amostra pequena domine a decisao.

Controles obrigatorios:

- opcao para zerar aprendizado e desativar adaptacao;
- schema de save versionado e migracao;
- limite de peso/contador e aritmetica definida;
- nenhuma coleta externa; dados permanecem no save local;
- seed e trace para reproduzir bugs;
- dificuldade e taxa de adaptacao comunicadas por configuracao, nao escondidas.

### 12.3 NPCs andando pelo mapa

Introduza um `NavigationGrid` derivado da colisao do mapa e use A* para destinos
longos. Para movimentacao local, reserve a proxima celula, detecte deadlock e aplique
prioridade estavel por actor ID. Portas, warps, ledges, agua e scripts precisam de
custos/capacidades explicitos.

Cada NPC pode ter agenda e maquina de estados: `Idle`, `Wander`, `Travel`, `Work`,
`Talk`, `Alert`, `ReturnHome`, `Scripted`. O path e recalculado somente quando alvo
ou mapa muda/bloqueia; nao a cada frame. Mapas descarregados usam simulacao de baixa
frequencia ou saltos de agenda, evitando tentar manter sprites ativos globalmente.

### 12.4 Parar o jogador para conversar

Generalize o pipeline ja usado por treinadores e Oak:

1. `PerceptionPolicy` detecta por alcance, cone de visao, trigger ou evento;
2. um arbitro garante que apenas um NPC reserve a interacao;
3. input do jogador e bloqueado por token com liberacao garantida;
4. NPC calcula caminho ate uma celula adjacente alcancavel;
5. ambos se encaram;
6. dialogo roda e pode emitir quest/batalha/transacao;
7. estado e input sao restaurados mesmo em cancelamento ou troca de mapa.

Inclua cooldown, prioridade de evento, verificacao de cutscene/batalha/menu e uma
rota de cancelamento. Sem isso, dois NPCs podem abordar ao mesmo tempo ou prender o
jogador.

### 12.5 Comportamentos adicionais seguros

- reacoes a horario, clima, historia e badges por regras declarativas;
- memoria curta de conversa e quest flags tipadas;
- fuga, patrulha, curiosidade e retorno ao posto;
- barks contextuais sem interromper o jogador;
- ajuda de navegacao e seguidores com reserva de celula;
- perfis de treinador que usam estrategia coerente com classe e time;
- telemetria local de decisao para explicar por que uma acao foi escolhida.

## 13. Estrategia TDD

### 13.1 Testes de caracterizacao obrigatorios

| ID | Caso | Evidencia esperada |
|---|---|---|
| AI-T01 | Classe sem camadas | conjunto original e sorteio por slot existente |
| AI-T02 | Status ja presente | golpe de status sem dano recebe `+5` |
| AI-T03 | Segundo momento do ativo | camada 2 ocorre somente com contador igual a 1 |
| AI-T04 | Super efetivo simples | nota `-1` pela primeira entrada de `TypeEffects` |
| AI-T05 | Pokemon dual type | reproduzir a primeira correspondencia, sem multiplicacao |
| AI-T06 | Disabled | slot recebe 80 e nao e selecionado quando ha alternativa |
| AI-T07 | Empate de minimos | distribuicao por slots e rejeicao de vazios seguem bytes gravados |
| AI-T08 | Blaine com HP cheio | pode desperdiçar Super Potion no limiar de RNG |
| AI-T09 | Cooltrainer F | cura/troca sem gate de 25% |
| AI-T10 | Agatha fronteiras 19/20/127/128 | troca, cura ou nenhuma acao exatamente como ASM |
| AI-T11 | Troca | primeiro membro vivo nao atual e escolhido |
| AI-T12 | Limite de item | decrementa apenas apos acao usada e reinicializa por ativo |
| NPC-T01 | WALK + ANY_DIR | quatro faixas de 64 bytes escolhem direcoes corretas |
| NPC-T02 | STAY | muda facing, nunca coordenada de mapa |
| NPC-T03 | atraso zero | dura 256 ticks em fidelidade |
| NPC-T04 | colisao | mascara e bloqueio iguais para todos os offsets limite |
| NPC-T05 | trainer sight | alinhamento, facing, distancia e flag nas fronteiras |
| NPC-T06 | alcance zero | nao aborda automaticamente; conversa manual funciona |
| NPC-T07 | approach | gera N-1 passos e termina adjacente |
| NPC-T08 | path guloso | reduz maior eixo e prefere X no empate |
| NPC-T09 | RLE | expande pares e preserva sentinela `$ff` |
| NPC-T10 | dialogo | encara durante texto e restaura direcao ao fechar |
| NPC-T11 | evento derrotado | treinador nao volta a abordar |
| NPC-T12 | input lock | toda saida de script libera controle exatamente uma vez |

### 13.2 Diferencial e propriedades

- rode todos os 256 bytes de RNG para cada rotina probabilistica;
- gere combinacoes dos quatro golpes, efeitos, tipos e status;
- compare RAM observavel, acao, carry e quantidade de bytes aleatorios consumidos;
- para movimento, varie os 256 bytes, bordas de tela, tile e 16 slots de colisao;
- para scripts, use golden traces de estado, flags, input simulado e sequencia textual;
- execute `GEN1_FIDELITY` e `ENHANCED` em suites separadas para impedir vazamento.

## 14. Riscos e nao conformidades conhecidas

| ID | Risco/defeito | Efeito | Tratamento |
|---|---|---|---|
| AI-R01 | Tipo dual nao combinado | escolha subotima | preservar em fiel; corrigir em melhorado |
| AI-R02 | Cooltrainer F sem retorno probabilistico | cura/troca muito frequente | teste de bug e feature flag de correcao |
| AI-R03 | Blaine ignora HP | item desperdicado | preservar/corrigir por modo |
| AI-R04 | Camada 2 depende de contador transitorio | preferencia ocorre uma vez | teste de sequencia, nao apenas unitario isolado |
| AI-R05 | PP inimigo ilimitado | diverge de regras do jogador | contrato explicito por modo |
| AI-R06 | RNG acoplado a `rDIV` | replay diverge por ordem/timing | porta de RNG e trace |
| NPC-R01 | path guloso ignora obstaculos | caminho invalido fora de cena prevista | manter apenas em scripts; A* no melhorado |
| NPC-R02 | script ignora colisao | atravessa mapa se dado errado | validar trajetos estaticamente |
| NPC-R03 | underflow de atraso | pausa longa inesperada | teste e opcao de correcao |
| NPC-R04 | limite de deslocamento assimetrico | NPC prende/vaga diferente por eixo | snapshot e correcao por modo |
| NPC-R05 | abordagem sem arbitragem geral | extensao pode gerar disputa | interaction coordinator |
| NPC-R06 | aprendizado persistente sem versao | save incompativel | schema e migracao |
| NPC-R07 | IA adaptativa muito forte | experiencia injusta | clamp, dificuldade e reset |

## 15. Rastreabilidade de requisitos

| Requisito | Fonte | Teste/aceitacao |
|---|---|---|
| AI-REQ-001 Escolher golpe fiel | `trainer_ai.asm`, `move_choices.asm` | AI-T01..AI-T07 |
| AI-REQ-002 Usar item/troca fiel | `trainer_ai.asm`, `ai_pointers.asm` | AI-T08..AI-T12 |
| AI-REQ-003 Preservar RNG | `home/random.asm`, `engine/math/random.asm`, `BattleRandom` | trace byte a byte |
| NPC-REQ-001 Atualizar movimento | `movement.asm`, `sprite_collisions.asm` | NPC-T01..NPC-T04 |
| NPC-REQ-002 Abordar jogador | `trainer_sight.asm`, `home/trainers.asm` | NPC-T05..NPC-T07 |
| NPC-REQ-003 Executar caminhos/scripts | `pathfinding.asm`, `auto_movement.asm` | NPC-T08..NPC-T09 |
| NPC-REQ-004 Interagir e persistir | `text_script.asm`, `scripts/*.asm` | NPC-T10..NPC-T12 |
| ENH-REQ-001 Melhorar sem regressao | `BehaviorMode` e ADR futuro | suite fiel continua identica |
| ENH-REQ-002 Aprender com controle | `PlayerModel` futuro | reset, clamp, migracao e shadow metrics |

## 16. Controle de mudancas e Graphify

Regenerar apos alterar objetos, trainer headers, scripts, movimento, colisao, RNG,
IA de batalha ou tabelas relacionadas:

```sh
python3 tools/generate_npc_ai_document.py
python3 tools/generate_npc_ai_document.py --check
$(cat graphify-out/.graphify_python) tools/graphify_rgbds.py .
$(cat graphify-out/.graphify_python) -m graphify export html
```

Revisao obrigatoria deve confirmar diff do documento, assertions do gerador, testes
afetados e grafo atualizado. O HTML e `graphify-out/graph.html`; o JSON consultavel
por agentes e `graphify-out/graph.json`.

## 17. Evidencias e aprovacao

### 17.1 Evidencias desta revisao

- consulta Graphify expandida com vocabulario do proprio grafo;
- leitura direta das rotinas e tabelas citadas;
- inventario deterministico dos fontes ASM;
- assertions de 47 classes, 918 objetos, 322 cabecalhos e 199 estados;
- verificacao de sintaxe do gerador e reproducibilidade do Markdown;
- atualizacao do grafo e export HTML apos emissao.

### 17.2 Checklist do aprovador

- [ ] Escopo e modos fiel/melhorado aprovados.
- [ ] Bugs historicos classificados entre preservar e corrigir.
- [ ] Casos TDD possuem fixtures e responsavel.
- [ ] Inventarios conferem com o baseline.
- [ ] Modelo de aprendizado possui opt-out, reset e schema de save.
- [ ] Graphify e links de fonte estao atualizados.

## 18. Referencias internas

- `docs/001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md`
- `docs/002-2026-08-01-Informações_sobre_Pokemons.md`
- `engine/battle/trainer_ai.asm`
- `engine/battle/core.asm`
- `data/trainers/ai_pointers.asm`
- `data/trainers/move_choices.asm`
- `engine/overworld/movement.asm`
- `engine/overworld/sprite_collisions.asm`
- `engine/overworld/trainer_sight.asm`
- `engine/overworld/pathfinding.asm`
- `engine/overworld/auto_movement.asm`
- `home/trainers.asm`
- `home/text_script.asm`
- `macros/scripts/maps.asm`
- `ram/wram.asm`

## 19. Resumo quantitativo gerado

| Medida | Resultado |
|---|---:|
| Classes de treinador com configuracao de IA | {len(classes)} |
| Objetos de mapa | {len(objects)} |
| Mapas com objeto | {object_maps} |
| NPC/interacao generica | {category_counts['NPC/interacao']} |
| Treinadores declarados como objeto | {category_counts['Treinador']} |
| Pokemon estaticos hostis | {category_counts['Pokemon estatico']} |
| Itens/objetos coletaveis | {category_counts['Item/objeto coletavel']} |
| Pokemon/cenario interativo | {category_counts['Pokemon/cenario interativo']} |
| Obstaculos empurraveis | {category_counts['Obstaculo empurravel']} |
| Outros objetos interativos | {category_counts['Objeto interativo']} |
| Cabecalhos `trainer` com flag/visao/textos | {len(headers)} em {trainer_maps} mapas |
| Estados nomeados nas tabelas de script | {len(states)} em {state_maps} mapas |
| Pontos de chamada de movimento roteirizado | {len(calls)} |

## 20. Inventario completo dos objetos de mapa

Este anexo e a cobertura estrutural de todos os `object_event`, inclusive NPCs,
treinadores, Pokemon de cenario, encontros estaticos, itens e obstaculos. `Texto`
aponta para o comportamento/dialogo especifico no script correspondente.
""")

    for section, (map_name, map_events) in enumerate(
        sorted(grouped(objects, lambda item: item.map_name).items()), 1
    ):
        out.append(f"\n### 20.{section} Mapa `{map_name}`\n")
        out.append("| # | X,Y | Sprite | Movimento/restricao | Categoria | Alvo/dado | Texto | Fonte |")
        out.append("|---:|---|---|---|---|---|---|---|")
        for index, event in enumerate(map_events, 1):
            out.append(
                f"| {index} | {md_escape(event.x)},{md_escape(event.y)} | `{event.sprite}` | "
                f"`{event.movement}` / `{event.constraint}` | {event.category} | "
                f"{md_escape(event.target)} | `{event.text_id}` | `{event.source}` |"
            )

    out.append("""

## 21. Inventario completo dos cabecalhos de treinador

Cada linha registra a flag persistente, alcance de visao e os tres destinos de
texto. A correspondencia com classe/conjunto esta no objeto de mapa do anexo 20.
""")
    for section, (map_name, map_headers) in enumerate(
        sorted(grouped(headers, lambda item: item.map_name).items()), 1
    ):
        out.append(f"\n### 21.{section} Mapa `{map_name}`\n")
        out.append("| # | Evento | Alcance | Antes | Fim | Depois | Fonte |")
        out.append("|---:|---|---:|---|---|---|---|")
        for index, header in enumerate(map_headers, 1):
            out.append(
                f"| {index} | `{header.event}` | {header.view_range} | `{header.before}` | "
                f"`{header.end}` | `{header.after}` | `{header.source}` |"
            )

    out.append("""

## 22. Inventario das maquinas de estado dos mapas

Entradas `dw_const` ligam o byte `w*CurScript` a uma funcao. Estados locais sem
constante continuam visiveis pelos callsites e pelo arquivo de script, mas esta
tabela cobre todas as 199 entradas `SCRIPT_*` nomeadas pelo DSL atual. Existem ainda duas
entradas `dw_const` cujo simbolo contem `Script`, mas que sao manipuladores de texto
(`TEXT_BILLSHOUSE_ACTIVATE_PC` e `TEXT_CELADONMANSION3F_GAME_SCRIPT_PC`), nao estados de mapa.

| Mapa | Estado | Handler | Fonte |
|---|---|---|---|
""".rstrip())
    for state in states:
        out.append(f"| `{state.map_name}` | `{state.state}` | `{state.handler}` | `{state.source}` |")

    out.append("""

## 23. Inventario de chamadas de movimento roteirizado

Esta tabela lista toda chamada encontrada em `scripts/*.asm` e
`engine/events/*.asm` para as cinco primitivas centrais. O label proprietario e o
label mais proximo antes da chamada e serve como ponto inicial de auditoria.

| Operacao | Instrucao | Proprietario | Fonte |
|---|---|---|---|
""".rstrip())
    for call in calls:
        out.append(f"| `{call.operation}` | `{call.instruction}` | `{call.owner}` | `{call.source}` |")

    out.append("""

## 24. Registro de aprovacao

| Papel | Nome | Data | Resultado |
|---|---|---|---|
| Elaboracao tecnica | Codex | 2026-08-01 | Concluida |
| Revisao tecnica ASM | Pendente | - | Pendente |
| Revisao da arquitetura C | Pendente | - | Pendente |
| Aprovacao do documento | Pendente | - | Pendente |
""")

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if output differs")
    args = parser.parse_args()

    content = build_document()
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != content:
            print(f"out of date: {output}")
            return 1
        print(f"up to date: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"wrote {output} ({content.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
