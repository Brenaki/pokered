# AGENTS.md

## Contexto

Este repositorio e uma disassembly RGBDS de Pokemon Red/Blue mantida no
formato original de ROM de Game Boy. O objetivo deste workspace nao e apenas
editar assembly: e entender como o projeto `.asm` funciona para reescrever o
comportamento aos poucos em C, preservando compatibilidade e validando cada
passo com testes.

A regra central: o assembly atual e a especificacao executavel. Nao substitua
um trecho por C sem antes entender suas entradas, saidas, estado global,
efeitos colaterais, layout de memoria e comportamento observavel.

## Principios De Trabalho

- Preserve comportamento antes de melhorar design.
- Prefira fatias pequenas e reversiveis a reescritas amplas.
- Use TDD no codigo C novo: teste vermelho, implementacao minima, refactor.
- Use testes de caracterizacao para capturar o comportamento do assembly antes
  de trocar a implementacao.
- Aplique SOLID como design modular em C: modulos coesos, interfaces pequenas,
  dependencia explicita e inversao para hardware, RNG, input, audio, video,
  memoria e filesystem/test harness.
- Aplique Refactoring de Martin Fowler como transformacoes pequenas sob teste:
  extrair funcao, explicitar estado, substituir numero magico por nome,
  separar consulta de comando, introduzir objeto/struct de parametro quando
  reduzir acoplamento real.
- Aplique DDD de forma pragmatica: use a linguagem do dominio ja presente nos
  labels, constantes e dados do jogo; nao invente nomes genericos quando o
  jogo ja tem termos como party, move, map, tileset, battle, trainer, item,
  box, sprite, text e script.

## Comandos Uteis

- `make` constroi `pokered.gbc`, `pokeblue.gbc` e `pokeblue_debug.gbc`.
- `make compare` constroi ROMs/patches e valida hashes em `roms.sha1`.
- `make DEBUG=1 compare` tambem gera simbolos/mapas para diagnostico.
- `make red`, `make blue`, `make blue_debug`, `make red_vc`, `make blue_vc`
  constroem alvos especificos.
- `make tools` compila ferramentas auxiliares em `tools/`.
- `make tidy` remove objetos, ROMs, simbolos, mapas e patches gerados.
- `make clean` executa `tidy` e tambem remove graficos compilados.
- `make RGBDS=path/to/rgbds/` usa uma instalacao local do RGBDS.
- `BATTLE_TEST_VARIANTS=red,blue uv run --project rewrite/battle --frozen pytest rewrite/battle/tests`
  executa o contrato de caracterizacao da batalha nas duas ROMs.
- `$(cat graphify-out/.graphify_python) tools/graphify_rgbds.py .` cria ou
  atualiza o grafo ASM-aware e a wiki navegavel por agentes.
- `graphify query "pergunta"` consulta `graphify-out/graph.json` quando o grafo
  ja existe.

O build espera RGBDS compativel com a versao indicada por `.rgbds-version` e
pela CI (`v1.0.2+hotfix`). Se uma validacao falhar por versao de assembler,
registre isso em vez de tentar ajustar bytes manualmente.

## Como O Build Funciona

- `Makefile` e o orquestrador. Ele compila ferramentas C auxiliares, calcula
  includes com `tools/scan_includes`, monta objetos RGBDS, linka via
  `layout.link`, aplica `rgbfix` e compara hashes.
- `includes.asm` e passado para o assembler com `-P`; macros e constantes dali
  ficam disponiveis para os arquivos `.asm`.
- `layout.link` fixa a ordem das secoes e bancos: `ROM0`, `ROMX`, `WRAM0`,
  `VRAM`, `SRAM` e `HRAM`. Alterar secoes pode mudar enderecos e quebrar a ROM.
- `home.asm` contem o codigo fixo de `ROM0`: header, interrupcoes, rotinas
  comuns, bancos, texto, joypad, audio, vblank, memoria e helpers.
- `main.asm` inclui grande parte da engine e dados banked em `ROMX`:
  overworld, battle, menus, Pokemon, items, link, movie, slots e predefs.
- `maps.asm` agrega headers, scripts, objetos e blocos de mapas.
- `text.asm` agrega bancos de texto.
- `audio.asm` agrega headers, SFX, musicas e engines de audio.
- `ram.asm` inclui os mapas de memoria em `ram/vram.asm`, `ram/wram.asm`,
  `ram/sram.asm` e `ram/hram.asm`.

