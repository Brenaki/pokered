---
type: "query"
date: "2026-08-01T19:41:36.094187+00:00"
question: "Quero documentar todas as informações sobre todas as IAs e compontamentos do NPCs que existem no jogo. Quero saber que algoritmo utilizam, quais tabelas são comparadas, se usa um perceptron simples para algo, ou apenas algoritmos deterministicos, etc. Quero também recomendações nessa reescrita para melhorar a IA dos npcs, podendo aprender o jeito que o jogador joga, andar pelo mapa, parar o jogador para conversar, e outras ações, se isso for possivel é claro, a ideia ainda é manter de forma fiel nessa reescrita, mas depois fazer modificações. Quero que descreva tudo o que foi solicitado com base na iso 9001 dentro da pasta docs colocar toda essa descrição em um arquivo markdown seguindo o padrão {numero com 3 digitos}-{ano}-{mes}-{dia}-{titulo_do_arquivo}.md (Exemplo: 003-2026-08-01-Funcionamento-das-IAs-Pokemon.md). No final commit e de push na main"
contributor: "graphify"
outcome: "useful"
source_nodes: ["AIEnemyTrainerChooseMoves", "TrainerAI", "TrainerAIPointers", "TrainerClassMoveChoiceModifications", "UpdateNPCSprite", "FindPathToPlayer", "TrainerWalkUpToPlayer", "TrainerEngage", "MoveSprite", "DisplayTextID"]
---

# Q: Quero documentar todas as informações sobre todas as IAs e compontamentos do NPCs que existem no jogo. Quero saber que algoritmo utilizam, quais tabelas são comparadas, se usa um perceptron simples para algo, ou apenas algoritmos deterministicos, etc. Quero também recomendações nessa reescrita para melhorar a IA dos npcs, podendo aprender o jeito que o jogador joga, andar pelo mapa, parar o jogador para conversar, e outras ações, se isso for possivel é claro, a ideia ainda é manter de forma fiel nessa reescrita, mas depois fazer modificações. Quero que descreva tudo o que foi solicitado com base na iso 9001 dentro da pasta docs colocar toda essa descrição em um arquivo markdown seguindo o padrão {numero com 3 digitos}-{ano}-{mes}-{dia}-{titulo_do_arquivo}.md (Exemplo: 003-2026-08-01-Funcionamento-das-IAs-Pokemon.md). No final commit e de push na main

## Answer

Query expandida com o vocabulario do grafo: [trainer, npc, movement, sight, battle, move, item, switch, random, script, collision, sprite]. A ROM não usa perceptron, rede neural nem aprendizado; usa regras e tabelas determinísticas, heurísticas de pontuação, RNG, máquinas de estado, sequências roteirizadas e um caminho guloso Manhattan. O documento controlado docs/003-2026-08-01-Funcionamento-das-IAs-Pokemon.md descreve IA de golpes, itens e trocas; TrainerAIPointers e modificadores por classe; movimento WALK/STAY, colisão, visão e abordagem; scripts e serviços; defeitos compatíveis; estratégia C com DDD, SOLID e TDD; e recomendações isoladas no modo ENHANCED para utility AI, modelo local do jogador, A*, agendas e conversas iniciadas por NPC. Inclui inventários gerados de 47 classes, 918 objetos, 322 cabeçalhos trainer e 199 estados SCRIPT_*.

## Outcome

- Signal: useful

## Source Nodes

- AIEnemyTrainerChooseMoves
- TrainerAI
- TrainerAIPointers
- TrainerClassMoveChoiceModifications
- UpdateNPCSprite
- FindPathToPlayer
- TrainerWalkUpToPlayer
- TrainerEngage
- MoveSprite
- DisplayTextID
- docs/003-2026-08-01-Funcionamento-das-IAs-Pokemon.md