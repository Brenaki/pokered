# Informações sobre os Pokémon de Pokémon Red/Blue

## Controle do documento

| Campo | Valor |
|---|---|
| Identificação | PKM-002 |
| Arquivo | `002-2026-08-01-Informações_sobre_Pokemons.md` |
| Revisão | 1.0 |
| Data de emissão | 2026-08-01 |
| Situação | Emitido para revisão e uso técnico interno |
| Responsável pelo processo | Equipe de reescrita ASM para C |
| Elaborado por | Gerador determinístico e verificação do código-fonte |
| Aprovador | Pendente de designação |
| Baseline do código | commit `9c8d8f44e5c5850414ea3e8bdb5795f78bcb7db5` |
| Abrangência | 151 espécies válidas da Pokédex de Pokémon Red/Blue |
| Classificação | Informação documentada interna |

### Histórico de revisões

| Revisão | Data | Alteração | Autor | Aprovação |
|---|---|---|---|---|
| 1.0 | 2026-08-01 | Emissão inicial do catálogo completo de espécies | Codex | Pendente |

## 1. Finalidade e relação com a ISO 9001

Este documento controla e torna rastreável o conhecimento sobre as espécies
implementadas nesta ROM. Ele serve como fonte para análise do legado, contrato de
compatibilidade da reescrita em C, entrada de testes e evidência de revisão.

A organização adota abordagem de processo, pensamento baseado em risco, critérios
de aceitação, rastreabilidade e controle de informação documentada inspirados na
ISO 9001. Isso **não** declara certificação nem conformidade formal do software ou
do repositório com a norma.