Diretorios principais:

- `home/`: rotinas sempre acessiveis em `ROM0`.
- `engine/`: logica de jogo por area funcional.
- `data/`: tabelas e estruturas de dados do jogo.
- `scripts/`: scripts de mapas/eventos.
- `maps/`: blocos binarios de mapas (`.blk`).
- `text/`: textos por localidade/feature.
- `constants/`: ids, flags, layouts e nomes compartilhados.
- `macros/`: macros RGBDS e DSLs de dados/scripts.
- `ram/`: layout de memoria nomeado; trate como contrato.
- `audio/`: engine, musicas, SFX e headers de audio.
- `gfx/`: assets graficos fonte e gerados.
- `tools/`: utilitarios C usados pelo build.
- `vc/`: constantes e templates de patches Virtual Console.

## Contexto Por Grafos Com Graphify

Use Graphify como mapa vivo do projeto. A intencao e que agentes consigam
entender relacoes entre labels, arquivos, bancos, dados, macros e notas de
reescrita por grafo, nao apenas por busca textual.

Nota especifica deste repo: o Graphify padrao nao classifica `.asm` como codigo.
Por isso, use `tools/graphify_rgbds.py`, que gera uma extracao RGBDS
deterministica e depois usa o pipeline de build/cluster/report/wiki do Graphify.

Regras obrigatorias:

- Antes de responder perguntas de arquitetura, fluxo de codigo, dependencias,
  "quem chama quem", impacto de mudanca ou planejamento de migracao para C,
  verifique se `graphify-out/graph.json` existe.
- Se o grafo existir, consulte-o primeiro com `graphify query "<pergunta>"`,
  `graphify path "<origem>" "<destino>"` ou `graphify explain "<no>"`.
- Se o grafo nao existir e a tarefa exigir contexto amplo, gere o grafo com
  `$(cat graphify-out/.graphify_python) tools/graphify_rgbds.py .` antes de
  propor arquitetura.
- Depois de alteracoes relevantes em `.asm`, `.inc`, `Makefile`, `tools/`,
  `docs/rewrite/`, `AGENTS.md` ou `CLAUDE.md`, atualize com
  `$(cat graphify-out/.graphify_python) tools/graphify_rgbds.py .`.
- Se a atualizacao nao puder ser rodada por falta de ferramenta, tempo ou
  dependencia local, registre isso no fechamento da tarefa.
- Nao invente relacoes: ao usar o grafo, diferencie fatos extraidos de
  inferencias e cite arquivos/labels quando possivel.

Artefatos esperados:

- `graphify-out/graph.json`: grafo bruto usado por consultas.
- `graphify-out/GRAPH_REPORT.md`: relatorio de comunidades, god nodes e
  perguntas sugeridas.
- `graphify-out/graph.html`: visualizacao interativa quando gerada.
- `graphify-out/wiki/` ou export equivalente: material navegavel por agentes
  quando `--wiki` for usado.

O grafo e auxiliar de entendimento, nao substitui testes, leitura de assembly
ou validacao de ROM. Use-o para orientar a exploracao e depois confirme o
comportamento nos arquivos fonte e no build.

## Como Estudar Um Comportamento

1. Comece por uma feature visivel: batalha, menu, mapa, item, texto, audio,
   save, link, NPC ou script.
2. Use `rg` para encontrar labels, constantes e textos relacionados.
3. Identifique por qual agregador o arquivo entra no build:
   `home.asm`, `main.asm`, `maps.asm`, `text.asm`, `audio.asm` ou `ram.asm`.
4. Consulte `layout.link` para saber banco/secao e possiveis restricoes.
5. Siga chamadas, tabelas, macros, `farcall`, `predef`, bancos e RAM tocada.
6. Leia os labels `w*`, `h*`, `s*` e `v*` em `ram/` antes de renomear estado.
7. Registre entradas, saidas, flags, registros, memoria alterada, RNG, input,
   efeitos de video/audio e dependencias de banco.
8. So depois escreva C ou altere assembly.

Ao criar notas de estudo, prefira arquivos pequenos em `docs/rewrite/` com:

- feature estudada;
- arquivos `.asm` fonte;
- labels de entrada;
- RAM/HRAM/SRAM/VRAM tocada;
- dados/tabelas envolvidos;
- comportamento esperado;
- casos de teste planejados;
- riscos de compatibilidade.

