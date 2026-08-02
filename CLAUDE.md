# CLAUDE.md

Leia e siga `AGENTS.md` antes de agir neste repositorio. Ele e a fonte canonica
das instrucoes para agentes.

Resumo operacional:

- Este projeto e a disassembly RGBDS de Pokemon Red/Blue.
- O objetivo local e entender o assembly e migrar comportamento aos poucos para
  C, preservando equivalencia.
- Trate o `.asm` atual como especificacao executavel.
- Antes de reescrever, caracterize comportamento, estado de memoria, bancos,
  inputs, outputs e efeitos colaterais.
- Use TDD no C novo, testes de caracterizacao contra o assembly e refactors
  pequenos no estilo Martin Fowler.
- Aplique SOLID de forma pragmatica em C: modulos coesos, headers pequenos,
  interfaces explicitas e inversao para hardware/RNG/input/video/audio.
- Use DDD com a linguagem do proprio jogo e dos labels existentes.
- O marco atual de batalha e pre-C: execute a suite em `rewrite/battle/` para
  Red e Blue e respeite `test_c_rewrite_gate.py` ate revisao humana explicita.
- Use Graphify como mapa vivo do codigo: consulte `graphify-out/graph.json`
  com `graphify query`, `graphify path` ou `graphify explain` antes de
  responder perguntas de arquitetura/fluxo. Neste repo, atualize com
  `$(cat graphify-out/.graphify_python) tools/graphify_rgbds.py .`, porque o
  Graphify padrao nao classifica `.asm`.
- Para mudancas em assembly ou layout, valide com `make DEBUG=1 compare` quando
  possivel.