Na data de emissão, a referência publicada é a
[ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html). A sexta edição
está em publicação, com [previsão da ISO para setembro de 2026](https://www.iso.org/standard/88464.html).
O controle aplicado também considera a orientação oficial sobre
[informação documentada](https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/documented_information.pdf).

## 2. Escopo

### 2.1 Incluído

- as 151 espécies numeradas por `DEX_BULBASAUR` a `DEX_MEW`;
- nome, categoria, descrição da Pokédex, altura, peso, tipos, catch rate, EXP base e crescimento;
- atributos base e resultados calculados nos níveis 0 e 99;
- movimentos iniciais, movimentos por nível e compatibilidade TM/HM;
- evolução direta, origem evolutiva e pré-requisitos;
- encontros terrestres, em cavernas, por Surf, por pesca e estáticos;
- diferenças de disponibilidade entre Red e Blue;
- presentes, escolhas, fósseis, prêmios e trocas com NPC;
- controles, riscos e testes necessários para a migração gradual para C.

### 2.2 Excluído

- índices `MISSINGNO.`, fósseis de exibição e o `RESTLESS_SOUL`;
- equipes de treinadores, sprites, paletas e cries;
- mecânicas inexistentes na Geração I, como abilities, natures, breeding, egg moves,
  gênero mecânico e itens segurados;
- dados de Pokémon Yellow ou gerações posteriores.

## 3. Objetivos e critérios da qualidade

| ID | Objetivo | Critério verificável |
|---|---|---|
| PKM-Q01 | Cobertura integral | Exatamente 151 espécies válidas, sem `MISSINGNO.`. |
| PKM-Q02 | Fidelidade | Todo dado transcrito aponta para uma tabela ASM canônica. |
| PKM-Q03 | Reprodutibilidade | O gerador produz o mesmo conteúdo para o mesmo commit. |
| PKM-Q04 | Correção numérica | Fórmulas usam inteiros, pisos e limites iguais aos da ROM. |
| PKM-Q05 | Distinção de versão | Encontros e prêmios Red/Blue não são fundidos indevidamente. |
| PKM-Q06 | Manutenção | Alterações nas fontes exigem regeneração, testes e Graphify. |

## 4. Fontes de verdade

| Responsabilidade | Fonte |
|---|---|
| Ordem nacional e IDs | `constants/pokedex_constants.asm` |
| Atributos, tipos, captura, EXP, golpes iniciais, crescimento e TM/HM | `data/pokemon/base_stats.asm`, `data/pokemon/base_stats/*.asm`, `data/pokemon/mew.asm` |
| Altura, peso e categoria | `data/pokemon/dex_entries.asm` |
| Descrição textual da Pokédex | `data/pokemon/dex_text.asm` |
| Evoluções e golpes por nível | `data/pokemon/evos_moves.asm` |
| Nomes de golpes | `constants/move_constants.asm`, `data/moves/names.asm` |
| Numeração TM/HM | `constants/item_constants.asm`, `data/moves/tmhm_moves.asm` |
| Encontros terrestres e Surf | `data/wild/grass_water.asm`, `data/wild/maps/*.asm` |
| Probabilidade dos dez slots | `data/wild/probabilities.asm` |
| Pesca | `engine/items/item_effects.asm`, `data/wild/good_rod.asm`, `data/wild/super_rod.asm` |
| Encontros estáticos | `data/maps/objects/*.asm`, `scripts/Route12.asm`, `scripts/Route16.asm` |
| Presentes, fósseis, prêmios e trocas | `scripts/OaksLab.asm`, `scripts/CeladonMansionRoofHouse.asm`, `scripts/SilphCo7F.asm`, `scripts/FightingDojo.asm`, `scripts/MtMoonPokecenter.asm`, `scripts/CinnabarLabFossilRoom.asm`, `data/events/prizes.asm`, `data/events/prize_mon_levels.asm`, `data/events/trades.asm` |
| Cálculo de atributos | `home/move_mon.asm` (`CalcStats`, `CalcStat`) |
| Evolução em execução | `engine/pokemon/evos_moves.asm` (`TryEvolvingMon`) |
| Captura | `engine/items/item_effects.asm` (`ItemUseBall`) |

## 5. Convenções e regras de interpretação

As descrições da Pokédex permanecem em inglês, como armazenadas na ROM. O gerador
une as linhas `text`/`next`/`page`, recompõe palavras hifenizadas apenas pela quebra
de tela e expande o token de fonte `#` para "Poké".

### 5.1 Atributos

A Geração I possui cinco atributos armazenados: HP, Attack, Defense, Speed e Special.
Não há Special Attack e Special Defense separados. `BST` neste documento é a soma
dos cinco atributos base.

Os atributos reais dependem do nível, DV e Stat Exp. Para tornar os valores de
nível 99 verificáveis, cada célula apresenta a faixa **mínimo-máximo**:

```text
Min: DV=0 e Stat Exp=0
Max: DV=15 e Stat Exp=65535; floor(ceil(sqrt(65535))/4)=63
Não HP = floor(((2*(Base+DV)+BonusStatExp)*Nivel)/100)+5
HP     = floor(((2*(Base+DV)+BonusStatExp)*Nivel)/100)+Nivel+10
Resultado final limitado a 999
```

Nível 0 não é um nível normal de progressão (`MAX_LEVEL` é 100). Ele é incluído
porque foi solicitado e representa a saída técnica da fórmula: HP=10 e os demais
atributos=5 para toda espécie, independentemente de DV e Stat Exp. O catálogo usa
nível 99, não 100, no segundo cenário.

### 5.2 Captura e classificação

`Catch rate` é o byte base da espécie. A chance efetiva também depende da Ball, HP
atual/máximo, status e RNG. Para comparar espécies, a coluna de dificuldade usa um
cenário normalizado: Poké Ball, sem status, HP=MaxHP=100. Nesse cenário, `W=85`,
o segundo teste passa em `86/256` e:

```text
P = ((CatchRate + 1) / 256) * (86 / 256)
```

O primeiro fator é limitado a 256 resultados. As classes são critérios internos
deste documento: muito difícil <4%; difícil <10%; intermediária <20%; favorável
<30%; muito favorável >=30%. Para o algoritmo completo, usar
`docs/001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md`.

### 5.3 Movimentos

- **Iniciais:** até quatro bytes `BASE_MOVES`, descritos no fonte como learnset de nível 1.
- **Por nível:** pares ordenados em `data/pokemon/evos_moves.asm`.
- **TM/HM:** bits de compatibilidade; a ficha mostra número do item e nome do golpe.
- Pokémon recebidos ou encontrados acima do nível 1 são montados pelo motor a partir
  dessas tabelas e mantêm no máximo quatro movimentos.
- Evolução preserva os golpes atuais. A nova espécie passa a usar seu próprio learnset
  para níveis posteriores; não existe Move Reminder nesta ROM.

### 5.4 Encontros

Cada tabela terrestre/Surf tem um limiar de encontro e dez slots condicionais com
pesos exatos `51, 51, 39, 25, 25, 25, 13, 13, 11, 3`, totalizando 256. A ficha
agrega slots repetidos por espécie e nível. O percentual entre parênteses é a chance
**condicional após ocorrer um encontro**; o limiar `N/256` é testado separadamente.

Good Rod tem 50% de não fisgar e, quando fisga, escolhe Goldeen ou Poliwag igualmente:
25% por uso para cada. Super Rod tem 50% de não fisgar e escolha uniforme dentro do
grupo do mapa. Old Rod sempre produz Magikarp Nv.5 quando a pesca é permitida.

### 5.5 Evolução e obtenção

`EVOLVE_LEVEL` exige nível atual igual ou maior que o limiar durante a avaliação
pós-batalha; `EVOLVE_ITEM` exige a pedra indicada e nível mínimo 1; `EVOLVE_TRADE`
exige troca por link e nível mínimo 1. A rotina original contém o bug documentado
em que encontros selvagens podem acionar evolução por pedra devido ao reuso de
`wCurItem`; a reescrita deve preservá-lo somente em modo de compatibilidade.

Trocas com NPC recebem o Pokémon no mesmo nível daquele entregue. Escolhas são
mutuamente exclusivas quando indicado. Mew possui dados completos, mas não possui
método normal de obtenção nesta ROM.

## 6. Resumo de cobertura

| Medida | Resultado |
|---|---:|
| Espécies válidas | 151 |
| Movimentos nomeados | 165 |
| Compatibilidades TM/HM possíveis | 55 itens |
| Entradas diretas de evolução | 72 |
| Espécies com evolução direta | 70 |
| Espécies com algum encontro capturável em Red | 91 |
| Espécies com algum encontro capturável em Blue | 91 |

## 7. Catálogo controlado das 151 espécies

As fichas seguem a ordem nacional. `Nenhum encontro` significa ausência nas tabelas
aleatórias, pesca e encontros estáticos capturáveis; a espécie ainda pode ser obtida
por evolução, presente, prêmio ou troca conforme as linhas seguintes.

### 001 Bulbasaur

| Campo | Valor |
|---|---|
| Nome/espécie | Bulbasaur (`DEX_BULBASAUR`) |
| Categoria Pokédex | Seed |
| Descrição Pokédex | A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon |
| Altura | 2'04" (0,71 m) |
| Peso | 15,0 lb (6,8 kg) |
| Tipo | Grass / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 64 / Medium Slow |
| Atributos base | HP 45; Atk 49; Def 49; Spd 45; Spc 65; BST 253 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 102-194; Def 102-194; Spd 94-186; Spc 133-225 |
| Movimentos iniciais | Tackle, Growl |
| Movimentos aprendidos por nível | Nv.7 Leech Seed; Nv.13 Vine Whip; Nv.20 Poisonpowder; Nv.27 Razor Leaf; Nv.34 Growth; Nv.41 Sleep Powder; Nv.48 Solarbeam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Ivysaur ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Aquisição especial em Blue | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Fonte específica | `data/pokemon/base_stats/bulbasaur.asm` |

### 002 Ivysaur

| Campo | Valor |
|---|---|
| Nome/espécie | Ivysaur (`DEX_IVYSAUR`) |
| Categoria Pokédex | Seed |
| Descrição Pokédex | When the bulb on its back grows large, it appears to lose the ability to stand on its hind legs |
| Altura | 3'03" (0,99 m) |
| Peso | 29,0 lb (13,2 kg) |
| Tipo | Grass / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 141 / Medium Slow |
| Atributos base | HP 60; Atk 62; Def 63; Spd 60; Spc 80; BST 325 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 127-219; Def 129-221; Spd 123-215; Spc 163-255 |
| Movimentos iniciais | Tackle, Growl, Leech Seed |
| Movimentos aprendidos por nível | Nv.7 Leech Seed; Nv.13 Vine Whip; Nv.22 Poisonpowder; Nv.30 Razor Leaf; Nv.38 Growth; Nv.46 Sleep Powder; Nv.54 Solarbeam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Venusaur ao atingir Nv.32 ou superior após ganho de nível |
| Origem por evolução | Bulbasaur: Ivysaur ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/ivysaur.asm` |

### 003 Venusaur

| Campo | Valor |
|---|---|
| Nome/espécie | Venusaur (`DEX_VENUSAUR`) |
| Categoria Pokédex | Seed |
| Descrição Pokédex | The plant blooms when it is absorbing solar energy. It stays on the move to seek sunlight |
| Altura | 6'07" (2,01 m) |
| Peso | 221,0 lb (100,2 kg) |
| Tipo | Grass / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 208 / Medium Slow |
| Atributos base | HP 80; Atk 82; Def 83; Spd 80; Spc 100; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 167-259; Def 169-261; Spd 163-255; Spc 203-295 |
| Movimentos iniciais | Tackle, Growl, Leech Seed, Vine Whip |
| Movimentos aprendidos por nível | Nv.7 Leech Seed; Nv.13 Vine Whip; Nv.22 Poisonpowder; Nv.30 Razor Leaf; Nv.43 Growth; Nv.55 Sleep Powder; Nv.65 Solarbeam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Ivysaur: Venusaur ao atingir Nv.32 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/venusaur.asm` |

### 004 Charmander

| Campo | Valor |
|---|---|
| Nome/espécie | Charmander (`DEX_CHARMANDER`) |
| Categoria Pokédex | Lizard |
| Descrição Pokédex | Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail |
| Altura | 2'00" (0,61 m) |
| Peso | 19,0 lb (8,6 kg) |
| Tipo | Fire |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 65 / Medium Slow |
| Atributos base | HP 39; Atk 52; Def 43; Spd 65; Spc 50; BST 249 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 186-278; Atk 107-200; Def 90-182; Spd 133-225; Spc 104-196 |
| Movimentos iniciais | Scratch, Growl |
| Movimentos aprendidos por nível | Nv.9 Ember; Nv.15 Leer; Nv.22 Rage; Nv.30 Slash; Nv.38 Flamethrower; Nv.46 Fire Spin |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM01 Mega Punch; TM03 Swords Dance; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM23 Dragon Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Charmeleon ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Aquisição especial em Blue | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Fonte específica | `data/pokemon/base_stats/charmander.asm` |

### 005 Charmeleon

| Campo | Valor |
|---|---|
| Nome/espécie | Charmeleon (`DEX_CHARMELEON`) |
| Categoria Pokédex | Flame |
| Descrição Pokédex | When it swings its burning tail, it elevates the temperature to unbearably high levels |
| Altura | 3'07" (1,09 m) |
| Peso | 42,0 lb (19,1 kg) |
| Tipo | Fire |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 142 / Medium Slow |
| Atributos base | HP 58; Atk 64; Def 58; Spd 80; Spc 65; BST 325 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 223-315; Atk 131-223; Def 119-211; Spd 163-255; Spc 133-225 |
| Movimentos iniciais | Scratch, Growl, Ember |
| Movimentos aprendidos por nível | Nv.9 Ember; Nv.15 Leer; Nv.24 Rage; Nv.33 Slash; Nv.42 Flamethrower; Nv.56 Fire Spin |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM01 Mega Punch; TM03 Swords Dance; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM23 Dragon Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Charizard ao atingir Nv.36 ou superior após ganho de nível |
| Origem por evolução | Charmander: Charmeleon ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/charmeleon.asm` |

### 006 Charizard

| Campo | Valor |
|---|---|
| Nome/espécie | Charizard (`DEX_CHARIZARD`) |
| Categoria Pokédex | Flame |
| Descrição Pokédex | Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally |
| Altura | 5'07" (1,70 m) |
| Peso | 200,0 lb (90,7 kg) |
| Tipo | Fire / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 209 / Medium Slow |
| Atributos base | HP 78; Atk 84; Def 78; Spd 100; Spc 85; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 263-355; Atk 171-263; Def 159-251; Spd 203-295; Spc 173-265 |
| Movimentos iniciais | Scratch, Growl, Ember, Leer |
| Movimentos aprendidos por nível | Nv.9 Ember; Nv.15 Leer; Nv.24 Rage; Nv.36 Slash; Nv.46 Flamethrower; Nv.55 Fire Spin |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM01 Mega Punch; TM03 Swords Dance; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM23 Dragon Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Charmeleon: Charizard ao atingir Nv.36 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/charizard.asm` |

### 007 Squirtle

| Campo | Valor |
|---|---|
| Nome/espécie | Squirtle (`DEX_SQUIRTLE`) |
| Categoria Pokédex | Tinyturtle |
| Descrição Pokédex | After birth, its back swells and hardens into a shell. Powerfully sprays foam from its mouth |
| Altura | 1'08" (0,51 m) |
| Peso | 20,0 lb (9,1 kg) |
| Tipo | Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 66 / Medium Slow |
| Atributos base | HP 44; Atk 48; Def 65; Spd 43; Spc 50; BST 250 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 196-288; Atk 100-192; Def 133-225; Spd 90-182; Spc 104-196 |
| Movimentos iniciais | Tackle, Tail Whip |
| Movimentos aprendidos por nível | Nv.8 Bubble; Nv.15 Water Gun; Nv.22 Bite; Nv.28 Withdraw; Nv.35 Skull Bash; Nv.42 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Wartortle ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Aquisição especial em Blue | Inicial no Oak's Lab, Nv.5; escolher apenas um dos três |
| Fonte específica | `data/pokemon/base_stats/squirtle.asm` |

### 008 Wartortle

| Campo | Valor |
|---|---|
| Nome/espécie | Wartortle (`DEX_WARTORTLE`) |
| Categoria Pokédex | Turtle |
| Descrição Pokédex | Often hides in water to stalk unwary prey. For swimming fast, it moves its ears to maintain balance |
| Altura | 3'03" (0,99 m) |
| Peso | 50,0 lb (22,7 kg) |
| Tipo | Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 143 / Medium Slow |
| Atributos base | HP 59; Atk 63; Def 80; Spd 58; Spc 65; BST 325 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 225-317; Atk 129-221; Def 163-255; Spd 119-211; Spc 133-225 |
| Movimentos iniciais | Tackle, Tail Whip, Bubble |
| Movimentos aprendidos por nível | Nv.8 Bubble; Nv.15 Water Gun; Nv.24 Bite; Nv.31 Withdraw; Nv.39 Skull Bash; Nv.47 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Blastoise ao atingir Nv.36 ou superior após ganho de nível |
| Origem por evolução | Squirtle: Wartortle ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/wartortle.asm` |

### 009 Blastoise

| Campo | Valor |
|---|---|
| Nome/espécie | Blastoise (`DEX_BLASTOISE`) |
| Categoria Pokédex | Shellfish |
| Descrição Pokédex | A brutal Pokémon with pressurized water jets on its shell. They are used for high speed tackles |
| Altura | 5'03" (1,60 m) |
| Peso | 189,0 lb (85,7 kg) |
| Tipo | Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 210 / Medium Slow |
| Atributos base | HP 79; Atk 83; Def 100; Spd 78; Spc 85; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 265-357; Atk 169-261; Def 203-295; Spd 159-251; Spc 173-265 |
| Movimentos iniciais | Tackle, Tail Whip, Bubble, Water Gun |
| Movimentos aprendidos por nível | Nv.8 Bubble; Nv.15 Water Gun; Nv.24 Bite; Nv.31 Withdraw; Nv.42 Skull Bash; Nv.52 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Wartortle: Blastoise ao atingir Nv.36 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/blastoise.asm` |

### 010 Caterpie

| Campo | Valor |
|---|---|
| Nome/espécie | Caterpie (`DEX_CATERPIE`) |
| Categoria Pokédex | Worm |
| Descrição Pokédex | Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls |
| Altura | 1'00" (0,30 m) |
| Peso | 6,0 lb (2,7 kg) |
| Tipo | Bug |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 53 / Medium Fast |
| Atributos base | HP 45; Atk 30; Def 35; Spd 45; Spc 20; BST 175 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 64-156; Def 74-166; Spd 94-186; Spc 44-136 |
| Movimentos iniciais | Tackle, String Shot |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Metapod ao atingir Nv.7 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 25 - terrestre/caverna, limiar 15/256: Nv.8 (1,2%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (5,1%) |
| Spawns em Blue | Route 2 - terrestre/caverna, limiar 25/256: Nv.3 (9,8%), Nv.4 (4,3%), Nv.5 (1,2%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.7 (19,9%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.8 (19,9%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (15,2%), Nv.4 (19,9%), Nv.5 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/caterpie.asm` |

### 011 Metapod

| Campo | Valor |
|---|---|
| Nome/espécie | Metapod (`DEX_METAPOD`) |
| Categoria Pokédex | Cocoon |
| Descrição Pokédex | This Pokémon is vulnerable to attack while its shell is soft, exposing its weak and tender body |
| Altura | 2'04" (0,71 m) |
| Peso | 22,0 lb (10,0 kg) |
| Tipo | Bug |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 72 / Medium Fast |
| Atributos base | HP 50; Atk 20; Def 55; Spd 30; Spc 25; BST 180 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 44-136; Def 113-205; Spd 64-156; Spc 54-146 |
| Movimentos iniciais | Harden |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Butterfree ao atingir Nv.10 ou superior após ganho de nível |
| Origem por evolução | Caterpie: Metapod ao atingir Nv.7 ou superior após ganho de nível |
| Spawns em Red | Route 25 - terrestre/caverna, limiar 15/256: Nv.7 (4,3%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.4 (5,1%) |
| Spawns em Blue | Route 24 - terrestre/caverna, limiar 25/256: Nv.8 (19,9%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.9 (19,9%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.4 (9,8%), Nv.5 (19,9%), Nv.6 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/metapod.asm` |

### 012 Butterfree

| Campo | Valor |
|---|---|
| Nome/espécie | Butterfree (`DEX_BUTTERFREE`) |
| Categoria Pokédex | Butterfly |
| Descrição Pokédex | In battle, it flaps its wings at high speed to release highly toxic dust into the air |
| Altura | 3'07" (1,09 m) |
| Peso | 71,0 lb (32,2 kg) |
| Tipo | Bug / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 160 / Medium Fast |
| Atributos base | HP 60; Atk 45; Def 50; Spd 70; Spc 80; BST 305 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 94-186; Def 104-196; Spd 143-235; Spc 163-255 |
| Movimentos iniciais | Confusion |
| Movimentos aprendidos por nível | Nv.12 Confusion; Nv.15 Poisonpowder; Nv.16 Stun Spore; Nv.17 Sleep Powder; Nv.21 Supersonic; Nv.26 Whirlwind; Nv.32 Psybeam |
| Movimentos possíveis por TM/HM | TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Metapod: Butterfree ao atingir Nv.10 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/butterfree.asm` |

### 013 Weedle

| Campo | Valor |
|---|---|
| Nome/espécie | Weedle (`DEX_WEEDLE`) |
| Categoria Pokédex | Hairy Bug |
| Descrição Pokédex | Often found in forests, eating leaves. It has a sharp venomous stinger on its head |
| Altura | 1'00" (0,30 m) |
| Peso | 7,0 lb (3,2 kg) |
| Tipo | Bug / Poison |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 52 / Medium Fast |
| Atributos base | HP 40; Atk 35; Def 30; Spd 50; Spc 20; BST 175 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 74-166; Def 64-156; Spd 104-196; Spc 44-136 |
| Movimentos iniciais | Poison Sting, String Shot |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Kakuna ao atingir Nv.7 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 2 - terrestre/caverna, limiar 25/256: Nv.3 (9,8%), Nv.4 (4,3%), Nv.5 (1,2%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.7 (19,9%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.8 (19,9%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (15,2%), Nv.4 (19,9%), Nv.5 (9,8%) |
| Spawns em Blue | Route 25 - terrestre/caverna, limiar 15/256: Nv.8 (1,2%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/weedle.asm` |

### 014 Kakuna

| Campo | Valor |
|---|---|
| Nome/espécie | Kakuna (`DEX_KAKUNA`) |
| Categoria Pokédex | Cocoon |
| Descrição Pokédex | Almost incapable of moving, this Pokémon can only harden its shell to protect itself from predators |
| Altura | 2'00" (0,61 m) |
| Peso | 22,0 lb (10,0 kg) |
| Tipo | Bug / Poison |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 71 / Medium Fast |
| Atributos base | HP 45; Atk 25; Def 50; Spd 35; Spc 25; BST 180 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 54-146; Def 104-196; Spd 74-166; Spc 54-146 |
| Movimentos iniciais | Harden |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Beedrill ao atingir Nv.10 ou superior após ganho de nível |
| Origem por evolução | Weedle: Kakuna ao atingir Nv.7 ou superior após ganho de nível |
| Spawns em Red | Route 24 - terrestre/caverna, limiar 25/256: Nv.8 (19,9%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.9 (19,9%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.4 (9,8%), Nv.5 (19,9%), Nv.6 (9,8%) |
| Spawns em Blue | Route 25 - terrestre/caverna, limiar 15/256: Nv.7 (4,3%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.4 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/kakuna.asm` |

### 015 Beedrill

| Campo | Valor |
|---|---|
| Nome/espécie | Beedrill (`DEX_BEEDRILL`) |
| Categoria Pokédex | Poison Bee |
| Descrição Pokédex | Flies at high speed and attacks using its large venomous stingers on its forelegs and tail |
| Altura | 3'03" (0,99 m) |
| Peso | 65,0 lb (29,5 kg) |
| Tipo | Bug / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 159 / Medium Fast |
| Atributos base | HP 65; Atk 80; Def 40; Spd 75; Spc 45; BST 305 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 163-255; Def 84-176; Spd 153-245; Spc 94-186 |
| Movimentos iniciais | Fury Attack |
| Movimentos aprendidos por nível | Nv.12 Fury Attack; Nv.16 Focus Energy; Nv.20 Twineedle; Nv.25 Rage; Nv.30 Pin Missile; Nv.35 Agility |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Kakuna: Beedrill ao atingir Nv.10 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/beedrill.asm` |

### 016 Pidgey

| Campo | Valor |
|---|---|
| Nome/espécie | Pidgey (`DEX_PIDGEY`) |
| Categoria Pokédex | Tiny Bird |
| Descrição Pokédex | A common sight in forests and woods. It flaps its wings at ground level to kick up blinding sand |
| Altura | 1'00" (0,30 m) |
| Peso | 4,0 lb (1,8 kg) |
| Tipo | Normal / Flying |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 55 / Medium Slow |
| Atributos base | HP 40; Atk 45; Def 40; Spd 56; Spc 35; BST 216 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 94-186; Def 84-176; Spd 115-207; Spc 74-166 |
| Movimentos iniciais | Gust |
| Movimentos aprendidos por nível | Nv.5 Sand-Attack; Nv.12 Quick Attack; Nv.19 Whirlwind; Nv.28 Wing Attack; Nv.36 Agility; Nv.44 Mirror Move |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Pidgeotto ao atingir Nv.18 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 1 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (34,8%), Nv.4 (4,3%), Nv.5 (1,2%)<br>Route 12 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%), Nv.25 (19,9%), Nv.27 (5,1%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.25 (19,9%), Nv.27 (15,2%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%)<br>Route 2 - terrestre/caverna, limiar 25/256: Nv.3 (19,9%), Nv.4 (15,2%), Nv.5 (9,8%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.21 (9,8%), Nv.23 (19,9%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.12 (15,2%), Nv.13 (5,1%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.13 (15,2%)<br>Route 3 - terrestre/caverna, limiar 20/256: Nv.6 (19,9%), Nv.7 (15,2%), Nv.8 (9,8%)<br>Route 5 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (15,2%), Nv.16 (5,1%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (15,2%), Nv.16 (5,1%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.19 (19,9%), Nv.22 (9,8%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.18 (19,9%), Nv.20 (9,8%) |
| Spawns em Blue | Route 1 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (34,8%), Nv.4 (4,3%), Nv.5 (1,2%)<br>Route 12 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%), Nv.25 (19,9%), Nv.27 (5,1%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.25 (19,9%), Nv.27 (15,2%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%)<br>Route 2 - terrestre/caverna, limiar 25/256: Nv.3 (19,9%), Nv.4 (15,2%), Nv.5 (9,8%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.21 (9,8%), Nv.23 (19,9%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.12 (15,2%), Nv.13 (5,1%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.13 (15,2%)<br>Route 3 - terrestre/caverna, limiar 20/256: Nv.6 (19,9%), Nv.7 (15,2%), Nv.8 (9,8%)<br>Route 5 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (15,2%), Nv.16 (5,1%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (15,2%), Nv.16 (5,1%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.19 (19,9%), Nv.22 (9,8%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.18 (19,9%), Nv.20 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/pidgey.asm` |

### 017 Pidgeotto

| Campo | Valor |
|---|---|
| Nome/espécie | Pidgeotto (`DEX_PIDGEOTTO`) |
| Categoria Pokédex | Bird |
| Descrição Pokédex | Very protective of its sprawling territorial area, this Pokémon will fiercely peck at any intruder |
| Altura | 3'07" (1,09 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Normal / Flying |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 113 / Medium Slow |
| Atributos base | HP 63; Atk 60; Def 55; Spd 71; Spc 50; BST 299 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 233-325; Atk 123-215; Def 113-205; Spd 145-237; Spc 104-196 |
| Movimentos iniciais | Gust, Sand-Attack |
| Movimentos aprendidos por nível | Nv.5 Sand-Attack; Nv.12 Quick Attack; Nv.21 Whirlwind; Nv.31 Wing Attack; Nv.40 Agility; Nv.49 Mirror Move |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Pidgeot ao atingir Nv.36 ou superior após ganho de nível |
| Origem por evolução | Pidgey: Pidgeotto ao atingir Nv.18 ou superior após ganho de nível |
| Spawns em Red | Route 14 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.30 (9,8%), Nv.32 (5,1%) |
| Spawns em Blue | Route 14 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.30 (9,8%), Nv.32 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/pidgeotto.asm` |

### 018 Pidgeot

| Campo | Valor |
|---|---|
| Nome/espécie | Pidgeot (`DEX_PIDGEOT`) |
| Categoria Pokédex | Bird |
| Descrição Pokédex | When hunting, it skims the surface of water at high speed to pick off unwary prey such as MAGIKARP |
| Altura | 4'11" (1,50 m) |
| Peso | 87,0 lb (39,5 kg) |
| Tipo | Normal / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 172 / Medium Slow |
| Atributos base | HP 83; Atk 80; Def 75; Spd 91; Spc 70; BST 399 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 273-365; Atk 163-255; Def 153-245; Spd 185-277; Spc 143-235 |
| Movimentos iniciais | Gust, Sand-Attack, Quick Attack |
| Movimentos aprendidos por nível | Nv.5 Sand-Attack; Nv.12 Quick Attack; Nv.21 Whirlwind; Nv.31 Wing Attack; Nv.44 Agility; Nv.54 Mirror Move |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Pidgeotto: Pidgeot ao atingir Nv.36 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/pidgeot.asm` |

### 019 Rattata

| Campo | Valor |
|---|---|
| Nome/espécie | Rattata (`DEX_RATTATA`) |
| Categoria Pokédex | Rat |
| Descrição Pokédex | Bites anything when it attacks. Small and very quick, it is a common sight in many places |
| Altura | 1'00" (0,30 m) |
| Peso | 8,0 lb (3,6 kg) |
| Tipo | Normal |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 57 / Medium Fast |
| Atributos base | HP 30; Atk 56; Def 35; Spd 72; Spc 25; BST 218 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 115-207; Def 74-166; Spd 147-239; Spc 54-146 |
| Movimentos iniciais | Tackle, Tail Whip |
| Movimentos aprendidos por nível | Nv.7 Quick Attack; Nv.14 Hyper Fang; Nv.23 Focus Energy; Nv.34 Super Fang |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Raticate ao atingir Nv.20 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 1 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (35,2%), Nv.4 (5,1%)<br>Route 16 - terrestre/caverna, limiar 25/256: Nv.18 (15,2%), Nv.20 (9,8%), Nv.22 (5,1%)<br>Route 2 - terrestre/caverna, limiar 25/256: Nv.2 (5,1%), Nv.3 (19,9%), Nv.4 (9,8%), Nv.5 (5,1%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.21 (19,9%), Nv.23 (9,8%)<br>Route 22 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (19,9%), Nv.4 (15,2%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.8 (15,2%), Nv.10 (19,9%), Nv.12 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.14 (15,2%), Nv.16 (19,9%), Nv.17 (5,1%) |
| Spawns em Blue | Route 1 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (35,2%), Nv.4 (5,1%)<br>Route 16 - terrestre/caverna, limiar 25/256: Nv.18 (15,2%), Nv.20 (9,8%), Nv.22 (5,1%)<br>Route 2 - terrestre/caverna, limiar 25/256: Nv.2 (5,1%), Nv.3 (19,9%), Nv.4 (9,8%), Nv.5 (5,1%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.21 (19,9%), Nv.23 (9,8%)<br>Route 22 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (19,9%), Nv.4 (15,2%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.8 (15,2%), Nv.10 (19,9%), Nv.12 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.14 (15,2%), Nv.16 (19,9%), Nv.17 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/rattata.asm` |

### 020 Raticate

| Campo | Valor |
|---|---|
| Nome/espécie | Raticate (`DEX_RATICATE`) |
| Categoria Pokédex | Rat |
| Descrição Pokédex | It uses its whiskers to maintain its balance. It apparently slows down if they are cut off |
| Altura | 2'04" (0,71 m) |
| Peso | 41,0 lb (18,6 kg) |
| Tipo | Normal |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 116 / Medium Fast |
| Atributos base | HP 55; Atk 81; Def 60; Spd 97; Spc 50; BST 343 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 165-257; Def 123-215; Spd 197-289; Spc 104-196 |
| Movimentos iniciais | Tackle, Tail Whip, Quick Attack |
| Movimentos aprendidos por nível | Nv.7 Quick Attack; Nv.14 Hyper Fang; Nv.27 Focus Energy; Nv.41 Super Fang |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Rattata: Raticate ao atingir Nv.20 ou superior após ganho de nível |
| Spawns em Red | Route 16 - terrestre/caverna, limiar 25/256: Nv.23 (4,3%), Nv.25 (1,2%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.25 (15,2%), Nv.27 (9,8%), Nv.29 (5,1%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.25 (15,2%), Nv.29 (5,1%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.30 (15,2%) |
| Spawns em Blue | Route 16 - terrestre/caverna, limiar 25/256: Nv.23 (4,3%), Nv.25 (1,2%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.25 (15,2%), Nv.27 (9,8%), Nv.29 (5,1%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.25 (15,2%), Nv.29 (5,1%)<br>Route 21 - terrestre/caverna, limiar 25/256: Nv.30 (15,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/raticate.asm` |

### 021 Spearow

| Campo | Valor |
|---|---|
| Nome/espécie | Spearow (`DEX_SPEAROW`) |
| Categoria Pokédex | Tiny Bird |
| Descrição Pokédex | Eats bugs in grassy areas. It has to flap its short wings at high speed to stay airborne |
| Altura | 1'00" (0,30 m) |
| Peso | 4,0 lb (1,8 kg) |
| Tipo | Normal / Flying |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 58 / Medium Fast |
| Atributos base | HP 40; Atk 60; Def 30; Spd 70; Spc 31; BST 231 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 123-215; Def 64-156; Spd 143-235; Spc 66-158 |
| Movimentos iniciais | Peck, Growl |
| Movimentos aprendidos por nível | Nv.9 Leer; Nv.15 Fury Attack; Nv.22 Mirror Move; Nv.29 Drill Peck; Nv.36 Agility |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Fearow ao atingir Nv.20 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 10 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.16 (19,9%), Nv.17 (5,1%)<br>Route 11 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.15 (19,9%), Nv.17 (5,1%)<br>Route 16 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 22 - terrestre/caverna, limiar 25/256: Nv.3 (5,1%), Nv.5 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.26 (15,2%)<br>Route 3 - terrestre/caverna, limiar 20/256: Nv.5 (19,9%), Nv.6 (9,8%), Nv.7 (9,8%), Nv.8 (5,1%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.8 (9,8%), Nv.10 (19,9%), Nv.12 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.16 (19,9%), Nv.17 (5,1%) |
| Spawns em Blue | Route 10 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.16 (19,9%), Nv.17 (5,1%)<br>Route 11 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.15 (19,9%), Nv.17 (5,1%)<br>Route 16 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.20 (19,9%), Nv.22 (19,9%)<br>Route 22 - terrestre/caverna, limiar 25/256: Nv.3 (5,1%), Nv.5 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.26 (15,2%)<br>Route 3 - terrestre/caverna, limiar 20/256: Nv.5 (19,9%), Nv.6 (9,8%), Nv.7 (9,8%), Nv.8 (5,1%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.8 (9,8%), Nv.10 (19,9%), Nv.12 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.13 (9,8%), Nv.16 (19,9%), Nv.17 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/spearow.asm` |

### 022 Fearow

| Campo | Valor |
|---|---|
| Nome/espécie | Fearow (`DEX_FEAROW`) |
| Categoria Pokédex | Beak |
| Descrição Pokédex | With its huge and magnificent wings, it can keep aloft without ever having to land for rest |
| Altura | 3'11" (1,19 m) |
| Peso | 84,0 lb (38,1 kg) |
| Tipo | Normal / Flying |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 162 / Medium Fast |
| Atributos base | HP 65; Atk 90; Def 65; Spd 100; Spc 61; BST 381 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 183-275; Def 133-225; Spd 203-295; Spc 125-217 |
| Movimentos iniciais | Peck, Growl, Leer |
| Movimentos aprendidos por nível | Nv.9 Leer; Nv.15 Fury Attack; Nv.25 Mirror Move; Nv.34 Drill Peck; Nv.43 Agility |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Spearow: Fearow ao atingir Nv.20 ou superior após ganho de nível |
| Spawns em Red | Route 17 - terrestre/caverna, limiar 25/256: Nv.25 (4,3%), Nv.27 (1,2%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.25 (9,8%), Nv.27 (4,3%), Nv.29 (1,2%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.38 (19,5%), Nv.41 (4,3%), Nv.43 (1,2%) |
| Spawns em Blue | Route 17 - terrestre/caverna, limiar 25/256: Nv.25 (4,3%), Nv.27 (1,2%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.25 (9,8%), Nv.27 (4,3%), Nv.29 (1,2%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.38 (19,5%), Nv.41 (4,3%), Nv.43 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/fearow.asm` |

### 023 Ekans

| Campo | Valor |
|---|---|
| Nome/espécie | Ekans (`DEX_EKANS`) |
| Categoria Pokédex | Snake |
| Descrição Pokédex | Moves silently and stealthily. Eats the eggs of birds, such as PIDGEY and SPEAROW, whole |
| Altura | 6'07" (2,01 m) |
| Peso | 15,0 lb (6,8 kg) |
| Tipo | Poison |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 62 / Medium Fast |
| Atributos base | HP 35; Atk 60; Def 44; Spd 55; Spc 40; BST 234 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 123-215; Def 92-184; Spd 113-205; Spc 84-176 |
| Movimentos iniciais | Wrap, Leer |
| Movimentos aprendidos por nível | Nv.10 Poison Sting; Nv.17 Bite; Nv.24 Glare; Nv.31 Screech; Nv.38 Acid |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Arbok ao atingir Nv.22 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 10 - terrestre/caverna, limiar 15/256: Nv.11 (9,8%), Nv.13 (4,3%), Nv.15 (9,8%), Nv.17 (1,2%)<br>Route 11 - terrestre/caverna, limiar 15/256: Nv.12 (15,2%), Nv.14 (19,9%), Nv.15 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.26 (19,9%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.6 (9,8%), Nv.8 (4,3%), Nv.10 (9,8%), Nv.12 (1,2%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.17 (15,2%), Nv.19 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.11 (9,8%), Nv.13 (4,3%), Nv.15 (9,8%), Nv.17 (1,2%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/ekans.asm` |

### 024 Arbok

| Campo | Valor |
|---|---|
| Nome/espécie | Arbok (`DEX_ARBOK`) |
| Categoria Pokédex | Cobra |
| Descrição Pokédex | It is rumored that the ferocious warning markings on its belly differ from area to area |
| Altura | 11'06" (3,51 m) |
| Peso | 143,0 lb (64,9 kg) |
| Tipo | Poison |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 147 / Medium Fast |
| Atributos base | HP 60; Atk 85; Def 69; Spd 80; Spc 65; BST 359 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 173-265; Def 141-233; Spd 163-255; Spc 133-225 |
| Movimentos iniciais | Wrap, Leer, Poison Sting |
| Movimentos aprendidos por nível | Nv.10 Poison Sting; Nv.17 Bite; Nv.27 Glare; Nv.36 Screech; Nv.47 Acid |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Ekans: Arbok ao atingir Nv.22 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.57 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.41 (5,1%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/arbok.asm` |

### 025 Pikachu

| Campo | Valor |
|---|---|
| Nome/espécie | Pikachu (`DEX_PIKACHU`) |
| Categoria Pokédex | Mouse |
| Descrição Pokédex | When several of these Pokémon gather, their electricity could build and cause lightning storms |
| Altura | 1'04" (0,41 m) |
| Peso | 13,0 lb (5,9 kg) |
| Tipo | Electric |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 82 / Medium Fast |
| Atributos base | HP 35; Atk 55; Def 30; Spd 90; Spc 50; BST 260 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 113-205; Def 64-156; Spd 183-275; Spc 104-196 |
| Movimentos iniciais | Thundershock, Growl |
| Movimentos aprendidos por nível | Nv.9 Thunder Wave; Nv.16 Quick Attack; Nv.26 Swift; Nv.33 Agility; Nv.43 Thunder |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM16 Pay Day; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Raichu ao usar Thunder Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Power Plant - terrestre/caverna, limiar 10/256: Nv.20 (15,2%), Nv.24 (9,8%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (4,3%), Nv.5 (1,2%) |
| Spawns em Blue | Power Plant - terrestre/caverna, limiar 10/256: Nv.20 (15,2%), Nv.24 (9,8%)<br>Viridian Forest - terrestre/caverna, limiar 8/256: Nv.3 (4,3%), Nv.5 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/pikachu.asm` |

### 026 Raichu

| Campo | Valor |
|---|---|
| Nome/espécie | Raichu (`DEX_RAICHU`) |
| Categoria Pokédex | Mouse |
| Descrição Pokédex | Its long tail serves as a ground to protect itself from its own high voltage power |
| Altura | 2'07" (0,79 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Electric |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 122 / Medium Fast |
| Atributos base | HP 60; Atk 90; Def 55; Spd 100; Spc 90; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 183-275; Def 113-205; Spd 203-295; Spc 183-275 |
| Movimentos iniciais | Thundershock, Growl, Thunder Wave |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Pikachu: Raichu ao usar Thunder Stone; nível mínimo 1 |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.53 (4,3%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.53 (4,3%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%)<br>Power Plant - terrestre/caverna, limiar 10/256: Nv.33 (4,3%), Nv.36 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/raichu.asm` |

### 027 Sandshrew

| Campo | Valor |
|---|---|
| Nome/espécie | Sandshrew (`DEX_SANDSHREW`) |
| Categoria Pokédex | Mouse |
| Descrição Pokédex | Burrows deep underground in arid locations far from water. It only emerges to hunt for food |
| Altura | 2'00" (0,61 m) |
| Peso | 26,0 lb (11,8 kg) |
| Tipo | Ground |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 93 / Medium Fast |
| Atributos base | HP 50; Atk 75; Def 85; Spd 40; Spc 30; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 153-245; Def 173-265; Spd 84-176; Spc 64-156 |
| Movimentos iniciais | Scratch |
| Movimentos aprendidos por nível | Nv.10 Sand-Attack; Nv.17 Slash; Nv.24 Poison Sting; Nv.31 Swift; Nv.38 Fury Swipes |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Sandslash ao atingir Nv.22 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Route 10 - terrestre/caverna, limiar 15/256: Nv.11 (9,8%), Nv.13 (4,3%), Nv.15 (9,8%), Nv.17 (1,2%)<br>Route 11 - terrestre/caverna, limiar 15/256: Nv.12 (15,2%), Nv.14 (19,9%), Nv.15 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.26 (19,9%)<br>Route 4 - terrestre/caverna, limiar 20/256: Nv.6 (9,8%), Nv.8 (4,3%), Nv.10 (9,8%), Nv.12 (1,2%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.17 (15,2%), Nv.19 (5,1%)<br>Route 9 - terrestre/caverna, limiar 15/256: Nv.11 (9,8%), Nv.13 (4,3%), Nv.15 (9,8%), Nv.17 (1,2%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/sandshrew.asm` |

### 028 Sandslash

| Campo | Valor |
|---|---|
| Nome/espécie | Sandslash (`DEX_SANDSLASH`) |
| Categoria Pokédex | Mouse |
| Descrição Pokédex | Curls up into a spiny ball when threatened. It can roll while curled up to attack or escape |
| Altura | 3'03" (0,99 m) |
| Peso | 65,0 lb (29,5 kg) |
| Tipo | Ground |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 163 / Medium Fast |
| Atributos base | HP 75; Atk 100; Def 110; Spd 65; Spc 55; BST 405 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 257-349; Atk 203-295; Def 222-314; Spd 133-225; Spc 113-205 |
| Movimentos iniciais | Scratch, Sand-Attack |
| Movimentos aprendidos por nível | Nv.10 Sand-Attack; Nv.17 Slash; Nv.27 Poison Sting; Nv.36 Swift; Nv.47 Fury Swipes |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Sandshrew: Sandslash ao atingir Nv.22 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.57 (5,1%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.41 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/sandslash.asm` |

### 029 Nidoran♀

| Campo | Valor |
|---|---|
| Nome/espécie | Nidoran♀ (`DEX_NIDORAN_F`) |
| Categoria Pokédex | Poison Pin |
| Descrição Pokédex | Although small, its venomous barbs render this Pokémon dangerous. The female has smaller horns |
| Altura | 1'04" (0,41 m) |
| Peso | 15,0 lb (6,8 kg) |
| Tipo | Poison |
| Catch rate | 235; cenário normalizado: 30,97% (muito favorável) |
| EXP base / crescimento | 59 / Medium Slow |
| Atributos base | HP 55; Atk 47; Def 52; Spd 41; Spc 40; BST 235 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 98-190; Def 107-200; Spd 86-178; Spc 84-176 |
| Movimentos iniciais | Growl, Tackle |
| Movimentos aprendidos por nível | Nv.8 Scratch; Nv.14 Poison Sting; Nv.21 Tail Whip; Nv.29 Bite; Nv.36 Fury Swipes; Nv.43 Double Kick |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Nidorina ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 22 - terrestre/caverna, limiar 25/256: Nv.3 (4,3%), Nv.4 (1,2%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.24 (5,1%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.25 (5,1%) |
| Spawns em Blue | Route 22 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (19,9%), Nv.4 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.22 (19,9%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.24 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.22 (19,9%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.25 (19,9%) |
| Aquisição especial em Red | Troca NPC em Underground Path Route 5: entregar Nidoran♂; recebido no mesmo nível, apelido SPOT |
| Aquisição especial em Blue | Troca NPC em Underground Path Route 5: entregar Nidoran♂; recebido no mesmo nível, apelido SPOT |
| Fonte específica | `data/pokemon/base_stats/nidoranf.asm` |

### 030 Nidorina

| Campo | Valor |
|---|---|
| Nome/espécie | Nidorina (`DEX_NIDORINA`) |
| Categoria Pokédex | Poison Pin |
| Descrição Pokédex | The female's horn develops slowly. Prefers physical attacks such as clawing and biting |
| Altura | 2'07" (0,79 m) |
| Peso | 44,0 lb (20,0 kg) |
| Tipo | Poison |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 117 / Medium Slow |
| Atributos base | HP 70; Atk 62; Def 67; Spd 56; Spc 55; BST 310 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 127-219; Def 137-229; Spd 115-207; Spc 113-205 |
| Movimentos iniciais | Growl, Tackle, Scratch |
| Movimentos aprendidos por nível | Nv.8 Scratch; Nv.14 Poison Sting; Nv.23 Tail Whip; Nv.32 Bite; Nv.41 Fury Swipes; Nv.50 Double Kick |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Nidoqueen ao usar Moon Stone; nível mínimo 1 |
| Origem por evolução | Nidoran♀: Nidorina ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.31 (5,1%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.30 (5,1%) |
| Spawns em Blue | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.31 (9,8%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.33 (9,8%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.30 (9,8%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.33 (9,8%) |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.17, por 1200 moedas<br>Troca NPC em Route 11 Gate 2F: entregar Nidorino; recebido no mesmo nível, apelido TERRY |
| Aquisição especial em Blue | Troca NPC em Route 11 Gate 2F: entregar Nidorino; recebido no mesmo nível, apelido TERRY |
| Fonte específica | `data/pokemon/base_stats/nidorina.asm` |

### 031 Nidoqueen

| Campo | Valor |
|---|---|
| Nome/espécie | Nidoqueen (`DEX_NIDOQUEEN`) |
| Categoria Pokédex | Drill |
| Descrição Pokédex | Its hard scales provide strong protection. It uses its hefty bulk to execute powerful moves |
| Altura | 4'03" (1,30 m) |
| Peso | 132,0 lb (59,9 kg) |
| Tipo | Poison / Ground |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 194 / Medium Slow |
| Atributos base | HP 90; Atk 82; Def 87; Spd 76; Spc 75; BST 410 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 167-259; Def 177-269; Spd 155-247; Spc 153-245 |
| Movimentos iniciais | Tackle, Scratch, Tail Whip, Body Slam |
| Movimentos aprendidos por nível | Nv.8 Scratch; Nv.14 Poison Sting; Nv.23 Body Slam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Nidorina: Nidoqueen ao usar Moon Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/nidoqueen.asm` |

### 032 Nidoran♂

| Campo | Valor |
|---|---|
| Nome/espécie | Nidoran♂ (`DEX_NIDORAN_M`) |
| Categoria Pokédex | Poison Pin |
| Descrição Pokédex | Stiffens its ears to sense danger. The larger its horns, the more powerful its secreted venom |
| Altura | 1'08" (0,51 m) |
| Peso | 20,0 lb (9,1 kg) |
| Tipo | Poison |
| Catch rate | 235; cenário normalizado: 30,97% (muito favorável) |
| EXP base / crescimento | 60 / Medium Slow |
| Atributos base | HP 46; Atk 57; Def 40; Spd 50; Spc 40; BST 233 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 200-292; Atk 117-209; Def 84-176; Spd 104-196; Spc 84-176 |
| Movimentos iniciais | Leer, Tackle |
| Movimentos aprendidos por nível | Nv.8 Horn Attack; Nv.14 Poison Sting; Nv.21 Focus Energy; Nv.29 Fury Attack; Nv.36 Horn Drill; Nv.43 Double Kick |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Nidorino ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 22 - terrestre/caverna, limiar 25/256: Nv.2 (9,8%), Nv.3 (19,9%), Nv.4 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.22 (19,9%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.24 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.22 (19,9%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.25 (19,9%) |
| Spawns em Blue | Route 22 - terrestre/caverna, limiar 25/256: Nv.3 (4,3%), Nv.4 (1,2%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.24 (5,1%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.25 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/nidoranm.asm` |

### 033 Nidorino

| Campo | Valor |
|---|---|
| Nome/espécie | Nidorino (`DEX_NIDORINO`) |
| Categoria Pokédex | Poison Pin |
| Descrição Pokédex | An aggressive Pokémon that is quick to attack. The horn on its head secretes a powerful venom |
| Altura | 2'11" (0,89 m) |
| Peso | 43,0 lb (19,5 kg) |
| Tipo | Poison |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 118 / Medium Slow |
| Atributos base | HP 61; Atk 72; Def 57; Spd 65; Spc 55; BST 310 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 229-321; Atk 147-239; Def 117-209; Spd 133-225; Spc 113-205 |
| Movimentos iniciais | Leer, Tackle, Horn Attack |
| Movimentos aprendidos por nível | Nv.8 Horn Attack; Nv.14 Poison Sting; Nv.23 Focus Energy; Nv.32 Fury Attack; Nv.41 Horn Drill; Nv.50 Double Kick |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Nidoking ao usar Moon Stone; nível mínimo 1 |
| Origem por evolução | Nidoran♂: Nidorino ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.31 (9,8%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.33 (9,8%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.30 (9,8%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.33 (9,8%) |
| Spawns em Blue | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.31 (5,1%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.30 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.17, por 1200 moedas |
| Fonte específica | `data/pokemon/base_stats/nidorino.asm` |

### 034 Nidoking

| Campo | Valor |
|---|---|
| Nome/espécie | Nidoking (`DEX_NIDOKING`) |
| Categoria Pokédex | Drill |
| Descrição Pokédex | It uses its powerful tail in battle to smash, constrict, then break the prey's bones |
| Altura | 4'07" (1,40 m) |
| Peso | 137,0 lb (62,1 kg) |
| Tipo | Poison / Ground |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 195 / Medium Slow |
| Atributos base | HP 81; Atk 92; Def 77; Spd 85; Spc 75; BST 410 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 269-361; Atk 187-279; Def 157-249; Spd 173-265; Spc 153-245 |
| Movimentos iniciais | Tackle, Horn Attack, Poison Sting, Thrash |
| Movimentos aprendidos por nível | Nv.8 Horn Attack; Nv.14 Poison Sting; Nv.23 Thrash |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Nidorino: Nidoking ao usar Moon Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/nidoking.asm` |

### 035 Clefairy

| Campo | Valor |
|---|---|
| Nome/espécie | Clefairy (`DEX_CLEFAIRY`) |
| Categoria Pokédex | Fairy |
| Descrição Pokédex | Its magical and cute appeal has many admirers. It is rare and found only in certain areas |
| Altura | 2'00" (0,61 m) |
| Peso | 17,0 lb (7,7 kg) |
| Tipo | Normal |
| Catch rate | 150; cenário normalizado: 19,82% (intermediária) |
| EXP base / crescimento | 68 / Fast |
| Atributos base | HP 70; Atk 45; Def 48; Spd 35; Spc 60; BST 258 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 94-186; Def 100-192; Spd 74-166; Spc 123-215 |
| Movimentos iniciais | Pound, Growl |
| Movimentos aprendidos por nível | Nv.13 Sing; Nv.18 Doubleslap; Nv.24 Minimize; Nv.31 Metronome; Nv.39 Defense Curl; Nv.48 Light Screen |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Clefable ao usar Moon Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (1,2%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.9 (4,3%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.10 (5,1%), Nv.12 (1,2%) |
| Spawns em Blue | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (1,2%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.9 (4,3%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.10 (5,1%), Nv.12 (1,2%) |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.8, por 500 moedas |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.12, por 750 moedas |
| Fonte específica | `data/pokemon/base_stats/clefairy.asm` |

### 036 Clefable

| Campo | Valor |
|---|---|
| Nome/espécie | Clefable (`DEX_CLEFABLE`) |
| Categoria Pokédex | Fairy |
| Descrição Pokédex | A timid fairy Pokémon that is rarely seen. It will run and hide the moment it senses people |
| Altura | 4'03" (1,30 m) |
| Peso | 88,0 lb (39,9 kg) |
| Tipo | Normal |
| Catch rate | 25; cenário normalizado: 3,41% (muito difícil) |
| EXP base / crescimento | 129 / Fast |
| Atributos base | HP 95; Atk 70; Def 73; Spd 60; Spc 85; BST 383 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 297-389; Atk 143-235; Def 149-241; Spd 123-215; Spc 173-265 |
| Movimentos iniciais | Sing, Doubleslap, Minimize, Metronome |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Clefairy: Clefable ao usar Moon Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/clefable.asm` |

### 037 Vulpix

| Campo | Valor |
|---|---|
| Nome/espécie | Vulpix (`DEX_VULPIX`) |
| Categoria Pokédex | Fox |
| Descrição Pokédex | At the time of birth, it has just one tail. The tail splits from its tip as it grows older |
| Altura | 2'00" (0,61 m) |
| Peso | 22,0 lb (10,0 kg) |
| Tipo | Fire |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 63 / Medium Fast |
| Atributos base | HP 38; Atk 41; Def 40; Spd 65; Spc 65; BST 249 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 184-276; Atk 86-178; Def 84-176; Spd 133-225; Spc 133-225 |
| Movimentos iniciais | Ember, Tail Whip |
| Movimentos aprendidos por nível | Nv.16 Quick Attack; Nv.21 Roar; Nv.28 Confuse Ray; Nv.35 Flamethrower; Nv.42 Fire Spin |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Ninetales ao usar Fire Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.34 (9,8%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.32 (19,9%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.33 (19,9%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.35 (15,2%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.18 (5,1%), Nv.20 (5,1%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.15 (4,3%), Nv.16 (9,8%), Nv.17 (5,1%), Nv.18 (1,2%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/vulpix.asm` |

### 038 Ninetales

| Campo | Valor |
|---|---|
| Nome/espécie | Ninetales (`DEX_NINETALES`) |
| Categoria Pokédex | Fox |
| Descrição Pokédex | Very smart and very vengeful. Grabbing one of its many tails could result in a 1000-year curse |
| Altura | 3'07" (1,09 m) |
| Peso | 44,0 lb (20,0 kg) |
| Tipo | Fire |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 178 / Medium Fast |
| Atributos base | HP 73; Atk 76; Def 75; Spd 100; Spc 100; BST 424 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 253-345; Atk 155-247; Def 153-245; Spd 203-295; Spc 203-295 |
| Movimentos iniciais | Ember, Tail Whip, Quick Attack, Roar |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Vulpix: Ninetales ao usar Fire Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/ninetales.asm` |

### 039 Jigglypuff

| Campo | Valor |
|---|---|
| Nome/espécie | Jigglypuff (`DEX_JIGGLYPUFF`) |
| Categoria Pokédex | Balloon |
| Descrição Pokédex | When its huge eyes light up, it sings a mysteriously soothing melody that lulls its enemies to sleep |
| Altura | 1'08" (0,51 m) |
| Peso | 12,0 lb (5,4 kg) |
| Tipo | Normal |
| Catch rate | 170; cenário normalizado: 22,44% (favorável) |
| EXP base / crescimento | 76 / Fast |
| Atributos base | HP 115; Atk 45; Def 20; Spd 20; Spc 25; BST 225 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 336-428; Atk 94-186; Def 44-136; Spd 44-136; Spc 54-146 |
| Movimentos iniciais | Sing |
| Movimentos aprendidos por nível | Nv.9 Pound; Nv.14 Disable; Nv.19 Defense Curl; Nv.24 Doubleslap; Nv.29 Rest; Nv.34 Body Slam; Nv.39 Double-Edge |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Wigglytuff ao usar Moon Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 3 - terrestre/caverna, limiar 20/256: Nv.3 (5,1%), Nv.5 (4,3%), Nv.7 (1,2%) |
| Spawns em Blue | Route 3 - terrestre/caverna, limiar 20/256: Nv.3 (5,1%), Nv.5 (4,3%), Nv.7 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/jigglypuff.asm` |

### 040 Wigglytuff

| Campo | Valor |
|---|---|
| Nome/espécie | Wigglytuff (`DEX_WIGGLYTUFF`) |
| Categoria Pokédex | Balloon |
| Descrição Pokédex | The body is soft and rubbery. When angered, it will suck in air and inflate itself to an enormous size |
| Altura | 3'03" (0,99 m) |
| Peso | 26,0 lb (11,8 kg) |
| Tipo | Normal |
| Catch rate | 50; cenário normalizado: 6,69% (difícil) |
| EXP base / crescimento | 109 / Fast |
| Atributos base | HP 140; Atk 70; Def 45; Spd 45; Spc 50; BST 350 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 386-478; Atk 143-235; Def 94-186; Spd 94-186; Spc 104-196 |
| Movimentos iniciais | Sing, Disable, Defense Curl, Doubleslap |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Jigglypuff: Wigglytuff ao usar Moon Stone; nível mínimo 1 |
| Spawns em Red | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.54 (5,1%) |
| Spawns em Blue | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.54 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/wigglytuff.asm` |

### 041 Zubat

| Campo | Valor |
|---|---|
| Nome/espécie | Zubat (`DEX_ZUBAT`) |
| Categoria Pokédex | Bat |
| Descrição Pokédex | Forms colonies in perpetually dark places. Uses ultrasonic waves to identify and approach targets |
| Altura | 2'07" (0,79 m) |
| Peso | 17,0 lb (7,7 kg) |
| Tipo | Poison / Flying |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 54 / Medium Fast |
| Atributos base | HP 40; Atk 45; Def 35; Spd 55; Spc 40; BST 215 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 94-186; Def 74-166; Spd 113-205; Spc 84-176 |
| Movimentos iniciais | Leech Life |
| Movimentos aprendidos por nível | Nv.10 Supersonic; Nv.15 Bite; Nv.21 Confuse Ray; Nv.28 Wing Attack; Nv.36 Haze |
| Movimentos possíveis por TM/HM | TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Golbat ao atingir Nv.22 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.6 (9,8%), Nv.7 (19,9%), Nv.8 (19,9%), Nv.9 (15,2%), Nv.10 (9,8%), Nv.11 (4,3%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.7 (19,9%), Nv.8 (19,9%), Nv.9 (9,8%), Nv.10 (5,1%), Nv.11 (5,1%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.9 (19,9%), Nv.10 (15,2%), Nv.11 (9,8%), Nv.12 (4,3%)<br>Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.15 (5,1%), Nv.16 (19,9%), Nv.17 (19,9%), Nv.18 (9,8%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.16 (19,9%), Nv.17 (19,9%), Nv.18 (9,8%)<br>Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.21 (9,8%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.22 (15,2%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.26 (15,2%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.22 (15,2%) |
| Spawns em Blue | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.6 (9,8%), Nv.7 (19,9%), Nv.8 (19,9%), Nv.9 (15,2%), Nv.10 (9,8%), Nv.11 (4,3%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.7 (19,9%), Nv.8 (19,9%), Nv.9 (9,8%), Nv.10 (5,1%), Nv.11 (5,1%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.9 (19,9%), Nv.10 (15,2%), Nv.11 (9,8%), Nv.12 (4,3%)<br>Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.15 (5,1%), Nv.16 (19,9%), Nv.17 (19,9%), Nv.18 (9,8%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.16 (19,9%), Nv.17 (19,9%), Nv.18 (9,8%)<br>Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.21 (9,8%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.22 (15,2%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.26 (15,2%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.22 (15,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/zubat.asm` |

### 042 Golbat

| Campo | Valor |
|---|---|
| Nome/espécie | Golbat (`DEX_GOLBAT`) |
| Categoria Pokédex | Bat |
| Descrição Pokédex | Once it strikes, it will not stop draining energy from the victim even if it gets too heavy to fly |
| Altura | 5'03" (1,60 m) |
| Peso | 121,0 lb (54,9 kg) |
| Tipo | Poison / Flying |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 171 / Medium Fast |
| Atributos base | HP 75; Atk 80; Def 70; Spd 90; Spc 75; BST 390 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 257-349; Atk 163-255; Def 143-235; Spd 183-275; Spc 153-245 |
| Movimentos iniciais | Leech Life, Screech, Bite |
| Movimentos aprendidos por nível | Nv.10 Supersonic; Nv.15 Bite; Nv.21 Confuse Ray; Nv.32 Wing Attack; Nv.43 Haze |
| Movimentos possíveis por TM/HM | TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Zubat: Golbat ao atingir Nv.22 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (19,9%)<br>Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.29 (5,1%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (4,3%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.32 (1,2%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.40 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (19,9%)<br>Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.29 (5,1%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (4,3%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.32 (1,2%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.40 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/golbat.asm` |

### 043 Oddish

| Campo | Valor |
|---|---|
| Nome/espécie | Oddish (`DEX_ODDISH`) |
| Categoria Pokédex | Weed |
| Descrição Pokédex | During the day, it keeps its face buried in the ground. At night, it wanders around sowing its seeds |
| Altura | 1'08" (0,51 m) |
| Peso | 12,0 lb (5,4 kg) |
| Tipo | Grass / Poison |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 78 / Medium Slow |
| Atributos base | HP 45; Atk 50; Def 55; Spd 30; Spc 75; BST 255 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 104-196; Def 113-205; Spd 64-156; Spc 153-245 |
| Movimentos iniciais | Absorb |
| Movimentos aprendidos por nível | Nv.15 Poisonpowder; Nv.17 Stun Spore; Nv.19 Sleep Powder; Nv.24 Acid; Nv.33 Petal Dance; Nv.46 Solarbeam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Gloom ao atingir Nv.21 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 12 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.12 (9,8%), Nv.13 (9,8%), Nv.14 (5,1%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.12 (9,8%), Nv.13 (9,8%), Nv.14 (5,1%)<br>Route 5 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (9,8%), Nv.16 (5,1%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (9,8%), Nv.16 (5,1%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.19 (19,9%), Nv.22 (9,8%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/oddish.asm` |

### 044 Gloom

| Campo | Valor |
|---|---|
| Nome/espécie | Gloom (`DEX_GLOOM`) |
| Categoria Pokédex | Weed |
| Descrição Pokédex | The fluid that oozes from its mouth isn't drool. It is a nectar that is used to attract prey |
| Altura | 2'07" (0,79 m) |
| Peso | 19,0 lb (8,6 kg) |
| Tipo | Grass / Poison |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 132 / Medium Slow |
| Atributos base | HP 60; Atk 65; Def 70; Spd 40; Spc 85; BST 320 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 133-225; Def 143-235; Spd 84-176; Spc 173-265 |
| Movimentos iniciais | Absorb, Poisonpowder, Stun Spore |
| Movimentos aprendidos por nível | Nv.15 Poisonpowder; Nv.17 Stun Spore; Nv.19 Sleep Powder; Nv.28 Acid; Nv.38 Petal Dance; Nv.52 Solarbeam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Vileplume ao usar Leaf Stone; nível mínimo 1 |
| Origem por evolução | Oddish: Gloom ao atingir Nv.21 ou superior após ganho de nível |
| Spawns em Red | Route 12 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.30 (5,1%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.30 (5,1%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/gloom.asm` |

### 045 Vileplume

| Campo | Valor |
|---|---|
| Nome/espécie | Vileplume (`DEX_VILEPLUME`) |
| Categoria Pokédex | Flower |
| Descrição Pokédex | The larger its petals, the more toxic pollen it contains. Its big head is heavy and hard to hold up |
| Altura | 3'11" (1,19 m) |
| Peso | 41,0 lb (18,6 kg) |
| Tipo | Grass / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 184 / Medium Slow |
| Atributos base | HP 75; Atk 80; Def 85; Spd 50; Spc 100; BST 390 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 257-349; Atk 163-255; Def 173-265; Spd 104-196; Spc 203-295 |
| Movimentos iniciais | Stun Spore, Sleep Powder, Acid, Petal Dance |
| Movimentos aprendidos por nível | Nv.15 Poisonpowder; Nv.17 Stun Spore; Nv.19 Sleep Powder |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Gloom: Vileplume ao usar Leaf Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/vileplume.asm` |

### 046 Paras

| Campo | Valor |
|---|---|
| Nome/espécie | Paras (`DEX_PARAS`) |
| Categoria Pokédex | Mushroom |
| Descrição Pokédex | Burrows to suck tree roots. The mushrooms on its back grow by drawing nutrients from the bug host |
| Altura | 1'00" (0,30 m) |
| Peso | 12,0 lb (5,4 kg) |
| Tipo | Bug / Grass |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 70 / Medium Fast |
| Atributos base | HP 35; Atk 70; Def 55; Spd 25; Spc 55; BST 240 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 143-235; Def 113-205; Spd 54-146; Spc 113-205 |
| Movimentos iniciais | Scratch |
| Movimentos aprendidos por nível | Nv.13 Stun Spore; Nv.20 Leech Life; Nv.27 Spore; Nv.34 Slash; Nv.41 Growth |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Parasect ao atingir Nv.24 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (5,1%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.10 (9,8%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.10 (9,8%), Nv.12 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.22 (15,2%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.23 (15,2%) |
| Spawns em Blue | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (5,1%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.10 (9,8%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.10 (9,8%), Nv.12 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.22 (15,2%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.23 (15,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/paras.asm` |

### 047 Parasect

| Campo | Valor |
|---|---|
| Nome/espécie | Parasect (`DEX_PARASECT`) |
| Categoria Pokédex | Mushroom |
| Descrição Pokédex | A host-parasite pair in which the parasite mushroom has taken over the host bug. Prefers damp places |
| Altura | 3'03" (0,99 m) |
| Peso | 65,0 lb (29,5 kg) |
| Tipo | Bug / Grass |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 128 / Medium Fast |
| Atributos base | HP 60; Atk 95; Def 80; Spd 30; Spc 80; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 193-285; Def 163-255; Spd 64-156; Spc 163-255 |
| Movimentos iniciais | Scratch, Stun Spore, Leech Life |
| Movimentos aprendidos por nível | Nv.13 Stun Spore; Nv.20 Leech Life; Nv.30 Spore; Nv.39 Slash; Nv.48 Growth |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Paras: Parasect ao atingir Nv.24 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.52 (5,1%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.30 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.25 (5,1%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.52 (5,1%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.30 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.25 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/parasect.asm` |

### 048 Venonat

| Campo | Valor |
|---|---|
| Nome/espécie | Venonat (`DEX_VENONAT`) |
| Categoria Pokédex | Insect |
| Descrição Pokédex | Lives in the shadows of tall trees where it eats insects. It is attracted by light at night |
| Altura | 3'03" (0,99 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Bug / Poison |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 75 / Medium Fast |
| Atributos base | HP 60; Atk 55; Def 50; Spd 45; Spc 40; BST 250 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 113-205; Def 104-196; Spd 94-186; Spc 84-176 |
| Movimentos iniciais | Tackle, Disable |
| Movimentos aprendidos por nível | Nv.24 Poisonpowder; Nv.27 Leech Life; Nv.30 Stun Spore; Nv.35 Psybeam; Nv.38 Sleep Powder; Nv.43 Psychic |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Venomoth ao atingir Nv.31 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 12 - terrestre/caverna, limiar 15/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.26 (9,8%), Nv.28 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.22 (15,2%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.23 (15,2%) |
| Spawns em Blue | Route 12 - terrestre/caverna, limiar 15/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.24 (9,8%), Nv.26 (9,8%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.26 (9,8%), Nv.28 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.22 (15,2%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.23 (15,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/venonat.asm` |

### 049 Venomoth

| Campo | Valor |
|---|---|
| Nome/espécie | Venomoth (`DEX_VENOMOTH`) |
| Categoria Pokédex | Poisonmoth |
| Descrição Pokédex | The dust-like scales covering its wings are color coded to indicate the kinds of poison it has |
| Altura | 4'11" (1,50 m) |
| Peso | 28,0 lb (12,7 kg) |
| Tipo | Bug / Poison |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 138 / Medium Fast |
| Atributos base | HP 70; Atk 65; Def 60; Spd 90; Spc 90; BST 375 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 133-225; Def 123-215; Spd 183-275; Spc 183-275 |
| Movimentos iniciais | Tackle, Disable, Poisonpowder, Leech Life |
| Movimentos aprendidos por nível | Nv.24 Poisonpowder; Nv.27 Leech Life; Nv.30 Stun Spore; Nv.38 Psybeam; Nv.43 Sleep Powder; Nv.50 Psychic |
| Movimentos possíveis por TM/HM | TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Venonat: Venomoth ao atingir Nv.31 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (9,8%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.32 (5,1%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.31 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.40 (9,8%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (9,8%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.32 (5,1%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.31 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.40 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/venomoth.asm` |

### 050 Diglett

| Campo | Valor |
|---|---|
| Nome/espécie | Diglett (`DEX_DIGLETT`) |
| Categoria Pokédex | Mole |
| Descrição Pokédex | Lives about one yard underground where it feeds on plant roots. It sometimes appears above ground |
| Altura | 0'08" (0,20 m) |
| Peso | 2,0 lb (0,9 kg) |
| Tipo | Ground |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 81 / Medium Fast |
| Atributos base | HP 10; Atk 55; Def 25; Spd 95; Spc 45; BST 230 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 128-220; Atk 113-205; Def 54-146; Spd 193-285; Spc 94-186 |
| Movimentos iniciais | Scratch |
| Movimentos aprendidos por nível | Nv.15 Growl; Nv.19 Dig; Nv.24 Sand-Attack; Nv.31 Slash; Nv.40 Earthquake |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Dugtrio ao atingir Nv.26 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Diglett's Cave - terrestre/caverna, limiar 20/256: Nv.15 (9,8%), Nv.16 (9,8%), Nv.17 (15,2%), Nv.18 (19,9%), Nv.19 (19,9%), Nv.20 (9,8%), Nv.21 (5,1%), Nv.22 (5,1%) |
| Spawns em Blue | Diglett's Cave - terrestre/caverna, limiar 20/256: Nv.15 (9,8%), Nv.16 (9,8%), Nv.17 (15,2%), Nv.18 (19,9%), Nv.19 (19,9%), Nv.20 (9,8%), Nv.21 (5,1%), Nv.22 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/diglett.asm` |

### 051 Dugtrio

| Campo | Valor |
|---|---|
| Nome/espécie | Dugtrio (`DEX_DUGTRIO`) |
| Categoria Pokédex | Mole |
| Descrição Pokédex | A team of DIGLETT triplets. It triggers huge earthquakes by burrowing 60 miles underground |
| Altura | 2'04" (0,71 m) |
| Peso | 73,0 lb (33,1 kg) |
| Tipo | Ground |
| Catch rate | 50; cenário normalizado: 6,69% (difícil) |
| EXP base / crescimento | 153 / Medium Fast |
| Atributos base | HP 35; Atk 80; Def 50; Spd 120; Spc 70; BST 355 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 163-255; Def 104-196; Spd 242-334; Spc 143-235 |
| Movimentos iniciais | Scratch, Growl, Dig |
| Movimentos aprendidos por nível | Nv.15 Growl; Nv.19 Dig; Nv.24 Sand-Attack; Nv.35 Slash; Nv.47 Earthquake |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Diglett: Dugtrio ao atingir Nv.26 ou superior após ganho de nível |
| Spawns em Red | Diglett's Cave - terrestre/caverna, limiar 20/256: Nv.29 (4,3%), Nv.31 (1,2%) |
| Spawns em Blue | Diglett's Cave - terrestre/caverna, limiar 20/256: Nv.29 (4,3%), Nv.31 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/dugtrio.asm` |

### 052 Meowth

| Campo | Valor |
|---|---|
| Nome/espécie | Meowth (`DEX_MEOWTH`) |
| Categoria Pokédex | Scratchcat |
| Descrição Pokédex | Adores circular objects. Wanders the streets on a nightly basis to look for dropped loose change |
| Altura | 1'04" (0,41 m) |
| Peso | 9,0 lb (4,1 kg) |
| Tipo | Normal |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 69 / Medium Fast |
| Atributos base | HP 40; Atk 45; Def 35; Spd 90; Spc 40; BST 250 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 94-186; Def 74-166; Spd 183-275; Spc 84-176 |
| Movimentos iniciais | Scratch, Growl |
| Movimentos aprendidos por nível | Nv.12 Bite; Nv.17 Pay Day; Nv.24 Screech; Nv.33 Fury Swipes; Nv.44 Slash |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM16 Pay Day; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Persian ao atingir Nv.28 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Route 5 - terrestre/caverna, limiar 15/256: Nv.10 (9,8%), Nv.12 (9,8%), Nv.14 (4,3%), Nv.16 (1,2%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.10 (9,8%), Nv.12 (9,8%), Nv.14 (4,3%), Nv.16 (1,2%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.17 (15,2%), Nv.18 (9,8%), Nv.19 (4,3%), Nv.20 (1,2%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.18 (19,9%), Nv.20 (9,8%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/meowth.asm` |

### 053 Persian

| Campo | Valor |
|---|---|
| Nome/espécie | Persian (`DEX_PERSIAN`) |
| Categoria Pokédex | Classy Cat |
| Descrição Pokédex | Although its fur has many admirers, it is tough to raise as a pet because of its fickle meanness |
| Altura | 3'03" (0,99 m) |
| Peso | 71,0 lb (32,2 kg) |
| Tipo | Normal |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 148 / Medium Fast |
| Atributos base | HP 65; Atk 70; Def 60; Spd 115; Spc 65; BST 375 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 143-235; Def 123-215; Spd 232-324; Spc 133-225 |
| Movimentos iniciais | Scratch, Growl, Bite, Screech |
| Movimentos aprendidos por nível | Nv.12 Bite; Nv.17 Pay Day; Nv.24 Screech; Nv.37 Fury Swipes; Nv.51 Slash |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM15 Hyper Beam; TM16 Pay Day; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Meowth: Persian ao atingir Nv.28 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/persian.asm` |

### 054 Psyduck

| Campo | Valor |
|---|---|
| Nome/espécie | Psyduck (`DEX_PSYDUCK`) |
| Categoria Pokédex | Duck |
| Descrição Pokédex | While lulling its enemies with its vacant look, this wily Pokémon will use psychokinetic powers |
| Altura | 2'07" (0,79 m) |
| Peso | 43,0 lb (19,5 kg) |
| Tipo | Water |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 80 / Medium Fast |
| Atributos base | HP 50; Atk 52; Def 48; Spd 55; Spc 50; BST 255 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 107-200; Def 100-192; Spd 113-205; Spc 104-196 |
| Movimentos iniciais | Scratch |
| Movimentos aprendidos por nível | Nv.28 Tail Whip; Nv.31 Disable; Nv.36 Confusion; Nv.43 Fury Swipes; Nv.52 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Golduck ao atingir Nv.33 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (5,1%)<br>Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.30 (19,9%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.28 (9,8%), Nv.30 (5,1%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (9,8%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (15,2%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.29 (9,8%), Nv.31 (5,1%)<br>Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/psyduck.asm` |

### 055 Golduck

| Campo | Valor |
|---|---|
| Nome/espécie | Golduck (`DEX_GOLDUCK`) |
| Categoria Pokédex | Duck |
| Descrição Pokédex | Often seen swimming elegantly by lake shores. It is often mistaken for the Japanese monster, Kappa |
| Altura | 5'07" (1,70 m) |
| Peso | 169,0 lb (76,7 kg) |
| Tipo | Water |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 174 / Medium Fast |
| Atributos base | HP 80; Atk 82; Def 78; Spd 85; Spc 80; BST 405 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 167-259; Def 159-251; Spd 173-265; Spc 163-255 |
| Movimentos iniciais | Scratch, Tail Whip, Disable |
| Movimentos aprendidos por nível | Nv.28 Tail Whip; Nv.31 Disable; Nv.39 Confusion; Nv.48 Fury Swipes; Nv.59 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Psyduck: Golduck ao atingir Nv.33 ou superior após ganho de nível |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.38 (1,2%) |
| Spawns em Blue | Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/golduck.asm` |

### 056 Mankey

| Campo | Valor |
|---|---|
| Nome/espécie | Mankey (`DEX_MANKEY`) |
| Categoria Pokédex | Pig Monkey |
| Descrição Pokédex | Extremely quick to anger. It could be docile one moment then thrashing away the next instant |
| Altura | 1'08" (0,51 m) |
| Peso | 62,0 lb (28,1 kg) |
| Tipo | Fighting |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 74 / Medium Fast |
| Atributos base | HP 40; Atk 80; Def 35; Spd 70; Spc 35; BST 260 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 163-255; Def 74-166; Spd 143-235; Spc 74-166 |
| Movimentos iniciais | Scratch, Leer |
| Movimentos aprendidos por nível | Nv.15 Karate Chop; Nv.21 Fury Swipes; Nv.27 Focus Energy; Nv.33 Seismic Toss; Nv.39 Thrash |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Primeape ao atingir Nv.28 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 5 - terrestre/caverna, limiar 15/256: Nv.10 (9,8%), Nv.12 (9,8%), Nv.14 (4,3%), Nv.16 (1,2%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.10 (9,8%), Nv.12 (9,8%), Nv.14 (4,3%), Nv.16 (1,2%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.17 (15,2%), Nv.18 (9,8%), Nv.19 (4,3%), Nv.20 (1,2%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.18 (19,9%), Nv.20 (9,8%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/mankey.asm` |

### 057 Primeape

| Campo | Valor |
|---|---|
| Nome/espécie | Primeape (`DEX_PRIMEAPE`) |
| Categoria Pokédex | Pig Monkey |
| Descrição Pokédex | Always furious and tenacious to boot. It will not abandon chasing its quarry until it is caught |
| Altura | 3'03" (0,99 m) |
| Peso | 71,0 lb (32,2 kg) |
| Tipo | Fighting |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 149 / Medium Fast |
| Atributos base | HP 65; Atk 105; Def 60; Spd 95; Spc 60; BST 385 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 212-304; Def 123-215; Spd 193-285; Spc 123-215 |
| Movimentos iniciais | Scratch, Leer, Karate Chop, Fury Swipes |
| Movimentos aprendidos por nível | Nv.15 Karate Chop; Nv.21 Fury Swipes; Nv.27 Focus Energy; Nv.37 Seismic Toss; Nv.46 Thrash |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Mankey: Primeape ao atingir Nv.28 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/primeape.asm` |

### 058 Growlithe

| Campo | Valor |
|---|---|
| Nome/espécie | Growlithe (`DEX_GROWLITHE`) |
| Categoria Pokédex | Puppy |
| Descrição Pokédex | Very protective of its territory. It will bark and bite to repel intruders from its space |
| Altura | 2'04" (0,71 m) |
| Peso | 42,0 lb (19,1 kg) |
| Tipo | Fire |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 91 / Slow |
| Atributos base | HP 55; Atk 70; Def 45; Spd 60; Spc 50; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 143-235; Def 94-186; Spd 123-215; Spc 104-196 |
| Movimentos iniciais | Bite, Roar |
| Movimentos aprendidos por nível | Nv.18 Ember; Nv.23 Leer; Nv.30 Take Down; Nv.39 Agility; Nv.50 Flamethrower |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM23 Dragon Rage; TM28 Dig; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Arcanine ao usar Fire Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.34 (9,8%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.32 (19,9%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.33 (19,9%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.35 (15,2%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.18 (5,1%), Nv.20 (5,1%)<br>Route 8 - terrestre/caverna, limiar 15/256: Nv.15 (4,3%), Nv.16 (9,8%), Nv.17 (5,1%), Nv.18 (1,2%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/growlithe.asm` |

### 059 Arcanine

| Campo | Valor |
|---|---|
| Nome/espécie | Arcanine (`DEX_ARCANINE`) |
| Categoria Pokédex | Legendary |
| Descrição Pokédex | A Pokémon that has been admired since the past for its beauty. It runs agilely as if on wings |
| Altura | 6'03" (1,91 m) |
| Peso | 342,0 lb (155,1 kg) |
| Tipo | Fire |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 213 / Slow |
| Atributos base | HP 90; Atk 110; Def 80; Spd 95; Spc 80; BST 455 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 222-314; Def 163-255; Spd 193-285; Spc 163-255 |
| Movimentos iniciais | Roar, Ember, Leer, Take Down |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM23 Dragon Rage; TM28 Dig; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Growlithe: Arcanine ao usar Fire Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/arcanine.asm` |

### 060 Poliwag

| Campo | Valor |
|---|---|
| Nome/espécie | Poliwag (`DEX_POLIWAG`) |
| Categoria Pokédex | Tadpole |
| Descrição Pokédex | Its newly grown legs prevent it from running. It appears to prefer swimming than trying to stand |
| Altura | 2'00" (0,61 m) |
| Peso | 27,0 lb (12,2 kg) |
| Tipo | Water |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 77 / Medium Slow |
| Atributos base | HP 40; Atk 50; Def 40; Spd 90; Spc 40; BST 260 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 104-196; Def 84-176; Spd 183-275; Spc 84-176 |
| Movimentos iniciais | Bubble |
| Movimentos aprendidos por nível | Nv.16 Hypnosis; Nv.19 Water Gun; Nv.25 Doubleslap; Nv.31 Body Slam; Nv.38 Amnesia; Nv.45 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Poliwhirl ao atingir Nv.25 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso<br>Super Rod - Pallet Town, Viridian City, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Route 22, Nv.15; 25,0% por uso (50% sem fisgada) |
| Spawns em Blue | Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso<br>Super Rod - Pallet Town, Viridian City, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Route 22, Nv.15; 25,0% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/poliwag.asm` |

### 061 Poliwhirl

| Campo | Valor |
|---|---|
| Nome/espécie | Poliwhirl (`DEX_POLIWHIRL`) |
| Categoria Pokédex | Tadpole |
| Descrição Pokédex | Capable of living in or out of water. When out of water, it sweats to keep its body slimy |
| Altura | 3'03" (0,99 m) |
| Peso | 44,0 lb (20,0 kg) |
| Tipo | Water |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 131 / Medium Slow |
| Atributos base | HP 65; Atk 65; Def 65; Spd 90; Spc 50; BST 335 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 133-225; Def 133-225; Spd 183-275; Spc 104-196 |
| Movimentos iniciais | Bubble, Hypnosis, Water Gun |
| Movimentos aprendidos por nível | Nv.16 Hypnosis; Nv.19 Water Gun; Nv.26 Doubleslap; Nv.33 Body Slam; Nv.41 Amnesia; Nv.49 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Poliwrath ao usar Water Stone; nível mínimo 1 |
| Origem por evolução | Poliwag: Poliwhirl ao atingir Nv.25 ou superior após ganho de nível |
| Spawns em Red | Super Rod - Celadon City, Route 10, Nv.23; 25,0% por uso (50% sem fisgada) |
| Spawns em Blue | Super Rod - Celadon City, Route 10, Nv.23; 25,0% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/poliwhirl.asm` |

### 062 Poliwrath

| Campo | Valor |
|---|---|
| Nome/espécie | Poliwrath (`DEX_POLIWRATH`) |
| Categoria Pokédex | Tadpole |
| Descrição Pokédex | An adept swimmer at both the front crawl and breast stroke. Easily overtakes the best human swimmers |
| Altura | 4'03" (1,30 m) |
| Peso | 119,0 lb (54,0 kg) |
| Tipo | Water / Fighting |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 185 / Medium Slow |
| Atributos base | HP 90; Atk 85; Def 95; Spd 70; Spc 70; BST 410 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 173-265; Def 193-285; Spd 143-235; Spc 143-235 |
| Movimentos iniciais | Hypnosis, Water Gun, Doubleslap, Body Slam |
| Movimentos aprendidos por nível | Nv.16 Hypnosis; Nv.19 Water Gun |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Poliwhirl: Poliwrath ao usar Water Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/poliwrath.asm` |

### 063 Abra

| Campo | Valor |
|---|---|
| Nome/espécie | Abra (`DEX_ABRA`) |
| Categoria Pokédex | Psi |
| Descrição Pokédex | Using its ability to read minds, it will identify impending danger and TELEPORT to safety |
| Altura | 2'11" (0,89 m) |
| Peso | 43,0 lb (19,5 kg) |
| Tipo | Psychic |
| Catch rate | 200; cenário normalizado: 26,38% (favorável) |
| EXP base / crescimento | 73 / Medium Slow |
| Atributos base | HP 25; Atk 20; Def 15; Spd 90; Spc 105; BST 255 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 158-250; Atk 44-136; Def 34-126; Spd 183-275; Spc 212-304 |
| Movimentos iniciais | Teleport |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Kadabra ao atingir Nv.16 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 24 - terrestre/caverna, limiar 25/256: Nv.8 (4,3%), Nv.10 (9,8%), Nv.12 (1,2%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.10 (5,1%), Nv.12 (9,8%) |
| Spawns em Blue | Route 24 - terrestre/caverna, limiar 25/256: Nv.8 (4,3%), Nv.10 (9,8%), Nv.12 (1,2%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.10 (5,1%), Nv.12 (9,8%) |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.9, por 180 moedas |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.6, por 120 moedas |
| Fonte específica | `data/pokemon/base_stats/abra.asm` |

### 064 Kadabra

| Campo | Valor |
|---|---|
| Nome/espécie | Kadabra (`DEX_KADABRA`) |
| Categoria Pokédex | Psi |
| Descrição Pokédex | It emits special alpha waves from its body that induce headaches just by being close by |
| Altura | 4'03" (1,30 m) |
| Peso | 125,0 lb (56,7 kg) |
| Tipo | Psychic |
| Catch rate | 100; cenário normalizado: 13,25% (intermediária) |
| EXP base / crescimento | 145 / Medium Slow |
| Atributos base | HP 40; Atk 35; Def 30; Spd 105; Spc 120; BST 330 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 74-166; Def 64-156; Spd 212-304; Spc 242-334 |
| Movimentos iniciais | Teleport, Confusion, Disable |
| Movimentos aprendidos por nível | Nv.16 Confusion; Nv.20 Disable; Nv.27 Psybeam; Nv.31 Recover; Nv.38 Psychic; Nv.42 Reflect |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Alakazam por troca via link; nível mínimo 1 |
| Origem por evolução | Abra: Kadabra ao atingir Nv.16 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (5,1%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (15,2%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (5,1%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (15,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/kadabra.asm` |

### 065 Alakazam

| Campo | Valor |
|---|---|
| Nome/espécie | Alakazam (`DEX_ALAKAZAM`) |
| Categoria Pokédex | Psi |
| Descrição Pokédex | Its brain can outperform a supercomputer. Its intelligence quotient is said to be 5,000 |
| Altura | 4'11" (1,50 m) |
| Peso | 106,0 lb (48,1 kg) |
| Tipo | Psychic |
| Catch rate | 50; cenário normalizado: 6,69% (difícil) |
| EXP base / crescimento | 186 / Medium Slow |
| Atributos base | HP 55; Atk 50; Def 45; Spd 120; Spc 135; BST 405 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 104-196; Def 94-186; Spd 242-334; Spc 272-364 |
| Movimentos iniciais | Teleport, Confusion, Disable |
| Movimentos aprendidos por nível | Nv.16 Confusion; Nv.20 Disable; Nv.27 Psybeam; Nv.31 Recover; Nv.38 Psychic; Nv.42 Reflect |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM28 Dig; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Kadabra: Alakazam por troca via link; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/alakazam.asm` |

### 066 Machop

| Campo | Valor |
|---|---|
| Nome/espécie | Machop (`DEX_MACHOP`) |
| Categoria Pokédex | Superpower |
| Descrição Pokédex | Loves to build its muscles. It trains in all styles of martial arts to become even stronger |
| Altura | 2'07" (0,79 m) |
| Peso | 43,0 lb (19,5 kg) |
| Tipo | Fighting |
| Catch rate | 180; cenário normalizado: 23,75% (favorável) |
| EXP base / crescimento | 88 / Medium Slow |
| Atributos base | HP 70; Atk 80; Def 50; Spd 35; Spc 35; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 163-255; Def 104-196; Spd 74-166; Spc 74-166 |
| Movimentos iniciais | Karate Chop |
| Movimentos aprendidos por nível | Nv.20 Low Kick; Nv.25 Leer; Nv.32 Focus Energy; Nv.39 Seismic Toss; Nv.46 Submission |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Machoke ao atingir Nv.28 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.15 (9,8%), Nv.17 (5,1%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.15 (9,8%), Nv.17 (5,1%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.24 (19,9%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.22 (19,9%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.24 (19,9%) |
| Spawns em Blue | Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.15 (9,8%), Nv.17 (5,1%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.15 (9,8%), Nv.17 (5,1%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.24 (19,9%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.22 (19,9%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.24 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/machop.asm` |

### 067 Machoke

| Campo | Valor |
|---|---|
| Nome/espécie | Machoke (`DEX_MACHOKE`) |
| Categoria Pokédex | Superpower |
| Descrição Pokédex | Its muscular body is so powerful, it must wear a power save belt to be able to regulate its motions |
| Altura | 4'11" (1,50 m) |
| Peso | 155,0 lb (70,3 kg) |
| Tipo | Fighting |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 146 / Medium Slow |
| Atributos base | HP 80; Atk 100; Def 70; Spd 45; Spc 50; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 203-295; Def 143-235; Spd 94-186; Spc 104-196 |
| Movimentos iniciais | Karate Chop, Low Kick, Leer |
| Movimentos aprendidos por nível | Nv.20 Low Kick; Nv.25 Leer; Nv.36 Focus Energy; Nv.44 Seismic Toss; Nv.52 Submission |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Machamp por troca via link; nível mínimo 1 |
| Origem por evolução | Machop: Machoke ao atingir Nv.28 ou superior após ganho de nível |
| Spawns em Red | Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.42 (4,3%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.41 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.42 (4,3%), Nv.45 (1,2%) |
| Spawns em Blue | Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.42 (4,3%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.41 (5,1%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.42 (4,3%), Nv.45 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/machoke.asm` |

### 068 Machamp

| Campo | Valor |
|---|---|
| Nome/espécie | Machamp (`DEX_MACHAMP`) |
| Categoria Pokédex | Superpower |
| Descrição Pokédex | Using its heavy muscles, it throws powerful punches that can send the victim clear over the horizon |
| Altura | 5'03" (1,60 m) |
| Peso | 287,0 lb (130,2 kg) |
| Tipo | Fighting |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 193 / Medium Slow |
| Atributos base | HP 90; Atk 130; Def 80; Spd 55; Spc 65; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 262-354; Def 163-255; Spd 113-205; Spc 133-225 |
| Movimentos iniciais | Karate Chop, Low Kick, Leer |
| Movimentos aprendidos por nível | Nv.20 Low Kick; Nv.25 Leer; Nv.36 Focus Energy; Nv.44 Seismic Toss; Nv.52 Submission |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Machoke: Machamp por troca via link; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/machamp.asm` |

### 069 Bellsprout

| Campo | Valor |
|---|---|
| Nome/espécie | Bellsprout (`DEX_BELLSPROUT`) |
| Categoria Pokédex | Flower |
| Descrição Pokédex | A carnivorous Pokémon that traps and eats bugs. It uses its root feet to soak up needed moisture |
| Altura | 2'04" (0,71 m) |
| Peso | 9,0 lb (4,1 kg) |
| Tipo | Grass / Poison |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 84 / Medium Slow |
| Atributos base | HP 50; Atk 75; Def 35; Spd 40; Spc 70; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 153-245; Def 74-166; Spd 84-176; Spc 143-235 |
| Movimentos iniciais | Vine Whip, Growth |
| Movimentos aprendidos por nível | Nv.13 Wrap; Nv.15 Poisonpowder; Nv.18 Sleep Powder; Nv.21 Stun Spore; Nv.26 Acid; Nv.33 Razor Leaf; Nv.42 Slam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Weepinbell ao atingir Nv.21 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Route 12 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.22 (9,8%), Nv.24 (19,9%), Nv.26 (5,1%)<br>Route 24 - terrestre/caverna, limiar 25/256: Nv.12 (9,8%), Nv.13 (9,8%), Nv.14 (5,1%)<br>Route 25 - terrestre/caverna, limiar 15/256: Nv.12 (9,8%), Nv.13 (9,8%), Nv.14 (5,1%)<br>Route 5 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (9,8%), Nv.16 (5,1%)<br>Route 6 - terrestre/caverna, limiar 15/256: Nv.13 (19,9%), Nv.15 (9,8%), Nv.16 (5,1%)<br>Route 7 - terrestre/caverna, limiar 15/256: Nv.19 (19,9%), Nv.22 (9,8%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/bellsprout.asm` |

### 070 Weepinbell

| Campo | Valor |
|---|---|
| Nome/espécie | Weepinbell (`DEX_WEEPINBELL`) |
| Categoria Pokédex | Flycatcher |
| Descrição Pokédex | It spits out POISONPOWDER to immobilize the enemy and then finishes it with a spray of ACID |
| Altura | 3'03" (0,99 m) |
| Peso | 14,0 lb (6,4 kg) |
| Tipo | Grass / Poison |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 151 / Medium Slow |
| Atributos base | HP 65; Atk 90; Def 50; Spd 55; Spc 85; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 183-275; Def 104-196; Spd 113-205; Spc 173-265 |
| Movimentos iniciais | Vine Whip, Growth, Wrap |
| Movimentos aprendidos por nível | Nv.13 Wrap; Nv.15 Poisonpowder; Nv.18 Sleep Powder; Nv.23 Stun Spore; Nv.29 Acid; Nv.38 Razor Leaf; Nv.49 Slam |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Victreebel ao usar Leaf Stone; nível mínimo 1 |
| Origem por evolução | Bellsprout: Weepinbell ao atingir Nv.21 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Route 12 - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.28 (4,3%), Nv.30 (1,2%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.30 (5,1%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.30 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/weepinbell.asm` |

### 071 Victreebel

| Campo | Valor |
|---|---|
| Nome/espécie | Victreebel (`DEX_VICTREEBEL`) |
| Categoria Pokédex | Flycatcher |
| Descrição Pokédex | Said to live in huge colonies deep in jungles, although no one has ever returned from there |
| Altura | 5'07" (1,70 m) |
| Peso | 34,0 lb (15,4 kg) |
| Tipo | Grass / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 191 / Medium Slow |
| Atributos base | HP 80; Atk 105; Def 65; Spd 70; Spc 100; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 212-304; Def 133-225; Spd 143-235; Spc 203-295 |
| Movimentos iniciais | Sleep Powder, Stun Spore, Acid, Razor Leaf |
| Movimentos aprendidos por nível | Nv.13 Wrap; Nv.15 Poisonpowder; Nv.18 Sleep Powder |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Weepinbell: Victreebel ao usar Leaf Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/victreebel.asm` |

### 072 Tentacool

| Campo | Valor |
|---|---|
| Nome/espécie | Tentacool (`DEX_TENTACOOL`) |
| Categoria Pokédex | Jellyfish |
| Descrição Pokédex | Drifts in shallow seas. Anglers who hook them by accident are often punished by its stinging acid |
| Altura | 2'11" (0,89 m) |
| Peso | 100,0 lb (45,4 kg) |
| Tipo | Water / Poison |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 105 / Slow |
| Atributos base | HP 40; Atk 40; Def 35; Spd 70; Spc 100; BST 285 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 84-176; Def 74-166; Spd 143-235; Spc 203-295 |
| Movimentos iniciais | Acid |
| Movimentos aprendidos por nível | Nv.7 Supersonic; Nv.13 Wrap; Nv.18 Poison Sting; Nv.22 Water Gun; Nv.27 Constrict; Nv.33 Barrier; Nv.40 Screech; Nv.48 Hydro Pump |
| Movimentos possíveis por TM/HM | HM01 Cut; HM03 Surf; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM21 Mega Drain; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Tentacruel ao atingir Nv.30 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 21 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Route 19 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Route 20 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Super Rod - Pallet Town, Viridian City, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.5; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Route 21 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Route 19 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Route 20 - Surf, limiar 5/256: Nv.5 (29,7%), Nv.10 (29,7%), Nv.15 (25,0%), Nv.20 (5,1%), Nv.30 (5,1%), Nv.35 (4,3%), Nv.40 (1,2%)<br>Super Rod - Pallet Town, Viridian City, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.5; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/tentacool.asm` |

### 073 Tentacruel

| Campo | Valor |
|---|---|
| Nome/espécie | Tentacruel (`DEX_TENTACRUEL`) |
| Categoria Pokédex | Jellyfish |
| Descrição Pokédex | The tentacles are normally kept short. On hunts, they are extended to ensnare and immobilize prey |
| Altura | 5'03" (1,60 m) |
| Peso | 121,0 lb (54,9 kg) |
| Tipo | Water / Poison |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 205 / Slow |
| Atributos base | HP 80; Atk 70; Def 65; Spd 100; Spc 120; BST 435 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 143-235; Def 133-225; Spd 203-295; Spc 242-334 |
| Movimentos iniciais | Acid, Supersonic, Wrap |
| Movimentos aprendidos por nível | Nv.7 Supersonic; Nv.13 Wrap; Nv.18 Poison Sting; Nv.22 Water Gun; Nv.27 Constrict; Nv.35 Barrier; Nv.43 Screech; Nv.50 Hydro Pump |
| Movimentos possíveis por TM/HM | HM01 Cut; HM03 Surf; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Tentacool: Tentacruel ao atingir Nv.30 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/tentacruel.asm` |

### 074 Geodude

| Campo | Valor |
|---|---|
| Nome/espécie | Geodude (`DEX_GEODUDE`) |
| Categoria Pokédex | Rock |
| Descrição Pokédex | Found in fields and mountains. Mistaking them for boulders, people often step or trip on them |
| Altura | 1'04" (0,41 m) |
| Peso | 44,0 lb (20,0 kg) |
| Tipo | Rock / Ground |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 86 / Medium Slow |
| Atributos base | HP 40; Atk 80; Def 100; Spd 20; Spc 30; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 163-255; Def 203-295; Spd 44-136; Spc 64-156 |
| Movimentos iniciais | Tackle |
| Movimentos aprendidos por nível | Nv.11 Defense Curl; Nv.16 Rock Throw; Nv.21 Selfdestruct; Nv.26 Harden; Nv.31 Earthquake; Nv.36 Explosion |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Graveler ao atingir Nv.25 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (9,8%), Nv.10 (5,1%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.7 (15,2%), Nv.8 (9,8%), Nv.9 (1,2%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.9 (19,9%), Nv.10 (9,8%)<br>Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.16 (9,8%), Nv.17 (15,2%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.16 (9,8%), Nv.17 (15,2%), Nv.18 (1,2%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.24 (19,9%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.26 (19,9%) |
| Spawns em Blue | Mt. Moon 1F - terrestre/caverna, limiar 10/256: Nv.8 (9,8%), Nv.10 (5,1%)<br>Mt. Moon B1F - terrestre/caverna, limiar 10/256: Nv.7 (15,2%), Nv.8 (9,8%), Nv.9 (1,2%)<br>Mt. Moon B2F - terrestre/caverna, limiar 10/256: Nv.9 (19,9%), Nv.10 (9,8%)<br>Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.16 (9,8%), Nv.17 (15,2%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.16 (9,8%), Nv.17 (15,2%), Nv.18 (1,2%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.24 (19,9%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.26 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/geodude.asm` |

### 075 Graveler

| Campo | Valor |
|---|---|
| Nome/espécie | Graveler (`DEX_GRAVELER`) |
| Categoria Pokédex | Rock |
| Descrição Pokédex | Rolls down slopes to move. It rolls over any obstacle without slowing or changing its direction |
| Altura | 3'03" (0,99 m) |
| Peso | 232,0 lb (105,2 kg) |
| Tipo | Rock / Ground |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 134 / Medium Slow |
| Atributos base | HP 55; Atk 95; Def 115; Spd 35; Spc 45; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 193-285; Def 232-324; Spd 74-166; Spc 94-186 |
| Movimentos iniciais | Tackle, Defense Curl |
| Movimentos aprendidos por nível | Nv.11 Defense Curl; Nv.16 Rock Throw; Nv.21 Selfdestruct; Nv.29 Harden; Nv.36 Earthquake; Nv.43 Explosion |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Golem por troca via link; nível mínimo 1 |
| Origem por evolução | Geodude: Graveler ao atingir Nv.25 ou superior após ganho de nível |
| Spawns em Red | Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.43 (1,2%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.43 (5,1%) |
| Spawns em Blue | Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.41 (5,1%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.43 (1,2%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.43 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/graveler.asm` |

### 076 Golem

| Campo | Valor |
|---|---|
| Nome/espécie | Golem (`DEX_GOLEM`) |
| Categoria Pokédex | Megaton |
| Descrição Pokédex | Its boulder-like body is extremely hard. It can easily withstand dynamite blasts without damage |
| Altura | 4'07" (1,40 m) |
| Peso | 662,0 lb (300,3 kg) |
| Tipo | Rock / Ground |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 177 / Medium Slow |
| Atributos base | HP 80; Atk 110; Def 130; Spd 45; Spc 55; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 222-314; Def 262-354; Spd 94-186; Spc 113-205 |
| Movimentos iniciais | Tackle, Defense Curl |
| Movimentos aprendidos por nível | Nv.11 Defense Curl; Nv.16 Rock Throw; Nv.21 Selfdestruct; Nv.29 Harden; Nv.36 Earthquake; Nv.43 Explosion |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Graveler: Golem por troca via link; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/golem.asm` |

### 077 Ponyta

| Campo | Valor |
|---|---|
| Nome/espécie | Ponyta (`DEX_PONYTA`) |
| Categoria Pokédex | Fire Horse |
| Descrição Pokédex | Its hooves are 10 times harder than diamonds. It can trample anything completely flat in little time |
| Altura | 3'03" (0,99 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Fire |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 152 / Medium Fast |
| Atributos base | HP 50; Atk 85; Def 55; Spd 90; Spc 65; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 173-265; Def 113-205; Spd 183-275; Spc 133-225 |
| Movimentos iniciais | Ember |
| Movimentos aprendidos por nível | Nv.30 Tail Whip; Nv.32 Stomp; Nv.35 Growl; Nv.39 Fire Spin; Nv.43 Take Down; Nv.48 Agility |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Rapidash ao atingir Nv.40 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%), Nv.32 (9,8%), Nv.34 (15,2%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%), Nv.32 (9,8%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.32 (9,8%), Nv.34 (9,8%), Nv.36 (4,3%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.32 (9,8%), Nv.34 (5,1%) |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%), Nv.32 (9,8%), Nv.34 (15,2%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%), Nv.32 (9,8%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.32 (9,8%), Nv.36 (4,3%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.32 (9,8%), Nv.34 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/ponyta.asm` |

### 078 Rapidash

| Campo | Valor |
|---|---|
| Nome/espécie | Rapidash (`DEX_RAPIDASH`) |
| Categoria Pokédex | Fire Horse |
| Descrição Pokédex | Very competitive, this Pokémon will chase anything that moves fast in the hopes of racing it |
| Altura | 5'07" (1,70 m) |
| Peso | 209,0 lb (94,8 kg) |
| Tipo | Fire |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 192 / Medium Fast |
| Atributos base | HP 65; Atk 100; Def 70; Spd 105; Spc 80; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 203-295; Def 143-235; Spd 212-304; Spc 163-255 |
| Movimentos iniciais | Ember, Tail Whip, Stomp, Growl |
| Movimentos aprendidos por nível | Nv.30 Tail Whip; Nv.32 Stomp; Nv.35 Growl; Nv.39 Fire Spin; Nv.47 Take Down; Nv.55 Agility |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Ponyta: Rapidash ao atingir Nv.40 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/rapidash.asm` |

### 079 Slowpoke

| Campo | Valor |
|---|---|
| Nome/espécie | Slowpoke (`DEX_SLOWPOKE`) |
| Categoria Pokédex | Dopey |
| Descrição Pokédex | Incredibly slow and dopey. It takes 5 seconds for it to feel pain when under attack |
| Altura | 3'11" (1,19 m) |
| Peso | 79,0 lb (35,8 kg) |
| Tipo | Water / Psychic |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 99 / Medium Fast |
| Atributos base | HP 90; Atk 65; Def 65; Spd 15; Spc 40; BST 275 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 133-225; Def 133-225; Spd 34-126; Spc 84-176 |
| Movimentos iniciais | Confusion |
| Movimentos aprendidos por nível | Nv.18 Disable; Nv.22 Headbutt; Nv.27 Growl; Nv.33 Water Gun; Nv.40 Amnesia; Nv.48 Psychic |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; HM05 Flash; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM16 Pay Day; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Slowbro ao atingir Nv.37 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.30 (19,9%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.28 (9,8%), Nv.30 (5,1%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (9,8%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (15,2%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.29 (9,8%), Nv.31 (5,1%)<br>Super Rod - Celadon City, Route 10, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (5,1%)<br>Super Rod - Celadon City, Route 10, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/slowpoke.asm` |

### 080 Slowbro

| Campo | Valor |
|---|---|
| Nome/espécie | Slowbro (`DEX_SLOWBRO`) |
| Categoria Pokédex | Hermitcrab |
| Descrição Pokédex | The SHELLDER that is latched onto SLOWPOKE's tail is said to feed on the host's left over scraps |
| Altura | 5'03" (1,60 m) |
| Peso | 173,0 lb (78,5 kg) |
| Tipo | Water / Psychic |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 164 / Medium Fast |
| Atributos base | HP 95; Atk 75; Def 110; Spd 30; Spc 80; BST 390 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 297-389; Atk 153-245; Def 222-314; Spd 64-156; Spc 163-255 |
| Movimentos iniciais | Confusion, Disable, Headbutt |
| Movimentos aprendidos por nível | Nv.18 Disable; Nv.22 Headbutt; Nv.27 Growl; Nv.33 Water Gun; Nv.37 Withdraw; Nv.44 Amnesia; Nv.55 Psychic |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Slowpoke: Slowbro ao atingir Nv.37 ou superior após ganho de nível |
| Spawns em Red | Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%)<br>Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.38 (1,2%)<br>Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/slowbro.asm` |

### 081 Magnemite

| Campo | Valor |
|---|---|
| Nome/espécie | Magnemite (`DEX_MAGNEMITE`) |
| Categoria Pokédex | Magnet |
| Descrição Pokédex | Uses anti-gravity to stay suspended. Appears without warning and uses THUNDER WAVE and similar moves |
| Altura | 1'00" (0,30 m) |
| Peso | 13,0 lb (5,9 kg) |
| Tipo | Electric |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 89 / Medium Fast |
| Atributos base | HP 25; Atk 35; Def 70; Spd 45; Spc 95; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 158-250; Atk 74-166; Def 143-235; Spd 94-186; Spc 193-285 |
| Movimentos iniciais | Tackle |
| Movimentos aprendidos por nível | Nv.21 Sonicboom; Nv.25 Thundershock; Nv.29 Supersonic; Nv.35 Thunder Wave; Nv.41 Swift; Nv.47 Screech |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Magneton ao atingir Nv.30 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Power Plant - terrestre/caverna, limiar 10/256: Nv.21 (19,9%), Nv.23 (9,8%) |
| Spawns em Blue | Power Plant - terrestre/caverna, limiar 10/256: Nv.21 (19,9%), Nv.23 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/magnemite.asm` |

### 082 Magneton

| Campo | Valor |
|---|---|
| Nome/espécie | Magneton (`DEX_MAGNETON`) |
| Categoria Pokédex | Magnet |
| Descrição Pokédex | Formed by several MAGNEMITEs linked together. They frequently appear when sunspots flare up |
| Altura | 3'03" (0,99 m) |
| Peso | 132,0 lb (59,9 kg) |
| Tipo | Electric |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 161 / Medium Fast |
| Atributos base | HP 50; Atk 60; Def 95; Spd 70; Spc 120; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 123-215; Def 193-285; Spd 143-235; Spc 242-334 |
| Movimentos iniciais | Tackle, Sonicboom, Thundershock |
| Movimentos aprendidos por nível | Nv.21 Sonicboom; Nv.25 Thundershock; Nv.29 Supersonic; Nv.38 Thunder Wave; Nv.46 Swift; Nv.54 Screech |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Magnemite: Magneton ao atingir Nv.30 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (15,2%)<br>Power Plant - terrestre/caverna, limiar 10/256: Nv.32 (5,1%), Nv.35 (5,1%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (15,2%)<br>Power Plant - terrestre/caverna, limiar 10/256: Nv.32 (5,1%), Nv.35 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/magneton.asm` |

### 083 Farfetch'd

| Campo | Valor |
|---|---|
| Nome/espécie | Farfetch'd (`DEX_FARFETCHD`) |
| Categoria Pokédex | Wild Duck |
| Descrição Pokédex | The sprig of green onions it holds is its weapon. It is used much like a metal sword |
| Altura | 2'07" (0,79 m) |
| Peso | 33,0 lb (15,0 kg) |
| Tipo | Normal / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 94 / Medium Fast |
| Atributos base | HP 52; Atk 65; Def 55; Spd 60; Spc 58; BST 290 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 211-304; Atk 133-225; Def 113-205; Spd 123-215; Spc 119-211 |
| Movimentos iniciais | Peck, Sand-Attack |
| Movimentos aprendidos por nível | Nv.7 Leer; Nv.15 Fury Attack; Nv.23 Swords Dance; Nv.31 Agility; Nv.39 Slash |
| Movimentos possíveis por TM/HM | HM01 Cut; HM02 Fly; TM02 Razor Wind; TM03 Swords Dance; TM04 Whirlwind; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Troca NPC em Vermilion Trade House: entregar Spearow; recebido no mesmo nível, apelido DUX |
| Aquisição especial em Blue | Troca NPC em Vermilion Trade House: entregar Spearow; recebido no mesmo nível, apelido DUX |
| Fonte específica | `data/pokemon/base_stats/farfetchd.asm` |

### 084 Doduo

| Campo | Valor |
|---|---|
| Nome/espécie | Doduo (`DEX_DODUO`) |
| Categoria Pokédex | Twin Bird |
| Descrição Pokédex | A bird that makes up for its poor flying with its fast foot speed. Leaves giant footprints |
| Altura | 4'07" (1,40 m) |
| Peso | 86,0 lb (39,0 kg) |
| Tipo | Normal / Flying |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 96 / Medium Fast |
| Atributos base | HP 35; Atk 85; Def 45; Spd 75; Spc 35; BST 275 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 173-265; Def 94-186; Spd 153-245; Spc 74-166 |
| Movimentos iniciais | Peck |
| Movimentos aprendidos por nível | Nv.20 Growl; Nv.24 Fury Attack; Nv.30 Drill Peck; Nv.36 Rage; Nv.40 Tri Attack; Nv.44 Agility |
| Movimentos possíveis por TM/HM | HM02 Fly; TM04 Whirlwind; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM43 Sky Attack; TM44 Rest; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Dodrio ao atingir Nv.31 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 16 - terrestre/caverna, limiar 25/256: Nv.18 (9,8%), Nv.20 (9,8%), Nv.22 (5,1%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.24 (9,8%), Nv.26 (9,8%), Nv.28 (5,1%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.24 (9,8%), Nv.26 (9,8%), Nv.28 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.26 (19,9%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.26 (19,9%) |
| Spawns em Blue | Route 16 - terrestre/caverna, limiar 25/256: Nv.18 (9,8%), Nv.20 (9,8%), Nv.22 (5,1%)<br>Route 17 - terrestre/caverna, limiar 25/256: Nv.24 (9,8%), Nv.26 (9,8%), Nv.28 (5,1%)<br>Route 18 - terrestre/caverna, limiar 25/256: Nv.24 (9,8%), Nv.26 (9,8%), Nv.28 (5,1%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.26 (19,9%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.26 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/doduo.asm` |

### 085 Dodrio

| Campo | Valor |
|---|---|
| Nome/espécie | Dodrio (`DEX_DODRIO`) |
| Categoria Pokédex | Triplebird |
| Descrição Pokédex | Uses its three brains to execute complex plans. While two heads sleep, one head stays awake |
| Altura | 5'11" (1,80 m) |
| Peso | 188,0 lb (85,3 kg) |
| Tipo | Normal / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 158 / Medium Fast |
| Atributos base | HP 60; Atk 110; Def 70; Spd 100; Spc 60; BST 400 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 222-314; Def 143-235; Spd 203-295; Spc 123-215 |
| Movimentos iniciais | Peck, Growl, Fury Attack |
| Movimentos aprendidos por nível | Nv.20 Growl; Nv.24 Fury Attack; Nv.30 Drill Peck; Nv.39 Rage; Nv.45 Tri Attack; Nv.51 Agility |
| Movimentos possíveis por TM/HM | HM02 Fly; TM04 Whirlwind; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM43 Sky Attack; TM44 Rest; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Doduo: Dodrio ao atingir Nv.31 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (9,8%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (19,9%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.49 (9,8%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.51 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/dodrio.asm` |

### 086 Seel

| Campo | Valor |
|---|---|
| Nome/espécie | Seel (`DEX_SEEL`) |
| Categoria Pokédex | Sea Lion |
| Descrição Pokédex | The protruding horn on its head is very hard. It is used for bashing through thick ice |
| Altura | 3'07" (1,09 m) |
| Peso | 198,0 lb (89,8 kg) |
| Tipo | Water |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 100 / Medium Fast |
| Atributos base | HP 65; Atk 45; Def 55; Spd 45; Spc 70; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 94-186; Def 113-205; Spd 94-186; Spc 143-235 |
| Movimentos iniciais | Headbutt |
| Movimentos aprendidos por nível | Nv.30 Growl; Nv.35 Aurora Beam; Nv.40 Rest; Nv.45 Take Down; Nv.50 Ice Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM16 Pay Day; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Dewgong ao atingir Nv.34 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.30 (19,9%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (15,2%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (9,8%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.29 (5,1%), Nv.31 (9,8%) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.30 (19,9%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%), Nv.30 (9,8%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (15,2%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (9,8%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.29 (5,1%), Nv.31 (9,8%) |
| Aquisição especial em Red | Troca NPC em Cinnabar Lab Fossil Room: entregar Ponyta; recebido no mesmo nível, apelido SAILOR |
| Aquisição especial em Blue | Troca NPC em Cinnabar Lab Fossil Room: entregar Ponyta; recebido no mesmo nível, apelido SAILOR |
| Fonte específica | `data/pokemon/base_stats/seel.asm` |

### 087 Dewgong

| Campo | Valor |
|---|---|
| Nome/espécie | Dewgong (`DEX_DEWGONG`) |
| Categoria Pokédex | Sea Lion |
| Descrição Pokédex | Stores thermal energy in its body. Swims at a steady 8 knots even in intensely cold waters |
| Altura | 5'07" (1,70 m) |
| Peso | 265,0 lb (120,2 kg) |
| Tipo | Water / Ice |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 176 / Medium Fast |
| Atributos base | HP 90; Atk 70; Def 80; Spd 70; Spc 95; BST 405 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 143-235; Def 163-255; Spd 143-235; Spc 193-285 |
| Movimentos iniciais | Headbutt, Growl, Aurora Beam |
| Movimentos aprendidos por nível | Nv.30 Growl; Nv.35 Aurora Beam; Nv.44 Rest; Nv.50 Take Down; Nv.56 Ice Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Seel: Dewgong ao atingir Nv.34 ou superior após ganho de nível |
| Spawns em Red | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.38 (4,3%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%) |
| Spawns em Blue | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.38 (4,3%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/dewgong.asm` |

### 088 Grimer

| Campo | Valor |
|---|---|
| Nome/espécie | Grimer (`DEX_GRIMER`) |
| Categoria Pokédex | Sludge |
| Descrição Pokédex | Appears in filthy areas. Thrives by sucking up polluted sludge that is pumped out of factories |
| Altura | 2'11" (0,89 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Poison |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 90 / Medium Fast |
| Atributos base | HP 80; Atk 80; Def 50; Spd 25; Spc 40; BST 275 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 163-255; Def 104-196; Spd 54-146; Spc 84-176 |
| Movimentos iniciais | Pound, Disable |
| Movimentos aprendidos por nível | Nv.30 Poison Gas; Nv.33 Minimize; Nv.37 Sludge; Nv.42 Harden; Nv.48 Screech; Nv.55 Acid Armor |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM20 Rage; TM21 Mega Drain; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Muk ao atingir Nv.38 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.30 (5,1%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.30 (5,1%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.34 (5,1%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.35 (5,1%) |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (19,9%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.30 (9,8%), Nv.34 (35,2%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.35 (15,2%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.31 (29,7%), Nv.33 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/grimer.asm` |

### 089 Muk

| Campo | Valor |
|---|---|
| Nome/espécie | Muk (`DEX_MUK`) |
| Categoria Pokédex | Sludge |
| Descrição Pokédex | Thickly covered with a filthy, vile sludge. It is so toxic, even its footprints contain poison |
| Altura | 3'11" (1,19 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Poison |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 157 / Medium Fast |
| Atributos base | HP 105; Atk 105; Def 75; Spd 50; Spc 65; BST 400 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 316-408; Atk 212-304; Def 153-245; Spd 104-196; Spc 133-225 |
| Movimentos iniciais | Pound, Disable, Poison Gas |
| Movimentos aprendidos por nível | Nv.30 Poison Gas; Nv.33 Minimize; Nv.37 Sludge; Nv.45 Harden; Nv.53 Screech; Nv.60 Acid Armor |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Grimer: Muk ao atingir Nv.38 ou superior após ganho de nível |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.39 (1,2%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.42 (1,2%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.42 (1,2%) |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.37 (4,3%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.38 (5,1%), Nv.40 (9,8%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.40 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/muk.asm` |

### 090 Shellder

| Campo | Valor |
|---|---|
| Nome/espécie | Shellder (`DEX_SHELLDER`) |
| Categoria Pokédex | Bivalve |
| Descrição Pokédex | Its hard shell repels any kind of attack. It is vulnerable only when its shell is open |
| Altura | 1'00" (0,30 m) |
| Peso | 9,0 lb (4,1 kg) |
| Tipo | Water |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 97 / Slow |
| Atributos base | HP 30; Atk 65; Def 100; Spd 40; Spc 45; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 133-225; Def 203-295; Spd 84-176; Spc 94-186 |
| Movimentos iniciais | Tackle, Withdraw |
| Movimentos aprendidos por nível | Nv.18 Supersonic; Nv.23 Clamp; Nv.30 Aurora Beam; Nv.39 Leer; Nv.50 Ice Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM39 Swift; TM44 Rest; TM47 Explosion; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Cloyster ao usar Water Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (15,2%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.32 (15,2%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.29 (5,1%), Nv.31 (9,8%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (9,8%)<br>Super Rod - Vermilion City, Route 6, Route 11, Vermilion Dock, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (9,8%)<br>Super Rod - Vermilion City, Route 6, Route 11, Vermilion Dock, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/shellder.asm` |

### 091 Cloyster

| Campo | Valor |
|---|---|
| Nome/espécie | Cloyster (`DEX_CLOYSTER`) |
| Categoria Pokédex | Bivalve |
| Descrição Pokédex | When attacked, it launches its horns in quick volleys. Its innards have never been seen |
| Altura | 4'11" (1,50 m) |
| Peso | 292,0 lb (132,4 kg) |
| Tipo | Water / Ice |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 203 / Slow |
| Atributos base | HP 50; Atk 95; Def 180; Spd 70; Spc 85; BST 480 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 193-285; Def 361-453; Spd 143-235; Spc 173-265 |
| Movimentos iniciais | Withdraw, Supersonic, Clamp, Aurora Beam |
| Movimentos aprendidos por nível | Nv.50 Spike Cannon |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM39 Swift; TM44 Rest; TM47 Explosion; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Shellder: Cloyster ao usar Water Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/cloyster.asm` |

### 092 Gastly

| Campo | Valor |
|---|---|
| Nome/espécie | Gastly (`DEX_GASTLY`) |
| Categoria Pokédex | Gas |
| Descrição Pokédex | Almost invisible, this gaseous Pokémon cloaks the target and puts it to sleep without notice |
| Altura | 4'03" (1,30 m) |
| Peso | 0,2 lb (0,1 kg) |
| Tipo | Ghost / Poison |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 95 / Medium Slow |
| Atributos base | HP 30; Atk 35; Def 30; Spd 80; Spc 100; BST 275 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 74-166; Def 64-156; Spd 163-255; Spc 203-295 |
| Movimentos iniciais | Lick, Confuse Ray, Night Shade |
| Movimentos aprendidos por nível | Nv.27 Hypnosis; Nv.35 Dream Eater |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM20 Rage; TM21 Mega Drain; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM42 Dream Eater; TM44 Rest; TM46 Psywave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Haunter ao atingir Nv.25 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (5,1%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (1,2%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (1,2%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.19 (9,8%), Nv.20 (9,8%), Nv.21 (19,9%), Nv.22 (19,9%), Nv.23 (15,2%), Nv.24 (9,8%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.20 (9,8%), Nv.21 (19,9%), Nv.22 (19,9%), Nv.23 (15,2%), Nv.24 (9,8%) |
| Spawns em Blue | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (5,1%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (1,2%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.18 (9,8%), Nv.19 (9,8%), Nv.20 (19,9%), Nv.21 (19,9%), Nv.22 (15,2%), Nv.23 (9,8%), Nv.24 (1,2%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.19 (9,8%), Nv.20 (9,8%), Nv.21 (19,9%), Nv.22 (19,9%), Nv.23 (15,2%), Nv.24 (9,8%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.20 (9,8%), Nv.21 (19,9%), Nv.22 (19,9%), Nv.23 (15,2%), Nv.24 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/gastly.asm` |

### 093 Haunter

| Campo | Valor |
|---|---|
| Nome/espécie | Haunter (`DEX_HAUNTER`) |
| Categoria Pokédex | Gas |
| Descrição Pokédex | Because of its ability to slip through block walls, it is said to be from another dimension |
| Altura | 5'03" (1,60 m) |
| Peso | 0,2 lb (0,1 kg) |
| Tipo | Ghost / Poison |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 126 / Medium Slow |
| Atributos base | HP 45; Atk 50; Def 45; Spd 95; Spc 115; BST 350 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 104-196; Def 94-186; Spd 193-285; Spc 232-324 |
| Movimentos iniciais | Lick, Confuse Ray, Night Shade |
| Movimentos aprendidos por nível | Nv.29 Hypnosis; Nv.38 Dream Eater |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM20 Rage; TM21 Mega Drain; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM42 Dream Eater; TM44 Rest; TM46 Psywave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Gengar por troca via link; nível mínimo 1 |
| Origem por evolução | Gastly: Haunter ao atingir Nv.25 ou superior após ganho de nível |
| Spawns em Red | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.25 (1,2%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.25 (5,1%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.25 (5,1%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.26 (5,1%), Nv.28 (1,2%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.28 (14,1%), Nv.30 (1,2%) |
| Spawns em Blue | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.25 (1,2%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.25 (5,1%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.25 (5,1%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.26 (5,1%), Nv.28 (1,2%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.28 (14,1%), Nv.30 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/haunter.asm` |

### 094 Gengar

| Campo | Valor |
|---|---|
| Nome/espécie | Gengar (`DEX_GENGAR`) |
| Categoria Pokédex | Shadow |
| Descrição Pokédex | Under a full moon, this Pokémon likes to mimic the shadows of people and laugh at their fright |
| Altura | 4'11" (1,50 m) |
| Peso | 89,0 lb (40,4 kg) |
| Tipo | Ghost / Poison |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 190 / Medium Slow |
| Atributos base | HP 60; Atk 65; Def 60; Spd 110; Spc 130; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 133-225; Def 123-215; Spd 222-314; Spc 262-354 |
| Movimentos iniciais | Lick, Confuse Ray, Night Shade |
| Movimentos aprendidos por nível | Nv.29 Hypnosis; Nv.38 Dream Eater |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM21 Mega Drain; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM40 Skull Bash; TM42 Dream Eater; TM44 Rest; TM46 Psywave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Haunter: Gengar por troca via link; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/gengar.asm` |

### 095 Onix

| Campo | Valor |
|---|---|
| Nome/espécie | Onix (`DEX_ONIX`) |
| Categoria Pokédex | Rock Snake |
| Descrição Pokédex | As it grows, the stone portions of its body harden to become similar to a diamond, but colored black |
| Altura | 28'10" (8,79 m) |
| Peso | 463,0 lb (210,0 kg) |
| Tipo | Rock / Ground |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 108 / Medium Fast |
| Atributos base | HP 35; Atk 45; Def 160; Spd 70; Spc 30; BST 340 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 94-186; Def 321-413; Spd 143-235; Spc 64-156 |
| Movimentos iniciais | Tackle, Screech |
| Movimentos aprendidos por nível | Nv.15 Bind; Nv.19 Rock Throw; Nv.25 Rage; Nv.33 Slam; Nv.43 Harden |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM40 Skull Bash; TM44 Rest; TM47 Explosion; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.13 (4,3%), Nv.15 (1,2%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.13 (4,3%), Nv.17 (5,1%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.36 (9,8%), Nv.39 (9,8%), Nv.42 (9,8%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.36 (9,8%), Nv.39 (9,8%), Nv.42 (9,8%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.42 (9,8%), Nv.45 (9,8%) |
| Spawns em Blue | Rock Tunnel 1F - terrestre/caverna, limiar 15/256: Nv.13 (4,3%), Nv.15 (1,2%)<br>Rock Tunnel B1F - terrestre/caverna, limiar 15/256: Nv.13 (4,3%), Nv.17 (5,1%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.36 (9,8%), Nv.39 (9,8%), Nv.42 (9,8%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.36 (9,8%), Nv.39 (9,8%), Nv.42 (9,8%)<br>Victory Road 3F - terrestre/caverna, limiar 15/256: Nv.42 (9,8%), Nv.45 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/onix.asm` |

### 096 Drowzee

| Campo | Valor |
|---|---|
| Nome/espécie | Drowzee (`DEX_DROWZEE`) |
| Categoria Pokédex | Hypnosis |
| Descrição Pokédex | Puts enemies to sleep then eats their dreams. Occasionally gets sick from eating bad dreams |
| Altura | 3'03" (0,99 m) |
| Peso | 71,0 lb (32,2 kg) |
| Tipo | Psychic |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 102 / Medium Fast |
| Atributos base | HP 60; Atk 48; Def 45; Spd 42; Spc 90; BST 285 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 100-192; Def 94-186; Spd 88-180; Spc 183-275 |
| Movimentos iniciais | Pound, Hypnosis |
| Movimentos aprendidos por nível | Nv.12 Disable; Nv.17 Confusion; Nv.24 Headbutt; Nv.29 Poison Gas; Nv.32 Psychic; Nv.37 Meditate |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM42 Dream Eater; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Hypno ao atingir Nv.26 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 11 - terrestre/caverna, limiar 15/256: Nv.9 (9,8%), Nv.11 (4,3%), Nv.13 (9,8%), Nv.15 (1,2%) |
| Spawns em Blue | Route 11 - terrestre/caverna, limiar 15/256: Nv.9 (9,8%), Nv.11 (4,3%), Nv.13 (9,8%), Nv.15 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/drowzee.asm` |

### 097 Hypno

| Campo | Valor |
|---|---|
| Nome/espécie | Hypno (`DEX_HYPNO`) |
| Categoria Pokédex | Hypnosis |
| Descrição Pokédex | When it locks eyes with an enemy, it will use a mix of PSI moves such as HYPNOSIS and CONFUSION |
| Altura | 5'03" (1,60 m) |
| Peso | 167,0 lb (75,7 kg) |
| Tipo | Psychic |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 165 / Medium Fast |
| Atributos base | HP 85; Atk 73; Def 70; Spd 67; Spc 115; BST 410 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 277-369; Atk 149-241; Def 143-235; Spd 137-229; Spc 232-324 |
| Movimentos iniciais | Pound, Hypnosis, Disable, Confusion |
| Movimentos aprendidos por nível | Nv.12 Disable; Nv.17 Confusion; Nv.24 Headbutt; Nv.33 Poison Gas; Nv.37 Psychic; Nv.43 Meditate |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM42 Dream Eater; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Drowzee: Hypno ao atingir Nv.26 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (19,9%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.46 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/hypno.asm` |

### 098 Krabby

| Campo | Valor |
|---|---|
| Nome/espécie | Krabby (`DEX_KRABBY`) |
| Categoria Pokédex | River Crab |
| Descrição Pokédex | Its pincers are not only powerful weapons, they are used for balance when walking sideways |
| Altura | 1'04" (0,41 m) |
| Peso | 14,0 lb (6,4 kg) |
| Tipo | Water |
| Catch rate | 225; cenário normalizado: 29,66% (favorável) |
| EXP base / crescimento | 115 / Medium Fast |
| Atributos base | HP 30; Atk 105; Def 90; Spd 50; Spc 25; BST 300 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 212-304; Def 183-275; Spd 104-196; Spc 54-146 |
| Movimentos iniciais | Bubble, Leer |
| Movimentos aprendidos por nível | Nv.20 Vicegrip; Nv.25 Guillotine; Nv.30 Stomp; Nv.35 Crabhammer; Nv.40 Harden |
| Movimentos possíveis por TM/HM | HM01 Cut; HM03 Surf; HM04 Strength; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Kingler ao atingir Nv.28 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Vermilion City, Route 6, Route 11, Vermilion Dock, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (9,8%), Nv.30 (9,8%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (9,8%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.28 (9,8%), Nv.30 (5,1%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.29 (9,8%), Nv.31 (5,1%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (15,2%)<br>Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Vermilion City, Route 6, Route 11, Vermilion Dock, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/krabby.asm` |

### 099 Kingler

| Campo | Valor |
|---|---|
| Nome/espécie | Kingler (`DEX_KINGLER`) |
| Categoria Pokédex | Pincer |
| Descrição Pokédex | The large pincer has 10000 hp of crushing power. However, its huge size makes it unwieldy to use |
| Altura | 4'03" (1,30 m) |
| Peso | 132,0 lb (59,9 kg) |
| Tipo | Water |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 206 / Medium Fast |
| Atributos base | HP 55; Atk 130; Def 115; Spd 75; Spc 50; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 262-354; Def 232-324; Spd 153-245; Spc 104-196 |
| Movimentos iniciais | Bubble, Leer, Vicegrip |
| Movimentos aprendidos por nível | Nv.20 Vicegrip; Nv.25 Guillotine; Nv.34 Stomp; Nv.42 Crabhammer; Nv.49 Harden |
| Movimentos possíveis por TM/HM | HM01 Cut; HM03 Surf; HM04 Strength; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Krabby: Kingler ao atingir Nv.28 ou superior após ganho de nível |
| Spawns em Red | Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%)<br>Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/kingler.asm` |

### 100 Voltorb

| Campo | Valor |
|---|---|
| Nome/espécie | Voltorb (`DEX_VOLTORB`) |
| Categoria Pokédex | Ball |
| Descrição Pokédex | Usually found in power plants. Easily mistaken for a Poké Ball, they have zapped many people |
| Altura | 1'08" (0,51 m) |
| Peso | 23,0 lb (10,4 kg) |
| Tipo | Electric |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 103 / Medium Fast |
| Atributos base | HP 40; Atk 30; Def 50; Spd 100; Spc 55; BST 275 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 64-156; Def 104-196; Spd 203-295; Spc 113-205 |
| Movimentos iniciais | Tackle, Screech |
| Movimentos aprendidos por nível | Nv.17 Sonicboom; Nv.22 Selfdestruct; Nv.29 Light Screen; Nv.36 Swift; Nv.43 Explosion |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM09 Take Down; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM39 Swift; TM44 Rest; TM45 Thunder Wave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Electrode ao atingir Nv.30 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Power Plant - terrestre/caverna, limiar 10/256: Nv.21 (19,9%), Nv.23 (9,8%)<br>Route 10 - terrestre/caverna, limiar 15/256: Nv.14 (15,2%), Nv.16 (19,9%), Nv.17 (5,1%)<br>Power Plant - encontro estático capturável, Nv.40 |
| Spawns em Blue | Power Plant - terrestre/caverna, limiar 10/256: Nv.21 (19,9%), Nv.23 (9,8%)<br>Route 10 - terrestre/caverna, limiar 15/256: Nv.14 (15,2%), Nv.16 (19,9%), Nv.17 (5,1%)<br>Power Plant - encontro estático capturável, Nv.40 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/voltorb.asm` |

### 101 Electrode

| Campo | Valor |
|---|---|
| Nome/espécie | Electrode (`DEX_ELECTRODE`) |
| Categoria Pokédex | Ball |
| Descrição Pokédex | It stores electric energy under very high pressure. It often explodes with little or no provocation |
| Altura | 3'11" (1,19 m) |
| Peso | 147,0 lb (66,7 kg) |
| Tipo | Electric |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 150 / Medium Fast |
| Atributos base | HP 60; Atk 50; Def 70; Spd 140; Spc 80; BST 400 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 104-196; Def 143-235; Spd 282-374; Spc 163-255 |
| Movimentos iniciais | Tackle, Screech, Sonicboom |
| Movimentos aprendidos por nível | Nv.17 Sonicboom; Nv.22 Selfdestruct; Nv.29 Light Screen; Nv.40 Swift; Nv.50 Explosion |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM09 Take Down; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Voltorb: Electrode ao atingir Nv.30 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (15,2%)<br>Power Plant - encontro estático capturável, Nv.43 |
| Spawns em Blue | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (15,2%)<br>Power Plant - encontro estático capturável, Nv.43 |
| Aquisição especial em Red | Troca NPC em Cinnabar Lab Trade Room: entregar Raichu; recebido no mesmo nível, apelido DORIS |
| Aquisição especial em Blue | Troca NPC em Cinnabar Lab Trade Room: entregar Raichu; recebido no mesmo nível, apelido DORIS |
| Fonte específica | `data/pokemon/base_stats/electrode.asm` |

### 102 Exeggcute

| Campo | Valor |
|---|---|
| Nome/espécie | Exeggcute (`DEX_EXEGGCUTE`) |
| Categoria Pokédex | Egg |
| Descrição Pokédex | Often mistaken for eggs. When disturbed, they quickly gather and attack in swarms |
| Altura | 1'04" (0,41 m) |
| Peso | 6,0 lb (2,7 kg) |
| Tipo | Grass / Psychic |
| Catch rate | 90; cenário normalizado: 11,94% (intermediária) |
| EXP base / crescimento | 98 / Slow |
| Atributos base | HP 60; Atk 40; Def 80; Spd 40; Spc 60; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 84-176; Def 163-255; Spd 84-176; Spc 123-215 |
| Movimentos iniciais | Barrage, Hypnosis |
| Movimentos aprendidos por nível | Nv.25 Reflect; Nv.28 Leech Seed; Nv.32 Stun Spore; Nv.37 Poisonpowder; Nv.42 Solarbeam; Nv.48 Sleep Powder |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM37 Egg Bomb; TM44 Rest; TM46 Psywave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Exeggutor ao usar Leaf Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.24 (9,8%), Nv.25 (9,8%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.23 (9,8%), Nv.25 (9,8%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.25 (9,8%), Nv.27 (9,8%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.24 (9,8%), Nv.26 (9,8%) |
| Spawns em Blue | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.24 (9,8%), Nv.25 (9,8%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.23 (9,8%), Nv.25 (9,8%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.25 (9,8%), Nv.27 (9,8%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.24 (9,8%), Nv.26 (9,8%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/exeggcute.asm` |

### 103 Exeggutor

| Campo | Valor |
|---|---|
| Nome/espécie | Exeggutor (`DEX_EXEGGUTOR`) |
| Categoria Pokédex | Coconut |
| Descrição Pokédex | Legend has it that on rare occasions, one of its heads will drop off and continue on as an EXEGGCUTE |
| Altura | 6'07" (2,01 m) |
| Peso | 265,0 lb (120,2 kg) |
| Tipo | Grass / Psychic |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 212 / Slow |
| Atributos base | HP 95; Atk 95; Def 85; Spd 55; Spc 125; BST 455 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 297-389; Atk 193-285; Def 173-265; Spd 113-205; Spc 252-344 |
| Movimentos iniciais | Barrage, Hypnosis |
| Movimentos aprendidos por nível | Nv.28 Stomp |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM36 Selfdestruct; TM37 Egg Bomb; TM44 Rest; TM46 Psywave; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Exeggcute: Exeggutor ao usar Leaf Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/exeggutor.asm` |

### 104 Cubone

| Campo | Valor |
|---|---|
| Nome/espécie | Cubone (`DEX_CUBONE`) |
| Categoria Pokédex | Lonely |
| Descrição Pokédex | Because it never removes its skull helmet, no one has ever seen this Pokémon's real face |
| Altura | 1'04" (0,41 m) |
| Peso | 14,0 lb (6,4 kg) |
| Tipo | Ground |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 87 / Medium Fast |
| Atributos base | HP 50; Atk 50; Def 95; Spd 35; Spc 40; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 104-196; Def 193-285; Spd 74-166; Spc 84-176 |
| Movimentos iniciais | Bone Club, Growl |
| Movimentos aprendidos por nível | Nv.25 Leer; Nv.31 Focus Energy; Nv.38 Thrash; Nv.43 Bonemerang; Nv.46 Rage |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Marowak ao atingir Nv.28 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.22 (5,1%), Nv.24 (4,3%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.22 (5,1%), Nv.24 (5,1%) |
| Spawns em Blue | Pokémon Tower 3F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 4F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 5F - terrestre/caverna, limiar 10/256: Nv.20 (5,1%), Nv.22 (4,3%)<br>Pokémon Tower 6F - terrestre/caverna, limiar 15/256: Nv.22 (5,1%), Nv.24 (4,3%)<br>Pokémon Tower 7F - terrestre/caverna, limiar 15/256: Nv.22 (5,1%), Nv.24 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/cubone.asm` |

### 105 Marowak

| Campo | Valor |
|---|---|
| Nome/espécie | Marowak (`DEX_MAROWAK`) |
| Categoria Pokédex | Bonekeeper |
| Descrição Pokédex | The bone it holds is its key weapon. It throws the bone skillfully like a boomerang to KO targets |
| Altura | 3'03" (0,99 m) |
| Peso | 99,0 lb (44,9 kg) |
| Tipo | Ground |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 124 / Medium Fast |
| Atributos base | HP 60; Atk 80; Def 110; Spd 45; Spc 50; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 163-255; Def 222-314; Spd 94-186; Spc 104-196 |
| Movimentos iniciais | Bone Club, Growl, Leer, Focus Energy |
| Movimentos aprendidos por nível | Nv.25 Leer; Nv.33 Focus Energy; Nv.41 Thrash; Nv.48 Bonemerang; Nv.55 Rage |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Cubone: Marowak ao atingir Nv.28 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (19,9%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.43 (1,2%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.40 (4,3%) |
| Spawns em Blue | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (19,9%)<br>Victory Road 1F - terrestre/caverna, limiar 15/256: Nv.43 (1,2%)<br>Victory Road 2F - terrestre/caverna, limiar 10/256: Nv.40 (4,3%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/marowak.asm` |

### 106 Hitmonlee

| Campo | Valor |
|---|---|
| Nome/espécie | Hitmonlee (`DEX_HITMONLEE`) |
| Categoria Pokédex | Kicking |
| Descrição Pokédex | When in a hurry, its legs lengthen progressively. It runs smoothly with extra long, loping strides |
| Altura | 4'11" (1,50 m) |
| Peso | 110,0 lb (49,9 kg) |
| Tipo | Fighting |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 139 / Medium Fast |
| Atributos base | HP 50; Atk 120; Def 53; Spd 87; Spc 35; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 242-334; Def 109-202; Spd 177-269; Spc 74-166 |
| Movimentos iniciais | Double Kick, Meditate |
| Movimentos aprendidos por nível | Nv.33 Rolling Kick; Nv.38 Jump Kick; Nv.43 Focus Energy; Nv.48 Hi Jump Kick; Nv.53 Mega Kick |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan |
| Aquisição especial em Blue | Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan |
| Fonte específica | `data/pokemon/base_stats/hitmonlee.asm` |

### 107 Hitmonchan

| Campo | Valor |
|---|---|
| Nome/espécie | Hitmonchan (`DEX_HITMONCHAN`) |
| Categoria Pokédex | Punching |
| Descrição Pokédex | While apparently doing nothing, it fires punches in lightning fast volleys that are impossible to see |
| Altura | 4'07" (1,40 m) |
| Peso | 111,0 lb (50,3 kg) |
| Tipo | Fighting |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 140 / Medium Fast |
| Atributos base | HP 50; Atk 105; Def 79; Spd 76; Spc 35; BST 345 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 208-300; Atk 212-304; Def 161-253; Spd 155-247; Spc 74-166 |
| Movimentos iniciais | Comet Punch, Agility |
| Movimentos aprendidos por nível | Nv.33 Fire Punch; Nv.38 Ice Punch; Nv.43 Thunderpunch; Nv.48 Mega Punch; Nv.53 Counter |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan |
| Aquisição especial em Blue | Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan |
| Fonte específica | `data/pokemon/base_stats/hitmonchan.asm` |

### 108 Lickitung

| Campo | Valor |
|---|---|
| Nome/espécie | Lickitung (`DEX_LICKITUNG`) |
| Categoria Pokédex | Licking |
| Descrição Pokédex | Its tongue can be extended like a chameleon's. It leaves a tingling sensation when it licks enemies |
| Altura | 3'11" (1,19 m) |
| Peso | 144,0 lb (65,3 kg) |
| Tipo | Normal |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 127 / Medium Fast |
| Atributos base | HP 90; Atk 55; Def 75; Spd 30; Spc 60; BST 310 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 113-205; Def 153-245; Spd 64-156; Spc 123-215 |
| Movimentos iniciais | Wrap, Supersonic |
| Movimentos aprendidos por nível | Nv.7 Stomp; Nv.15 Disable; Nv.23 Defense Curl; Nv.31 Slam; Nv.39 Screech |
| Movimentos possíveis por TM/HM | HM01 Cut; HM03 Surf; HM04 Strength; TM01 Mega Punch; TM03 Swords Dance; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Troca NPC em Route 18 Gate 2F: entregar Slowbro; recebido no mesmo nível, apelido MARC |
| Aquisição especial em Blue | Troca NPC em Route 18 Gate 2F: entregar Slowbro; recebido no mesmo nível, apelido MARC |
| Fonte específica | `data/pokemon/base_stats/lickitung.asm` |

### 109 Koffing

| Campo | Valor |
|---|---|
| Nome/espécie | Koffing (`DEX_KOFFING`) |
| Categoria Pokédex | Poison Gas |
| Descrição Pokédex | Because it stores several kinds of toxic gases in its body, it is prone to exploding without warning |
| Altura | 2'00" (0,61 m) |
| Peso | 2,0 lb (0,9 kg) |
| Tipo | Poison |
| Catch rate | 190; cenário normalizado: 25,06% (favorável) |
| EXP base / crescimento | 114 / Medium Fast |
| Atributos base | HP 40; Atk 65; Def 95; Spd 35; Spc 60; BST 295 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 133-225; Def 193-285; Spd 74-166; Spc 123-215 |
| Movimentos iniciais | Tackle, Smog |
| Movimentos aprendidos por nível | Nv.32 Sludge; Nv.37 Smokescreen; Nv.40 Selfdestruct; Nv.45 Haze; Nv.48 Explosion |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Weezing ao atingir Nv.35 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (19,9%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.30 (9,8%), Nv.34 (35,2%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.35 (15,2%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.31 (29,7%), Nv.33 (19,9%) |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.30 (5,1%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.30 (5,1%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.34 (5,1%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.35 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/koffing.asm` |

### 110 Weezing

| Campo | Valor |
|---|---|
| Nome/espécie | Weezing (`DEX_WEEZING`) |
| Categoria Pokédex | Poison Gas |
| Descrição Pokédex | Where two kinds of poison gases meet, 2 KOFFINGs can fuse into a WEEZING over many years |
| Altura | 3'11" (1,19 m) |
| Peso | 21,0 lb (9,5 kg) |
| Tipo | Poison |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 173 / Medium Fast |
| Atributos base | HP 65; Atk 90; Def 120; Spd 60; Spc 85; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 183-275; Def 242-334; Spd 123-215; Spc 173-265 |
| Movimentos iniciais | Tackle, Smog, Sludge |
| Movimentos aprendidos por nível | Nv.32 Sludge; Nv.39 Smokescreen; Nv.43 Selfdestruct; Nv.49 Haze; Nv.53 Explosion |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM34 Bide; TM36 Selfdestruct; TM38 Fire Blast; TM44 Rest; TM47 Explosion; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Koffing: Weezing ao atingir Nv.35 ou superior após ganho de nível |
| Spawns em Red | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.37 (4,3%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.38 (5,1%), Nv.40 (9,8%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.40 (9,8%), Nv.42 (4,3%) |
| Spawns em Blue | Pokémon Mansion 1F - terrestre/caverna, limiar 10/256: Nv.39 (1,2%)<br>Pokémon Mansion 2F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.42 (1,2%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.42 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/weezing.asm` |

### 111 Rhyhorn

| Campo | Valor |
|---|---|
| Nome/espécie | Rhyhorn (`DEX_RHYHORN`) |
| Categoria Pokédex | Spikes |
| Descrição Pokédex | Its massive bones are 1000 times harder than human bones. It can easily knock a trailer flying |
| Altura | 3'03" (0,99 m) |
| Peso | 254,0 lb (115,2 kg) |
| Tipo | Ground / Rock |
| Catch rate | 120; cenário normalizado: 15,88% (intermediária) |
| EXP base / crescimento | 135 / Slow |
| Atributos base | HP 80; Atk 85; Def 95; Spd 25; Spc 30; BST 315 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 173-265; Def 193-285; Spd 54-146; Spc 64-156 |
| Movimentos iniciais | Horn Attack |
| Movimentos aprendidos por nível | Nv.30 Stomp; Nv.35 Tail Whip; Nv.40 Fury Attack; Nv.45 Horn Drill; Nv.50 Leer; Nv.55 Take Down |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Rhydon ao atingir Nv.42 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.25 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.26 (19,9%) |
| Spawns em Blue | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.25 (19,9%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.26 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/rhyhorn.asm` |

### 112 Rhydon

| Campo | Valor |
|---|---|
| Nome/espécie | Rhydon (`DEX_RHYDON`) |
| Categoria Pokédex | Drill |
| Descrição Pokédex | Protected by an armor-like hide, it is capable of living in molten lava of 3,600 degrees |
| Altura | 6'03" (1,91 m) |
| Peso | 265,0 lb (120,2 kg) |
| Tipo | Ground / Rock |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 204 / Slow |
| Atributos base | HP 105; Atk 130; Def 120; Spd 40; Spc 45; BST 440 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 316-408; Atk 262-354; Def 242-334; Spd 84-176; Spc 94-186 |
| Movimentos iniciais | Horn Attack, Stomp, Tail Whip, Fury Attack |
| Movimentos aprendidos por nível | Nv.30 Stomp; Nv.35 Tail Whip; Nv.40 Fury Attack; Nv.48 Horn Drill; Nv.55 Leer; Nv.64 Take Down |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Rhyhorn: Rhydon ao atingir Nv.42 ou superior após ganho de nível |
| Spawns em Red | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (19,9%) |
| Spawns em Blue | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.52 (9,8%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.55 (19,9%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/rhydon.asm` |

### 113 Chansey

| Campo | Valor |
|---|---|
| Nome/espécie | Chansey (`DEX_CHANSEY`) |
| Categoria Pokédex | Egg |
| Descrição Pokédex | A rare and elusive Pokémon that is said to bring happiness to those who manage to get it |
| Altura | 3'07" (1,09 m) |
| Peso | 76,0 lb (34,5 kg) |
| Tipo | Normal |
| Catch rate | 30; cenário normalizado: 4,07% (difícil) |
| EXP base / crescimento | 255 / Fast |
| Atributos base | HP 250; Atk 5; Def 5; Spd 50; Spc 105; BST 415 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 604-696; Atk 14-106; Def 14-106; Spd 104-196; Spc 212-304 |
| Movimentos iniciais | Pound, Doubleslap |
| Movimentos aprendidos por nível | Nv.24 Sing; Nv.30 Growl; Nv.38 Minimize; Nv.44 Defense Curl; Nv.48 Light Screen; Nv.54 Double-Edge |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM37 Egg Bomb; TM38 Fire Blast; TM40 Skull Bash; TM41 Softboiled; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.56 (5,1%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.23 (1,2%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.26 (4,3%) |
| Spawns em Blue | Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.56 (5,1%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.64 (9,8%)<br>Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.23 (1,2%)<br>Safari Zone North - terrestre/caverna, limiar 30/256: Nv.26 (4,3%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/chansey.asm` |

### 114 Tangela

| Campo | Valor |
|---|---|
| Nome/espécie | Tangela (`DEX_TANGELA`) |
| Categoria Pokédex | Vine |
| Descrição Pokédex | The whole body is swathed with wide vines that are similar to seaweed. Its vines shake as it walks |
| Altura | 3'03" (0,99 m) |
| Peso | 77,0 lb (34,9 kg) |
| Tipo | Grass |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 166 / Medium Fast |
| Atributos base | HP 65; Atk 55; Def 115; Spd 60; Spc 100; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 113-205; Def 232-324; Spd 123-215; Spc 203-295 |
| Movimentos iniciais | Constrict, Bind |
| Movimentos aprendidos por nível | Nv.29 Absorb; Nv.32 Poisonpowder; Nv.36 Stun Spore; Nv.39 Sleep Powder; Nv.45 Slam; Nv.49 Growth |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM31 Mimic; TM32 Double Team; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 21 - terrestre/caverna, limiar 25/256: Nv.28 (5,1%), Nv.30 (4,3%), Nv.32 (1,2%) |
| Spawns em Blue | Route 21 - terrestre/caverna, limiar 25/256: Nv.28 (5,1%), Nv.30 (4,3%), Nv.32 (1,2%) |
| Aquisição especial em Red | Troca NPC em Cinnabar Lab Trade Room: entregar Venonat; recebido no mesmo nível, apelido CRINKLES |
| Aquisição especial em Blue | Troca NPC em Cinnabar Lab Trade Room: entregar Venonat; recebido no mesmo nível, apelido CRINKLES |
| Fonte específica | `data/pokemon/base_stats/tangela.asm` |

### 115 Kangaskhan

| Campo | Valor |
|---|---|
| Nome/espécie | Kangaskhan (`DEX_KANGASKHAN`) |
| Categoria Pokédex | Parent |
| Descrição Pokédex | The infant rarely ventures out of its mother's protective pouch until it is 3 years old |
| Altura | 7'03" (2,21 m) |
| Peso | 176,0 lb (79,8 kg) |
| Tipo | Normal |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 175 / Medium Fast |
| Atributos base | HP 105; Atk 95; Def 80; Spd 90; Spc 40; BST 410 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 316-408; Atk 193-285; Def 163-255; Spd 183-275; Spc 84-176 |
| Movimentos iniciais | Comet Punch, Rage |
| Movimentos aprendidos por nível | Nv.26 Bite; Nv.31 Tail Whip; Nv.36 Mega Punch; Nv.41 Leer; Nv.46 Dizzy Punch |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Safari Zone East - terrestre/caverna, limiar 30/256: Nv.25 (4,3%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.28 (1,2%) |
| Spawns em Blue | Safari Zone East - terrestre/caverna, limiar 30/256: Nv.25 (4,3%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.28 (1,2%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/kangaskhan.asm` |

### 116 Horsea

| Campo | Valor |
|---|---|
| Nome/espécie | Horsea (`DEX_HORSEA`) |
| Categoria Pokédex | Dragon |
| Descrição Pokédex | Known to shoot down flying bugs with precision blasts of ink from the surface of the water |
| Altura | 1'04" (0,41 m) |
| Peso | 18,0 lb (8,2 kg) |
| Tipo | Water |
| Catch rate | 225; cenário normalizado: 29,66% (favorável) |
| EXP base / crescimento | 83 / Medium Fast |
| Atributos base | HP 30; Atk 40; Def 70; Spd 60; Spc 70; BST 270 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 84-176; Def 143-235; Spd 123-215; Spc 143-235 |
| Movimentos iniciais | Bubble |
| Movimentos aprendidos por nível | Nv.19 Smokescreen; Nv.24 Leer; Nv.30 Water Gun; Nv.37 Agility; Nv.45 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Seadra ao atingir Nv.32 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (9,8%), Nv.30 (9,8%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%), Nv.32 (9,8%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.28 (9,8%), Nv.30 (5,1%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.29 (9,8%), Nv.31 (5,1%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (15,2%)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/horsea.asm` |

### 117 Seadra

| Campo | Valor |
|---|---|
| Nome/espécie | Seadra (`DEX_SEADRA`) |
| Categoria Pokédex | Dragon |
| Descrição Pokédex | Capable of swimming backwards by rapidly flapping its wing-like pectoral fins and stout tail |
| Altura | 3'11" (1,19 m) |
| Peso | 55,0 lb (24,9 kg) |
| Tipo | Water |
| Catch rate | 75; cenário normalizado: 9,97% (difícil) |
| EXP base / crescimento | 155 / Medium Fast |
| Atributos base | HP 55; Atk 65; Def 95; Spd 85; Spc 95; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 133-225; Def 193-285; Spd 173-265; Spc 193-285 |
| Movimentos iniciais | Bubble, Smokescreen |
| Movimentos aprendidos por nível | Nv.19 Smokescreen; Nv.24 Leer; Nv.30 Water Gun; Nv.41 Agility; Nv.52 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Horsea: Seadra ao atingir Nv.32 ou superior após ganho de nível |
| Spawns em Red | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.37 (1,2%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.39 (4,3%)<br>Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/seadra.asm` |

### 118 Goldeen

| Campo | Valor |
|---|---|
| Nome/espécie | Goldeen (`DEX_GOLDEEN`) |
| Categoria Pokédex | Goldfish |
| Descrição Pokédex | Its tail fin billows like an elegant ballroom dress, giving it the nickname of the Water Queen |
| Altura | 2'00" (0,61 m) |
| Peso | 33,0 lb (15,0 kg) |
| Tipo | Water |
| Catch rate | 225; cenário normalizado: 29,66% (favorável) |
| EXP base / crescimento | 111 / Medium Fast |
| Atributos base | HP 45; Atk 67; Def 60; Spd 63; Spc 50; BST 285 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 198-290; Atk 137-229; Def 123-215; Spd 129-221; Spc 104-196 |
| Movimentos iniciais | Peck, Tail Whip |
| Movimentos aprendidos por nível | Nv.19 Supersonic; Nv.24 Horn Attack; Nv.30 Fury Attack; Nv.37 Waterfall; Nv.45 Horn Drill; Nv.54 Agility |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM07 Horn Drill; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Seaking ao atingir Nv.33 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso<br>Super Rod - Route 22, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso<br>Super Rod - Route 22, Nv.15; 25,0% por uso (50% sem fisgada)<br>Super Rod - Cerulean City, Route 4, Route 24, Route 25, Cerulean Gym, Nv.15; 16,7% por uso (50% sem fisgada)<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/goldeen.asm` |

### 119 Seaking

| Campo | Valor |
|---|---|
| Nome/espécie | Seaking (`DEX_SEAKING`) |
| Categoria Pokédex | Goldfish |
| Descrição Pokédex | In the autumn spawning season, they can be seen swimming powerfully up rivers and creeks |
| Altura | 4'03" (1,30 m) |
| Peso | 86,0 lb (39,0 kg) |
| Tipo | Water |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 170 / Medium Fast |
| Atributos base | HP 80; Atk 92; Def 65; Spd 68; Spc 80; BST 385 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 187-279; Def 133-225; Spd 139-231; Spc 163-255 |
| Movimentos iniciais | Peck, Tail Whip, Supersonic |
| Movimentos aprendidos por nível | Nv.19 Supersonic; Nv.24 Horn Attack; Nv.30 Fury Attack; Nv.39 Waterfall; Nv.48 Horn Drill; Nv.54 Agility |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM07 Horn Drill; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Goldeen: Seaking ao atingir Nv.33 ou superior após ganho de nível |
| Spawns em Red | Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.23; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Super Rod - Route 23, Cerulean Cave 2F, Cerulean Cave B1F, Cerulean Cave 1F, Nv.23; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.23; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/seaking.asm` |

### 120 Staryu

| Campo | Valor |
|---|---|
| Nome/espécie | Staryu (`DEX_STARYU`) |
| Categoria Pokédex | Starshape |
| Descrição Pokédex | An enigmatic Pokémon that can effortlessly regenerate any appendage it loses in battle |
| Altura | 2'07" (0,79 m) |
| Peso | 76,0 lb (34,5 kg) |
| Tipo | Water |
| Catch rate | 225; cenário normalizado: 29,66% (favorável) |
| EXP base / crescimento | 106 / Slow |
| Atributos base | HP 30; Atk 45; Def 55; Spd 85; Spc 70; BST 285 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 94-186; Def 113-205; Spd 173-265; Spc 143-235 |
| Movimentos iniciais | Tackle |
| Movimentos aprendidos por nível | Nv.17 Water Gun; Nv.22 Harden; Nv.27 Recover; Nv.32 Swift; Nv.37 Minimize; Nv.42 Light Screen; Nv.47 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM05 Flash; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Starmie ao usar Water Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.30 (19,9%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.30 (9,8%)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Seafoam Islands 1F - terrestre/caverna, limiar 15/256: Nv.28 (4,3%), Nv.30 (15,2%)<br>Seafoam Islands B1F - terrestre/caverna, limiar 10/256: Nv.32 (15,2%)<br>Seafoam Islands B2F - terrestre/caverna, limiar 10/256: Nv.28 (5,1%)<br>Seafoam Islands B3F - terrestre/caverna, limiar 10/256: Nv.29 (5,1%), Nv.31 (9,8%)<br>Seafoam Islands B4F - terrestre/caverna, limiar 10/256: Nv.31 (19,9%), Nv.33 (9,8%)<br>Super Rod - Cinnabar Island, Route 19, Route 20, Route 21, Seafoam Islands B3F, Seafoam Islands B4F, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/staryu.asm` |

### 121 Starmie

| Campo | Valor |
|---|---|
| Nome/espécie | Starmie (`DEX_STARMIE`) |
| Categoria Pokédex | Mysterious |
| Descrição Pokédex | Its central core glows with the seven colors of the rainbow. Some people value the core as a gem |
| Altura | 3'07" (1,09 m) |
| Peso | 176,0 lb (79,8 kg) |
| Tipo | Water / Psychic |
| Catch rate | 60; cenário normalizado: 8,00% (difícil) |
| EXP base / crescimento | 207 / Slow |
| Atributos base | HP 60; Atk 75; Def 85; Spd 115; Spc 100; BST 435 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 153-245; Def 173-265; Spd 232-324; Spc 203-295 |
| Movimentos iniciais | Tackle, Water Gun, Harden |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | HM03 Surf; HM05 Flash; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Staryu: Starmie ao usar Water Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/starmie.asm` |

### 122 Mr. Mime

| Campo | Valor |
|---|---|
| Nome/espécie | Mr. Mime (`DEX_MR_MIME`) |
| Categoria Pokédex | Barrier |
| Descrição Pokédex | If interrupted while it is miming, it will slap around the offender with its broad hands |
| Altura | 4'03" (1,30 m) |
| Peso | 120,0 lb (54,4 kg) |
| Tipo | Psychic |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 136 / Medium Fast |
| Atributos base | HP 40; Atk 45; Def 65; Spd 90; Spc 100; BST 340 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 188-280; Atk 94-186; Def 133-225; Spd 183-275; Spc 203-295 |
| Movimentos iniciais | Confusion, Barrier |
| Movimentos aprendidos por nível | Nv.15 Confusion; Nv.23 Light Screen; Nv.31 Doubleslap; Nv.39 Meditate; Nv.47 Substitute |
| Movimentos possíveis por TM/HM | HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Troca NPC em Route 2 Trade House: entregar Abra; recebido no mesmo nível, apelido MARCEL |
| Aquisição especial em Blue | Troca NPC em Route 2 Trade House: entregar Abra; recebido no mesmo nível, apelido MARCEL |
| Fonte específica | `data/pokemon/base_stats/mrmime.asm` |

### 123 Scyther

| Campo | Valor |
|---|---|
| Nome/espécie | Scyther (`DEX_SCYTHER`) |
| Categoria Pokédex | Mantis |
| Descrição Pokédex | With ninja-like agility and speed, it can create the illusion that there is more than one |
| Altura | 4'11" (1,50 m) |
| Peso | 123,0 lb (55,8 kg) |
| Tipo | Bug / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 187 / Medium Fast |
| Atributos base | HP 70; Atk 110; Def 80; Spd 105; Spc 55; BST 420 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 222-314; Def 163-255; Spd 212-304; Spc 113-205 |
| Movimentos iniciais | Quick Attack |
| Movimentos aprendidos por nível | Nv.17 Leer; Nv.20 Focus Energy; Nv.24 Double Team; Nv.29 Slash; Nv.35 Swords Dance; Nv.42 Agility |
| Movimentos possíveis por TM/HM | HM01 Cut; TM03 Swords Dance; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.23 (4,3%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.28 (1,2%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.25, por 5500 moedas |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/scyther.asm` |

### 124 Jynx

| Campo | Valor |
|---|---|
| Nome/espécie | Jynx (`DEX_JYNX`) |
| Categoria Pokédex | Humanshape |
| Descrição Pokédex | It seductively wiggles its hips as it walks. It can cause people to dance in unison with it |
| Altura | 4'07" (1,40 m) |
| Peso | 90,0 lb (40,8 kg) |
| Tipo | Ice / Psychic |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 137 / Medium Fast |
| Atributos base | HP 65; Atk 50; Def 35; Spd 95; Spc 95; BST 340 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 104-196; Def 74-166; Spd 193-285; Spc 193-285 |
| Movimentos iniciais | Pound, Lovely Kiss |
| Movimentos aprendidos por nível | Nv.18 Lick; Nv.23 Doubleslap; Nv.31 Ice Punch; Nv.39 Body Slam; Nv.47 Thrash; Nv.58 Blizzard |
| Movimentos possíveis por TM/HM | TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Troca NPC em Cerulean Trade House: entregar Poliwhirl; recebido no mesmo nível, apelido LOLA |
| Aquisição especial em Blue | Troca NPC em Cerulean Trade House: entregar Poliwhirl; recebido no mesmo nível, apelido LOLA |
| Fonte específica | `data/pokemon/base_stats/jynx.asm` |

### 125 Electabuzz

| Campo | Valor |
|---|---|
| Nome/espécie | Electabuzz (`DEX_ELECTABUZZ`) |
| Categoria Pokédex | Electric |
| Descrição Pokédex | Normally found near power plants, they can wander away and cause major blackouts in cities |
| Altura | 3'07" (1,09 m) |
| Peso | 66,0 lb (29,9 kg) |
| Tipo | Electric |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 156 / Medium Fast |
| Atributos base | HP 65; Atk 83; Def 57; Spd 105; Spc 85; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 169-261; Def 117-209; Spd 212-304; Spc 173-265 |
| Movimentos iniciais | Quick Attack, Leer |
| Movimentos aprendidos por nível | Nv.34 Thundershock; Nv.37 Screech; Nv.42 Thunderpunch; Nv.49 Light Screen; Nv.54 Thunder |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Power Plant - terrestre/caverna, limiar 10/256: Nv.33 (4,3%), Nv.36 (1,2%) |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Troca via link com uma partida de Pokémon Red |
| Fonte específica | `data/pokemon/base_stats/electabuzz.asm` |

### 126 Magmar

| Campo | Valor |
|---|---|
| Nome/espécie | Magmar (`DEX_MAGMAR`) |
| Categoria Pokédex | Spitfire |
| Descrição Pokédex | Its body always burns with an orange glow that enables it to hide perfectly among flames |
| Altura | 4'03" (1,30 m) |
| Peso | 98,0 lb (44,5 kg) |
| Tipo | Fire |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 167 / Medium Fast |
| Atributos base | HP 65; Atk 95; Def 57; Spd 93; Spc 85; BST 395 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 193-285; Def 117-209; Spd 189-281; Spc 173-265 |
| Movimentos iniciais | Ember |
| Movimentos aprendidos por nível | Nv.36 Leer; Nv.39 Confuse Ray; Nv.43 Fire Punch; Nv.48 Smokescreen; Nv.52 Smog; Nv.55 Flamethrower |
| Movimentos possíveis por TM/HM | HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM34 Bide; TM35 Metronome; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Pokémon Mansion 3F - terrestre/caverna, limiar 10/256: Nv.34 (9,8%)<br>Pokémon Mansion B1F - terrestre/caverna, limiar 10/256: Nv.38 (4,3%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/magmar.asm` |

### 127 Pinsir

| Campo | Valor |
|---|---|
| Nome/espécie | Pinsir (`DEX_PINSIR`) |
| Categoria Pokédex | Stagbeetle |
| Descrição Pokédex | If it fails to crush the victim in its pincers, it will swing it around and toss it hard |
| Altura | 4'11" (1,50 m) |
| Peso | 121,0 lb (54,9 kg) |
| Tipo | Bug |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 200 / Slow |
| Atributos base | HP 65; Atk 125; Def 100; Spd 85; Spc 55; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 252-344; Def 203-295; Spd 173-265; Spc 113-205 |
| Movimentos iniciais | Vicegrip |
| Movimentos aprendidos por nível | Nv.25 Seismic Toss; Nv.30 Guillotine; Nv.36 Focus Energy; Nv.43 Harden; Nv.49 Slash; Nv.54 Swords Dance |
| Movimentos possíveis por TM/HM | HM01 Cut; HM04 Strength; TM03 Swords Dance; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM31 Mimic; TM32 Double Team; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Safari Zone Center - terrestre/caverna, limiar 30/256: Nv.23 (4,3%)<br>Safari Zone East - terrestre/caverna, limiar 30/256: Nv.28 (1,2%) |
| Aquisição especial em Red | Troca via link com uma partida de Pokémon Blue |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.20, por 2500 moedas |
| Fonte específica | `data/pokemon/base_stats/pinsir.asm` |

### 128 Tauros

| Campo | Valor |
|---|---|
| Nome/espécie | Tauros (`DEX_TAUROS`) |
| Categoria Pokédex | Wild Bull |
| Descrição Pokédex | When it targets an enemy, it charges furiously while whipping its body with its long tails |
| Altura | 4'07" (1,40 m) |
| Peso | 195,0 lb (88,5 kg) |
| Tipo | Normal |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 211 / Slow |
| Atributos base | HP 75; Atk 100; Def 95; Spd 110; Spc 70; BST 450 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 257-349; Atk 203-295; Def 193-285; Spd 222-314; Spc 143-235 |
| Movimentos iniciais | Tackle |
| Movimentos aprendidos por nível | Nv.21 Stomp; Nv.28 Tail Whip; Nv.35 Leer; Nv.44 Rage; Nv.51 Take Down |
| Movimentos possíveis por TM/HM | HM04 Strength; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM31 Mimic; TM32 Double Team; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Safari Zone North - terrestre/caverna, limiar 30/256: Nv.28 (1,2%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.26 (4,3%) |
| Spawns em Blue | Safari Zone North - terrestre/caverna, limiar 30/256: Nv.28 (1,2%)<br>Safari Zone West - terrestre/caverna, limiar 30/256: Nv.26 (4,3%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/tauros.asm` |

### 129 Magikarp

| Campo | Valor |
|---|---|
| Nome/espécie | Magikarp (`DEX_MAGIKARP`) |
| Categoria Pokédex | Fish |
| Descrição Pokédex | In the distant past, it was somewhat stronger than the horribly weak descendants that exist today |
| Altura | 2'11" (0,89 m) |
| Peso | 22,0 lb (10,0 kg) |
| Tipo | Water |
| Catch rate | 255; cenário normalizado: 33,59% (muito favorável) |
| EXP base / crescimento | 20 / Slow |
| Atributos base | HP 20; Atk 10; Def 55; Spd 80; Spc 20; BST 185 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 148-240; Atk 24-116; Def 113-205; Spd 163-255; Spc 44-136 |
| Movimentos iniciais | Splash |
| Movimentos aprendidos por nível | Nv.15 Tackle |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Gyarados ao atingir Nv.20 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Old Rod - qualquer ponto de pesca válido, Nv.5; fisgada garantida<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Old Rod - qualquer ponto de pesca válido, Nv.5; fisgada garantida<br>Super Rod - Route 12, Route 13, Route 17, Route 18, Nv.15; 12,5% por uso (50% sem fisgada)<br>Super Rod - Fuchsia City, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Compra no Mt. Moon Pokécenter, Nv.5, por ₽500 |
| Aquisição especial em Blue | Compra no Mt. Moon Pokécenter, Nv.5, por ₽500 |
| Fonte específica | `data/pokemon/base_stats/magikarp.asm` |

### 130 Gyarados

| Campo | Valor |
|---|---|
| Nome/espécie | Gyarados (`DEX_GYARADOS`) |
| Categoria Pokédex | Atrocious |
| Descrição Pokédex | Rarely seen in the wild. Huge and vicious, it is capable of destroying entire cities in a rage |
| Altura | 21'04" (6,50 m) |
| Peso | 518,0 lb (235,0 kg) |
| Tipo | Water / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 214 / Slow |
| Atributos base | HP 95; Atk 125; Def 79; Spd 81; Spc 100; BST 480 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 297-389; Atk 252-344; Def 161-253; Spd 165-257; Spc 203-295 |
| Movimentos iniciais | Bite, Dragon Rage, Leer, Hydro Pump |
| Movimentos aprendidos por nível | Nv.20 Bite; Nv.25 Dragon Rage; Nv.32 Leer; Nv.41 Hydro Pump; Nv.52 Hyper Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Magikarp: Gyarados ao atingir Nv.20 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/gyarados.asm` |

### 131 Lapras

| Campo | Valor |
|---|---|
| Nome/espécie | Lapras (`DEX_LAPRAS`) |
| Categoria Pokédex | Transport |
| Descrição Pokédex | A Pokémon that has been overhunted almost to extinction. It can ferry people across the water |
| Altura | 8'02" (2,49 m) |
| Peso | 485,0 lb (220,0 kg) |
| Tipo | Water / Ice |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 219 / Slow |
| Atributos base | HP 130; Atk 85; Def 80; Spd 60; Spc 95; BST 450 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 366-458; Atk 173-265; Def 163-255; Spd 123-215; Spc 193-285 |
| Movimentos iniciais | Water Gun, Growl |
| Movimentos aprendidos por nível | Nv.16 Sing; Nv.20 Mist; Nv.25 Body Slam; Nv.31 Confuse Ray; Nv.38 Ice Beam; Nv.46 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM22 Solarbeam; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Presente no Silph Co. 7F, Nv.15 |
| Aquisição especial em Blue | Presente no Silph Co. 7F, Nv.15 |
| Fonte específica | `data/pokemon/base_stats/lapras.asm` |

### 132 Ditto

| Campo | Valor |
|---|---|
| Nome/espécie | Ditto (`DEX_DITTO`) |
| Categoria Pokédex | Transform |
| Descrição Pokédex | Capable of copying an enemy's genetic code to instantly transform itself into a duplicate of the enemy |
| Altura | 1'00" (0,30 m) |
| Peso | 9,0 lb (4,1 kg) |
| Tipo | Normal |
| Catch rate | 35; cenário normalizado: 4,72% (difícil) |
| EXP base / crescimento | 61 / Medium Fast |
| Atributos base | HP 48; Atk 48; Def 48; Spd 48; Spc 48; BST 240 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 204-296; Atk 100-192; Def 100-192; Spd 100-192; Spc 100-192 |
| Movimentos iniciais | Transform |
| Movimentos aprendidos por nível | Nenhum |
| Movimentos possíveis por TM/HM | Nenhum |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.53 (1,2%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.55 (4,3%), Nv.60 (1,2%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.63 (4,3%), Nv.65 (5,1%), Nv.67 (1,2%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.25 (5,1%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.33 (19,9%), Nv.38 (9,8%), Nv.43 (5,1%) |
| Spawns em Blue | Cerulean Cave 1F - terrestre/caverna, limiar 10/256: Nv.53 (1,2%)<br>Cerulean Cave 2F - terrestre/caverna, limiar 15/256: Nv.55 (4,3%), Nv.60 (1,2%)<br>Cerulean Cave B1F - terrestre/caverna, limiar 25/256: Nv.63 (4,3%), Nv.65 (5,1%), Nv.67 (1,2%)<br>Route 13 - terrestre/caverna, limiar 20/256: Nv.25 (5,1%)<br>Route 14 - terrestre/caverna, limiar 15/256: Nv.23 (15,2%)<br>Route 15 - terrestre/caverna, limiar 15/256: Nv.26 (19,9%)<br>Route 23 - terrestre/caverna, limiar 10/256: Nv.33 (19,9%), Nv.38 (9,8%), Nv.43 (5,1%) |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/ditto.asm` |

### 133 Eevee

| Campo | Valor |
|---|---|
| Nome/espécie | Eevee (`DEX_EEVEE`) |
| Categoria Pokédex | Evolution |
| Descrição Pokédex | Its genetic code is irregular. It may mutate if it is exposed to radiation from element STONEs |
| Altura | 1'00" (0,30 m) |
| Peso | 14,0 lb (6,4 kg) |
| Tipo | Normal |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 92 / Medium Fast |
| Atributos base | HP 55; Atk 55; Def 50; Spd 55; Spc 65; BST 280 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 217-309; Atk 113-205; Def 104-196; Spd 113-205; Spc 133-225 |
| Movimentos iniciais | Tackle, Sand-Attack |
| Movimentos aprendidos por nível | Nv.27 Quick Attack; Nv.31 Tail Whip; Nv.37 Bite; Nv.45 Take Down |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Flareon ao usar Fire Stone; nível mínimo 1; Jolteon ao usar Thunder Stone; nível mínimo 1; Vaporeon ao usar Water Stone; nível mínimo 1 |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Presente no Celadon Mansion Roof House, Nv.25 |
| Aquisição especial em Blue | Presente no Celadon Mansion Roof House, Nv.25 |
| Fonte específica | `data/pokemon/base_stats/eevee.asm` |

### 134 Vaporeon

| Campo | Valor |
|---|---|
| Nome/espécie | Vaporeon (`DEX_VAPOREON`) |
| Categoria Pokédex | Bubble Jet |
| Descrição Pokédex | Lives close to water. Its long tail is ridged with a fin which is often mistaken for a mermaid's |
| Altura | 3'03" (0,99 m) |
| Peso | 64,0 lb (29,0 kg) |
| Tipo | Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 196 / Medium Fast |
| Atributos base | HP 130; Atk 65; Def 60; Spd 65; Spc 110; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 366-458; Atk 133-225; Def 123-215; Spd 133-225; Spc 222-314 |
| Movimentos iniciais | Tackle, Sand-Attack, Quick Attack, Water Gun |
| Movimentos aprendidos por nível | Nv.27 Quick Attack; Nv.31 Water Gun; Nv.37 Tail Whip; Nv.40 Bite; Nv.42 Acid Armor; Nv.44 Haze; Nv.48 Mist; Nv.54 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Eevee: Vaporeon ao usar Water Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/vaporeon.asm` |

### 135 Jolteon

| Campo | Valor |
|---|---|
| Nome/espécie | Jolteon (`DEX_JOLTEON`) |
| Categoria Pokédex | Lightning |
| Descrição Pokédex | It accumulates negative ions in the atmosphere to blast out 10000volt lightning bolts |
| Altura | 2'07" (0,79 m) |
| Peso | 54,0 lb (24,5 kg) |
| Tipo | Electric |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 197 / Medium Fast |
| Atributos base | HP 65; Atk 65; Def 60; Spd 130; Spc 110; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 133-225; Def 123-215; Spd 262-354; Spc 222-314 |
| Movimentos iniciais | Tackle, Sand-Attack, Quick Attack, Thundershock |
| Movimentos aprendidos por nível | Nv.27 Quick Attack; Nv.31 Thundershock; Nv.37 Tail Whip; Nv.40 Thunder Wave; Nv.42 Double Kick; Nv.44 Agility; Nv.48 Pin Missile; Nv.54 Thunder |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Eevee: Jolteon ao usar Thunder Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/jolteon.asm` |

### 136 Flareon

| Campo | Valor |
|---|---|
| Nome/espécie | Flareon (`DEX_FLAREON`) |
| Categoria Pokédex | Flame |
| Descrição Pokédex | When storing thermal energy in its body, its temperature could soar to over 1600 degrees |
| Altura | 2'11" (0,89 m) |
| Peso | 55,0 lb (24,9 kg) |
| Tipo | Fire |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 198 / Medium Fast |
| Atributos base | HP 65; Atk 130; Def 60; Spd 65; Spc 110; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 262-354; Def 123-215; Spd 133-225; Spc 222-314 |
| Movimentos iniciais | Tackle, Sand-Attack, Quick Attack, Ember |
| Movimentos aprendidos por nível | Nv.27 Quick Attack; Nv.31 Ember; Nv.37 Tail Whip; Nv.40 Bite; Nv.42 Leer; Nv.44 Fire Spin; Nv.48 Rage; Nv.54 Flamethrower |
| Movimentos possíveis por TM/HM | TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Eevee: Flareon ao usar Fire Stone; nível mínimo 1 |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/flareon.asm` |

### 137 Porygon

| Campo | Valor |
|---|---|
| Nome/espécie | Porygon (`DEX_PORYGON`) |
| Categoria Pokédex | Virtual |
| Descrição Pokédex | A Pokémon that consists entirely of programming code. Capable of moving freely in cyberspace |
| Altura | 2'07" (0,79 m) |
| Peso | 80,0 lb (36,3 kg) |
| Tipo | Normal |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 130 / Medium Fast |
| Atributos base | HP 65; Atk 60; Def 70; Spd 40; Spc 75; BST 310 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 237-329; Atk 123-215; Def 143-235; Spd 84-176; Spc 153-245 |
| Movimentos iniciais | Tackle, Sharpen, Conversion |
| Movimentos aprendidos por nível | Nv.23 Psybeam; Nv.28 Recover; Nv.35 Agility; Nv.42 Tri Attack |
| Movimentos possíveis por TM/HM | HM05 Flash; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.26, por 9999 moedas |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.18, por 6500 moedas |
| Fonte específica | `data/pokemon/base_stats/porygon.asm` |

### 138 Omanyte

| Campo | Valor |
|---|---|
| Nome/espécie | Omanyte (`DEX_OMANYTE`) |
| Categoria Pokédex | Spiral |
| Descrição Pokédex | Although long extinct, in rare cases, it can be genetically resurrected from fossils |
| Altura | 1'04" (0,41 m) |
| Peso | 17,0 lb (7,7 kg) |
| Tipo | Rock / Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 120 / Medium Fast |
| Atributos base | HP 35; Atk 40; Def 100; Spd 35; Spc 90; BST 300 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 178-270; Atk 84-176; Def 203-295; Spd 74-166; Spc 183-275 |
| Movimentos iniciais | Water Gun, Withdraw |
| Movimentos aprendidos por nível | Nv.34 Horn Attack; Nv.39 Leer; Nv.46 Spike Cannon; Nv.53 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Omastar ao atingir Nv.40 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Reviver Helix Fossil no Cinnabar Lab, Nv.30 |
| Aquisição especial em Blue | Reviver Helix Fossil no Cinnabar Lab, Nv.30 |
| Fonte específica | `data/pokemon/base_stats/omanyte.asm` |

### 139 Omastar

| Campo | Valor |
|---|---|
| Nome/espécie | Omastar (`DEX_OMASTAR`) |
| Categoria Pokédex | Spiral |
| Descrição Pokédex | A prehistoric Pokémon that died out when its heavy shell made it impossible to catch prey |
| Altura | 3'03" (0,99 m) |
| Peso | 77,0 lb (34,9 kg) |
| Tipo | Rock / Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 199 / Medium Fast |
| Atributos base | HP 70; Atk 60; Def 125; Spd 55; Spc 115; BST 425 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 247-339; Atk 123-215; Def 252-344; Spd 113-205; Spc 232-324 |
| Movimentos iniciais | Water Gun, Withdraw, Horn Attack |
| Movimentos aprendidos por nível | Nv.34 Horn Attack; Nv.39 Leer; Nv.44 Spike Cannon; Nv.49 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Omanyte: Omastar ao atingir Nv.40 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/omastar.asm` |

### 140 Kabuto

| Campo | Valor |
|---|---|
| Nome/espécie | Kabuto (`DEX_KABUTO`) |
| Categoria Pokédex | Shellfish |
| Descrição Pokédex | A Pokémon that was resurrected from a fossil found in what was once the ocean floor eons ago |
| Altura | 1'08" (0,51 m) |
| Peso | 25,0 lb (11,3 kg) |
| Tipo | Rock / Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 119 / Medium Fast |
| Atributos base | HP 30; Atk 80; Def 90; Spd 55; Spc 45; BST 300 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 168-260; Atk 163-255; Def 183-275; Spd 113-205; Spc 94-186 |
| Movimentos iniciais | Scratch, Harden |
| Movimentos aprendidos por nível | Nv.34 Absorb; Nv.39 Slash; Nv.44 Leer; Nv.49 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Kabutops ao atingir Nv.40 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Reviver Dome Fossil no Cinnabar Lab, Nv.30 |
| Aquisição especial em Blue | Reviver Dome Fossil no Cinnabar Lab, Nv.30 |
| Fonte específica | `data/pokemon/base_stats/kabuto.asm` |

### 141 Kabutops

| Campo | Valor |
|---|---|
| Nome/espécie | Kabutops (`DEX_KABUTOPS`) |
| Categoria Pokédex | Shellfish |
| Descrição Pokédex | Its sleek shape is perfect for swimming. It slashes prey with its claws and drains the body fluids |
| Altura | 4'03" (1,30 m) |
| Peso | 89,0 lb (40,4 kg) |
| Tipo | Rock / Water |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 201 / Medium Fast |
| Atributos base | HP 60; Atk 115; Def 105; Spd 80; Spc 70; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 227-319; Atk 232-324; Def 212-304; Spd 163-255; Spc 143-235 |
| Movimentos iniciais | Scratch, Harden, Absorb |
| Movimentos aprendidos por nível | Nv.34 Absorb; Nv.39 Slash; Nv.46 Leer; Nv.53 Hydro Pump |
| Movimentos possíveis por TM/HM | HM03 Surf; TM02 Razor Wind; TM03 Swords Dance; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM17 Submission; TM19 Seismic Toss; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM40 Skull Bash; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Kabuto: Kabutops ao atingir Nv.40 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/kabutops.asm` |

### 142 Aerodactyl

| Campo | Valor |
|---|---|
| Nome/espécie | Aerodactyl (`DEX_AERODACTYL`) |
| Categoria Pokédex | Fossil |
| Descrição Pokédex | A ferocious, prehistoric Pokémon that goes for the enemy's throat with its serrated saw-like fangs |
| Altura | 5'11" (1,80 m) |
| Peso | 130,0 lb (59,0 kg) |
| Tipo | Rock / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 202 / Slow |
| Atributos base | HP 80; Atk 105; Def 65; Spd 130; Spc 60; BST 440 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 267-359; Atk 212-304; Def 133-225; Spd 262-354; Spc 123-215 |
| Movimentos iniciais | Wing Attack, Agility |
| Movimentos aprendidos por nível | Nv.33 Supersonic; Nv.38 Bite; Nv.45 Take Down; Nv.54 Hyper Beam |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM23 Dragon Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Reviver Old Amber no Cinnabar Lab, Nv.30 |
| Aquisição especial em Blue | Reviver Old Amber no Cinnabar Lab, Nv.30 |
| Fonte específica | `data/pokemon/base_stats/aerodactyl.asm` |

### 143 Snorlax

| Campo | Valor |
|---|---|
| Nome/espécie | Snorlax (`DEX_SNORLAX`) |
| Categoria Pokédex | Sleeping |
| Descrição Pokédex | Very lazy. Just eats and sleeps. As its rotund bulk builds, it becomes steadily more slothful |
| Altura | 6'11" (2,11 m) |
| Peso | 1014,0 lb (459,9 kg) |
| Tipo | Normal |
| Catch rate | 25; cenário normalizado: 3,41% (muito difícil) |
| EXP base / crescimento | 154 / Slow |
| Atributos base | HP 160; Atk 110; Def 65; Spd 30; Spc 65; BST 430 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 425-517; Atk 222-314; Def 133-225; Spd 64-156; Spc 133-225 |
| Movimentos iniciais | Headbutt, Amnesia, Rest |
| Movimentos aprendidos por nível | Nv.35 Body Slam; Nv.41 Harden; Nv.48 Double-Edge; Nv.56 Hyper Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM29 Psychic; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM46 Psywave; TM48 Rock Slide; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Route 12 - encontro estático capturável, Nv.30<br>Route 16 - encontro estático capturável, Nv.30 |
| Spawns em Blue | Route 12 - encontro estático capturável, Nv.30<br>Route 16 - encontro estático capturável, Nv.30 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/snorlax.asm` |

### 144 Articuno

| Campo | Valor |
|---|---|
| Nome/espécie | Articuno (`DEX_ARTICUNO`) |
| Categoria Pokédex | Freeze |
| Descrição Pokédex | A legendary bird Pokémon that is said to appear to doomed people who are lost in icy mountains |
| Altura | 5'07" (1,70 m) |
| Peso | 122,0 lb (55,3 kg) |
| Tipo | Ice / Flying |
| Catch rate | 3; cenário normalizado: 0,52% (muito difícil) |
| EXP base / crescimento | 215 / Slow |
| Atributos base | HP 90; Atk 85; Def 100; Spd 85; Spc 125; BST 485 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 173-265; Def 203-295; Spd 173-265; Spc 252-344 |
| Movimentos iniciais | Peck, Ice Beam |
| Movimentos aprendidos por nível | Nv.51 Blizzard; Nv.55 Agility; Nv.60 Mist |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Seafoam Islands B4F - encontro estático capturável, Nv.50 |
| Spawns em Blue | Seafoam Islands B4F - encontro estático capturável, Nv.50 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/articuno.asm` |

### 145 Zapdos

| Campo | Valor |
|---|---|
| Nome/espécie | Zapdos (`DEX_ZAPDOS`) |
| Categoria Pokédex | Electric |
| Descrição Pokédex | A legendary bird Pokémon that is said to appear from clouds while dropping enormous lightning bolts |
| Altura | 5'03" (1,60 m) |
| Peso | 116,0 lb (52,6 kg) |
| Tipo | Electric / Flying |
| Catch rate | 3; cenário normalizado: 0,52% (muito difícil) |
| EXP base / crescimento | 216 / Slow |
| Atributos base | HP 90; Atk 90; Def 85; Spd 100; Spc 125; BST 490 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 183-275; Def 173-265; Spd 203-295; Spc 252-344 |
| Movimentos iniciais | Thundershock, Drill Peck |
| Movimentos aprendidos por nível | Nv.51 Thunder; Nv.55 Agility; Nv.60 Light Screen |
| Movimentos possíveis por TM/HM | HM02 Fly; HM05 Flash; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Power Plant - encontro estático capturável, Nv.50 |
| Spawns em Blue | Power Plant - encontro estático capturável, Nv.50 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/zapdos.asm` |

### 146 Moltres

| Campo | Valor |
|---|---|
| Nome/espécie | Moltres (`DEX_MOLTRES`) |
| Categoria Pokédex | Flame |
| Descrição Pokédex | Known as the legendary bird of fire. Every flap of its wings creates a dazzling flash of flames |
| Altura | 6'07" (2,01 m) |
| Peso | 132,0 lb (59,9 kg) |
| Tipo | Fire / Flying |
| Catch rate | 3; cenário normalizado: 0,52% (muito difícil) |
| EXP base / crescimento | 217 / Slow |
| Atributos base | HP 90; Atk 100; Def 90; Spd 90; Spc 125; BST 495 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 287-379; Atk 203-295; Def 183-275; Spd 183-275; Spc 252-344 |
| Movimentos iniciais | Peck, Fire Spin |
| Movimentos aprendidos por nível | Nv.51 Leer; Nv.55 Agility; Nv.60 Sky Attack |
| Movimentos possíveis por TM/HM | HM02 Fly; TM02 Razor Wind; TM04 Whirlwind; TM06 Toxic; TM09 Take Down; TM10 Double-Edge; TM15 Hyper Beam; TM20 Rage; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM43 Sky Attack; TM44 Rest; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Victory Road 2F - encontro estático capturável, Nv.50 |
| Spawns em Blue | Victory Road 2F - encontro estático capturável, Nv.50 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/moltres.asm` |

### 147 Dratini

| Campo | Valor |
|---|---|
| Nome/espécie | Dratini (`DEX_DRATINI`) |
| Categoria Pokédex | Dragon |
| Descrição Pokédex | Long considered a mythical Pokémon until recently when a small colony was found living underwater |
| Altura | 5'11" (1,80 m) |
| Peso | 7,0 lb (3,2 kg) |
| Tipo | Dragon |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 67 / Slow |
| Atributos base | HP 41; Atk 64; Def 45; Spd 50; Spc 50; BST 250 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 190-282; Atk 131-223; Def 94-186; Spd 104-196; Spc 104-196 |
| Movimentos iniciais | Wrap, Leer |
| Movimentos aprendidos por nível | Nv.10 Thunder Wave; Nv.20 Agility; Nv.30 Slam; Nv.40 Dragon Rage; Nv.50 Hyper Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Dragonair ao atingir Nv.30 ou superior após ganho de nível |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Spawns em Blue | Super Rod - Safari Zone East, Safari Zone North, Safari Zone West, Safari Zone Center, Nv.15; 12,5% por uso (50% sem fisgada) |
| Aquisição especial em Red | Celadon Game Corner Prize, Nv.18, por 2800 moedas |
| Aquisição especial em Blue | Celadon Game Corner Prize, Nv.24, por 4600 moedas |
| Fonte específica | `data/pokemon/base_stats/dratini.asm` |

### 148 Dragonair

| Campo | Valor |
|---|---|
| Nome/espécie | Dragonair (`DEX_DRAGONAIR`) |
| Categoria Pokédex | Dragon |
| Descrição Pokédex | A mystical Pokémon that exudes a gentle aura. Has the ability to change climate conditions |
| Altura | 13'01" (3,99 m) |
| Peso | 36,0 lb (16,3 kg) |
| Tipo | Dragon |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 144 / Slow |
| Atributos base | HP 61; Atk 84; Def 65; Spd 70; Spc 70; BST 350 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 229-321; Atk 171-263; Def 133-225; Spd 143-235; Spc 143-235 |
| Movimentos iniciais | Wrap, Leer, Thunder Wave |
| Movimentos aprendidos por nível | Nv.10 Thunder Wave; Nv.20 Agility; Nv.35 Slam; Nv.45 Dragon Rage; Nv.55 Hyper Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM20 Rage; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Dragonite ao atingir Nv.55 ou superior após ganho de nível |
| Origem por evolução | Dratini: Dragonair ao atingir Nv.30 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/dragonair.asm` |

### 149 Dragonite

| Campo | Valor |
|---|---|
| Nome/espécie | Dragonite (`DEX_DRAGONITE`) |
| Categoria Pokédex | Dragon |
| Descrição Pokédex | An extremely rarely seen marine Pokémon. Its intelligence is said to match that of humans |
| Altura | 7'03" (2,21 m) |
| Peso | 463,0 lb (210,0 kg) |
| Tipo | Dragon / Flying |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 218 / Slow |
| Atributos base | HP 91; Atk 134; Def 95; Spd 80; Spc 100; BST 500 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 289-381; Atk 270-362; Def 193-285; Spd 163-255; Spc 203-295 |
| Movimentos iniciais | Wrap, Leer, Thunder Wave, Agility |
| Movimentos aprendidos por nível | Nv.10 Thunder Wave; Nv.20 Agility; Nv.35 Slam; Nv.45 Dragon Rage; Nv.60 Hyper Beam |
| Movimentos possíveis por TM/HM | HM03 Surf; HM04 Strength; TM02 Razor Wind; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM20 Rage; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Dragonair: Dragonite ao atingir Nv.55 ou superior após ganho de nível |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/dragonite.asm` |

### 150 Mewtwo

| Campo | Valor |
|---|---|
| Nome/espécie | Mewtwo (`DEX_MEWTWO`) |
| Categoria Pokédex | Genetic |
| Descrição Pokédex | It was created by a scientist after years of horrific gene splicing and DNA engineering experiments |
| Altura | 6'07" (2,01 m) |
| Peso | 269,0 lb (122,0 kg) |
| Tipo | Psychic |
| Catch rate | 3; cenário normalizado: 0,52% (muito difícil) |
| EXP base / crescimento | 220 / Slow |
| Atributos base | HP 106; Atk 110; Def 90; Spd 130; Spc 154; BST 590 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 318-410; Atk 222-314; Def 183-275; Spd 262-354; Spc 309-401 |
| Movimentos iniciais | Confusion, Disable, Swift, Psychic |
| Movimentos aprendidos por nível | Nv.63 Barrier; Nv.66 Psychic; Nv.70 Recover; Nv.75 Mist; Nv.81 Amnesia |
| Movimentos possíveis por TM/HM | HM04 Strength; HM05 Flash; TM01 Mega Punch; TM05 Mega Kick; TM06 Toxic; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM22 Solarbeam; TM24 Thunderbolt; TM25 Thunder; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM38 Fire Blast; TM40 Skull Bash; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Cerulean Cave B1F - encontro estático capturável, Nv.70 |
| Spawns em Blue | Cerulean Cave B1F - encontro estático capturável, Nv.70 |
| Aquisição especial em Red | Nenhuma aquisição especial |
| Aquisição especial em Blue | Nenhuma aquisição especial |
| Fonte específica | `data/pokemon/base_stats/mewtwo.asm` |

### 151 Mew

| Campo | Valor |
|---|---|
| Nome/espécie | Mew (`DEX_MEW`) |
| Categoria Pokédex | New Specie |
| Descrição Pokédex | So rare that it is still said to be a mirage by many experts. Only a few people have seen it worldwide |
| Altura | 1'04" (0,41 m) |
| Peso | 9,0 lb (4,1 kg) |
| Tipo | Psychic |
| Catch rate | 45; cenário normalizado: 6,04% (difícil) |
| EXP base / crescimento | 64 / Medium Slow |
| Atributos base | HP 100; Atk 100; Def 100; Spd 100; Spc 100; BST 500 |
| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |
| Atributos no Nv.99, mínimo-máximo | HP 307-399; Atk 203-295; Def 203-295; Spd 203-295; Spc 203-295 |
| Movimentos iniciais | Pound |
| Movimentos aprendidos por nível | Nv.10 Transform; Nv.20 Mega Punch; Nv.30 Metronome; Nv.40 Psychic |
| Movimentos possíveis por TM/HM | HM01 Cut; HM02 Fly; HM03 Surf; HM04 Strength; HM05 Flash; TM01 Mega Punch; TM02 Razor Wind; TM03 Swords Dance; TM04 Whirlwind; TM05 Mega Kick; TM06 Toxic; TM07 Horn Drill; TM08 Body Slam; TM09 Take Down; TM10 Double-Edge; TM11 Bubblebeam; TM12 Water Gun; TM13 Ice Beam; TM14 Blizzard; TM15 Hyper Beam; TM16 Pay Day; TM17 Submission; TM18 Counter; TM19 Seismic Toss; TM20 Rage; TM21 Mega Drain; TM22 Solarbeam; TM23 Dragon Rage; TM24 Thunderbolt; TM25 Thunder; TM26 Earthquake; TM27 Fissure; TM28 Dig; TM29 Psychic; TM30 Teleport; TM31 Mimic; TM32 Double Team; TM33 Reflect; TM34 Bide; TM35 Metronome; TM36 Selfdestruct; TM37 Egg Bomb; TM38 Fire Blast; TM39 Swift; TM40 Skull Bash; TM41 Softboiled; TM42 Dream Eater; TM43 Sky Attack; TM44 Rest; TM45 Thunder Wave; TM46 Psywave; TM47 Explosion; TM48 Rock Slide; TM49 Tri Attack; TM50 Substitute |
| Evolução e pré-requisito | Não possui evolução direta nesta ROM |
| Origem por evolução | Não é resultado de evolução |
| Spawns em Red | Nenhum encontro |
| Spawns em Blue | Nenhum encontro |
| Aquisição especial em Red | Sem obtenção normal nesta ROM; exige distribuição/evento ou meio externo |
| Aquisição especial em Blue | Sem obtenção normal nesta ROM; exige distribuição/evento ou meio externo |
| Fonte específica | `data/pokemon/base_stats/mew.asm` |

## 8. Controles de risco e não conformidades conhecidas

| ID | Risco ou condição | Controle requerido na reescrita |
|---|---|---|
| PKM-R01 | Confundir índice interno com número da Pokédex. | Usar um tipo distinto para `PokemonIndex` e `PokedexNumber`; testar `IndexToPokedex`. |
| PKM-R02 | Fundir dados Red e Blue. | Carregar `GameVersion` explicitamente e manter golden masters por versão. |
| PKM-R03 | Tratar Special como dois atributos. | Modelo Gen I deve possuir um único `Special`. |
| PKM-R04 | Calcular stats sem DV/Stat Exp ou com arredondamento real. | Reproduzir pisos intermediários e teto 999. |
| PKM-R05 | Interpretar nível 0 como jogável. | Mantê-lo apenas como caso técnico de fronteira. |
| PKM-R06 | Aplicar fórmula moderna de captura. | Usar o algoritmo de `ItemUseBall` e fixtures do documento de batalhas. |
| PKM-R07 | Conceder todos os golpes listados ao mesmo tempo. | Limitar moveset ativo a quatro e separar catálogo de estado da instância. |
| PKM-R08 | Ensinar TM/HM incompatível. | Validar o bitset de 55 posições da espécie. |
| PKM-R08A | Interpretar o bit `UNUSED` de Mew como um 56º item ensinável. | Ignorar o bit de preenchimento na API de domínio e preservá-lo apenas na serialização compatível. |
| PKM-R09 | Evoluir por pedra sem intenção. | Decidir e registrar modo compatível para o bug de `wCurItem`. |
| PKM-R10 | Considerar Mew normalmente disponível. | Marcar obtenção externa como requisito, sem inventar spawn. |
| PKM-R11 | Tratar chance de slot como chance total por passo. | Aplicar primeiro o limiar do mapa e depois o peso do slot. |
| PKM-R12 | Omitir escolhas mutuamente exclusivas. | Modelar starter, Fighting Dojo e Dome/Helix como decisões persistentes. |

## 9. Modelo de domínio para a reescrita em C

### 9.1 Bounded contexts

| Contexto | Responsabilidade |
|---|---|
| `SpeciesCatalog` | Dados imutáveis de espécie, tipos, base stats, crescimento e captura. |
| `MoveLearning` | Golpes iniciais, por nível e compatibilidade TM/HM. |
| `Evolution` | Regras, gatilhos, escolhas e resultado da transformação. |
| `Encounter` | Tabelas por versão, método, mapa, slot e nível. |
| `Acquisition` | Presentes, fósseis, prêmios e trocas NPC. |
| `PokemonInstance` | Nível, DV, Stat Exp, EXP, HP, status e moveset atual. |

### 9.2 SOLID e refatoração incremental

- **SRP:** separar parser de dados, cálculo de stats, encontro, evolução e captura.
- **OCP:** estratégias por `GameVersion` e método de encontro sem condicionais espalhadas.
- **LSP:** implementações ASM-oracle e C devem obedecer aos mesmos contratos observáveis.
- **ISP:** interfaces pequenas como `SpeciesRepository`, `StatCalculator` e `EncounterTable`.
- **DIP:** serviços de domínio dependem dessas interfaces, não do layout binário da ROM.
- Aplicar **Sprout Method/Class** e **Branch by Abstraction** para substituir uma regra
  por vez, mantendo golden masters antes de cada mudança estrutural.

## 10. Estratégia TDD e critérios de aceitação

| ID | Teste | Resultado esperado |
|---|---|---|
| PKM-T001 | Carregar catálogo | 151 espécies únicas e números 1..151. |
| PKM-T002 | Validar movimentos | Todo movimento referenciado pertence aos 165 IDs válidos. |
| PKM-T003 | Validar TM/HM | Exatamente 55 posições e nenhuma compatibilidade fora do bitset. |
| PKM-T004 | Validar evoluções | 72 entradas, alvos válidos e métodos/níveis preservados. |
| PKM-T005 | Stats Nv.0 | Toda espécie resulta em HP 10 e demais atributos 5. |
| PKM-T006 | Stats Nv.99 | Fixtures mínimas/máximas igualam `CalcStat`, inclusive teto 999. |
| PKM-T007 | Slots selvagens | Cada tabela ativa tem 10 slots e soma de pesos 256. |
| PKM-T008 | Versões | Exclusivos e níveis de prêmios correspondem a Red e Blue. |
| PKM-T009 | Pesca | Old sempre Magikarp; Good e Super reproduzem chance de não fisgar. |
| PKM-T010 | Captura por espécie | Catch rate carregado é idêntico ao cabeçalho base. |
| PKM-T011 | Evolução por nível/item/troca | Limiares e pré-condições são exercitados nas bordas N-1/N. |
| PKM-T012 | Golden master | Serialização C das 151 fichas é igual ao extrator ASM da mesma baseline. |

Ciclo recomendado de Kent Beck: escrever primeiro um exemplo mínimo falho, fazê-lo
passar com a menor implementação, refatorar sem alterar a saída e repetir por regra.

## 11. Rastreabilidade de requisitos

| Requisito | Evidência neste documento | Fonte principal | Testes |
|---|---|---|---|
| PKM-REQ-NOME | Nome e número | Seção 7 | `constants/pokedex_constants.asm` | PKM-T001 |
| PKM-REQ-DIM | Categoria, descrição, altura e peso | Seção 7 | `data/pokemon/dex_entries.asm`, `data/pokemon/dex_text.asm` | PKM-T012 |
| PKM-REQ-TIPO | Tipos | Seção 7 | `data/pokemon/base_stats/*.asm` | PKM-T012 |
| PKM-REQ-MOVE | Movimentos aprendidos/possíveis | Seções 5.3 e 7 | `data/pokemon/evos_moves.asm`, bitset `tmhm` | PKM-T002/003 |
| PKM-REQ-SPAWN | Local, nível, versão e chance | Seções 5.4 e 7 | `data/wild/**`, objetos e pesca | PKM-T007/008/009 |
| PKM-REQ-CATCH | Dificuldade de captura | Seções 5.2 e 7 | `BASE_CATCH_RATE`, `ItemUseBall` | PKM-T010 |
| PKM-REQ-EVO | Evolução e pré-requisitos | Seções 5.5 e 7 | `data/pokemon/evos_moves.asm` | PKM-T004/011 |
| PKM-REQ-STAT | Base, nível 0 e nível 99 | Seções 5.1 e 7 | `CalcStat` | PKM-T005/006 |
| PKM-REQ-ACQ | Presentes, prêmios e trocas | Seção 7 | scripts e `data/events/*` | PKM-T008/012 |

## 12. Manutenção, aprovação e Graphify

### 12.1 Regeneração

```bash
python3 tools/generate_pokemon_catalog.py
python3 tools/graphify_rgbds.py .
$(cat graphify-out/.graphify_python) -m graphify export html
```

Toda alteração nas fontes da Seção 4 exige: regenerar este arquivo, revisar o diff,
executar as validações, atualizar `graphify-out/graph.json` e `graphify-out/graph.html`
e registrar nova linha no histórico de revisão.

### 12.2 Checklist de aprovação

- [x] 151 espécies válidas presentes.
- [x] Dados Red e Blue processados separadamente.
- [x] Descrição, altura, peso, tipos, captura, stats, golpes e evolução rastreados.
- [x] Encontros terrestres, Surf, pesca e estáticos contemplados.
- [x] Aquisições especiais e indisponibilidade normal de Mew registradas.
- [x] Fórmulas e pressupostos dos níveis 0 e 99 declarados.
- [ ] Revisão técnica independente concluída.
- [ ] Aprovador e data de aprovação registrados.

## 13. Referências

- Código-fonte desta baseline, conforme fontes da Seção 4.
- `docs/001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md`.
- [ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html).
- [ISO 9001 em publicação](https://www.iso.org/standard/88464.html).
- [ISO: Guidance on documented information](https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/documented_information.pdf).