## Estrategia Para Reescrever Em C

Use uma camada C paralela antes de substituir comportamento real da ROM. O
assembly deve continuar compilando enquanto o C amadurece por testes.

O marco atual de batalha e deliberadamente pre-C. Enquanto
`rewrite/battle/tests/test_c_rewrite_gate.py` existir, nao adicione `.c` ou `.h`
em `rewrite/`. Revise primeiro `rewrite/battle/contracts/traceability.json`, os
casos ASM e os riscos isolados; a liberacao do gate deve ser uma decisao humana
registrada em commit proprio.

Fluxo recomendado:

1. Caracterize o comportamento do assembly com exemplos concretos.
2. Modele os dados em C com tamanhos explicitos: `uint8_t`, `uint16_t`, enums
   com valores fixos e structs documentando layout.
3. Escreva testes contra o comportamento observado.
4. Traduza uma rotina pequena ou uma tabela por vez.
5. Compare saida, estado de memoria, flags relevantes e efeitos colaterais.
6. Refatore o C sob teste para clareza e baixo acoplamento.
7. Integre somente quando a fatia estiver coberta.

Contextos de dominio candidatos:

- Hardware/Runtime: memoria, bancos, interrupcoes, joypad, RNG, timers, OAM,
  VRAM, SRAM e registradores Game Boy.
- Overworld/Map: carregamento de mapa, tiles, colisao, warps, sprites, NPCs e
  scripts.
- Battle: estado de batalha, turnos, movimentos, efeitos, AI, dano, status,
  experiencia e captura.
- Pokemon/Party/Box: especies, stats, moves, evolucao, party, boxes e storage.
- Items/Inventory: bag, marts, TMs/HMs, dinheiro, precos e efeitos de item.
- Menu/Text: listas, caixas de texto, input, charmap, impressao e nomes.
- Audio: canais, SFX, musicas, tempo, vibrato e comandos de audio.
- Save/Link: SRAM, checksums, serial/link cable e compatibilidade de dados.

Em C, prefira modulos com headers pequenos e dependencia explicita. Evite
hierarquias artificiais: este projeto pede baixo acoplamento, estado claro e
testabilidade, nao OO por obrigacao.

## Testes E Validacao

- Para mudancas em assembly, rode pelo menos o alvo afetado; para mudancas que
  podem afetar layout ou comportamento global, rode `make DEBUG=1 compare`.
- Para C novo, crie testes antes ou junto da implementacao. Se ainda nao houver
  harness C, adicione o menor harness possivel para a fatia em questao.
- Use golden masters quando apropriado: hashes de ROM, dumps de tabelas, traces
  de memoria, fixtures de estado e saidas deterministicas.
- Controle fontes nao deterministicas em testes: RNG, input, tempo, VBlank,
  audio e ordem de eventos.
- Nao aprove uma migracao para C apenas porque "parece equivalente"; exija
  evidencia executavel.

## Regras Ao Editar

- Use `rg`/`rg --files` para explorar o repositorio.
- Nao altere ordem de `SECTION`, `INCLUDE`, `INCBIN` ou dados binarios sem
  entender impacto em banco, endereco e hash.
- Nao faca formatacao ampla em `.asm`; preserve estilo local.
- Nao versione artefatos gerados ignorados por `.gitignore`: objetos, ROMs,
  graficos compilados, patches, `.map` e `.sym`.
- Se tocar `tools/`, valide com `make tools` e depois com o alvo que usa a
  ferramenta.
- Se tocar macros ou constantes, trate como mudanca de superficie ampla.
- Quando houver alteracoes de usuario no worktree, preserve-as e trabalhe ao
  redor delas.
- Mantenha o grafo Graphify atualizado apos mudancas relevantes, ou registre
  explicitamente por que isso nao foi feito.

## Definition Of Done

Uma fatia esta pronta quando:

- o comportamento estudado esta documentado o suficiente para outra pessoa
  seguir a trilha;
- testes de caracterizacao ou unitarios cobrem a decisao tomada;
- o build relevante passa;
- `make DEBUG=1 compare` foi rodado quando layout, assembly ou comportamento
  global foram afetados;
- Graphify foi consultado para contexto amplo e atualizado quando a mudanca
  altera relacoes relevantes do projeto;
- os nomes em C refletem a linguagem do jogo e os labels originais importantes;
- nao ha refactor amplo sem necessidade para a fatia.
