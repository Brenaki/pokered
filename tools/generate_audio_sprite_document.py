#!/usr/bin/env python3
"""Generate the controlled audio and character graphics document from RGBDS sources."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/004-2026-08-01-Audio_Musicas_Efeitos_Sonoros_e_Sprites.md"
BASELINE_COMMIT = "28c9cf2e1f75c1cc5efdd76fdb34130b0bd380cd"


@dataclass(frozen=True)
class AudioConstant:
    identifier: str
    target: str
    bank: int
    line: int
    comment: str


@dataclass(frozen=True)
class AudioHeader:
    symbol: str
    bank: int
    channels: tuple[int, ...]
    pointers: tuple[str, ...]
    source: str
    line: int


@dataclass(frozen=True)
class MapSong:
    map_name: str
    music_id: str
    bank_symbol: str
    line: int


@dataclass(frozen=True)
class Cry:
    index: int
    base: str
    pitch: str
    length: str
    pokemon: str
    line: int


@dataclass(frozen=True)
class OverworldSprite:
    sprite_id: int
    identifier: str
    symbol: str
    tiles: int
    source_asset: str
    constant_line: int
    table_line: int


@dataclass(frozen=True)
class TrainerPicture:
    trainer_index: int
    symbol: str
    reward: int
    source_asset: str
    line: int


@dataclass(frozen=True)
class PictureAsset:
    symbol: str
    source_asset: str
    source: str
    line: int


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def md(value: object) -> str:
    return str(value).replace("|", "\\|")


def source_link(path: str, line: int | None = None) -> str:
    suffix = f":{line}" if line else ""
    return f"`{path}{suffix}`"


def parse_audio_constants() -> tuple[list[AudioConstant], list[AudioConstant]]:
    path = ROOT / "constants/music_constants.asm"
    pattern = re.compile(
        r"^\s*music_const\s+([A-Z0-9_]+),\s*([A-Za-z0-9_]+)(?:\s*;\s*(.*))?$"
    )
    current_bank = 0
    music: list[AudioConstant] = []
    sfx: list[AudioConstant] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        bank_match = re.match(r"^\s*; AUDIO_([123])\s*$", raw)
        if bank_match:
            current_bank = int(bank_match.group(1))
        match = pattern.match(raw)
        if not match:
            continue
        identifier, target, comment = match.groups()
        if identifier.startswith("MUSIC_"):
            item = AudioConstant(identifier, target, current_bank, line_no, comment or "")
            music.append(item)
        elif identifier.startswith("SFX_"):
            # Shared constants are encoded from engine 1, but availability is derived
            # independently from each engine's header table.
            item = AudioConstant(identifier, target, current_bank, line_no, comment or "")
            sfx.append(item)
    return music, sfx


def parse_headers(kind: str) -> list[AudioHeader]:
    headers: list[AudioHeader] = []
    for bank in (1, 2, 3):
        path = ROOT / f"audio/headers/{kind}headers{bank}.asm"
        lines = path.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines):
            match = re.match(r"^([A-Za-z0-9_]+)::$", lines[index])
            if not match or match.group(1) in {f"Music_Headers_{bank}", f"SFX_Headers_{bank}"}:
                index += 1
                continue
            symbol = match.group(1)
            source_line = index + 1
            channels: list[int] = []
            pointers: list[str] = []
            cursor = index + 1
            while cursor < len(lines) and not re.match(r"^[A-Za-z0-9_]+::$", lines[cursor]):
                channel = re.match(r"^\s*channel\s+(\d+),\s*([A-Za-z0-9_]+)", lines[cursor])
                if channel:
                    channels.append(int(channel.group(1)))
                    pointers.append(channel.group(2))
                cursor += 1
            if channels:
                headers.append(
                    AudioHeader(symbol, bank, tuple(channels), tuple(pointers), rel(path), source_line)
                )
            index = cursor
    return headers


def audio_data_sources() -> dict[str, str]:
    result: dict[str, str] = {}
    for directory in (ROOT / "audio/music", ROOT / "audio/sfx"):
        for path in sorted(directory.glob("*.asm")):
            for raw in path.read_text(encoding="utf-8").splitlines():
                match = re.match(r"^([A-Za-z0-9_]+)(?:::|:)$", raw)
                if match:
                    result.setdefault(match.group(1), rel(path))
    return result


def parse_map_songs() -> list[MapSong]:
    path = ROOT / "data/maps/songs.asm"
    pattern = re.compile(
        r"^\s*db\s+(MUSIC_[A-Z0-9_]+),\s*BANK\(([A-Za-z0-9_]+)\)\s*;\s*(.+?)\s*$"
    )
    result: list[MapSong] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = pattern.match(raw)
        if match:
            result.append(MapSong(match.group(3), match.group(1), match.group(2), line_no))
    return result


def parse_cries() -> list[Cry]:
    path = ROOT / "data/pokemon/cries.asm"
    pattern = re.compile(
        r"^\s*mon_cry\s+(SFX_CRY_[0-9A-F]+),\s*(\$[0-9A-F]+),\s*(\$[0-9A-F]+)\s*;\s*(.+?)\s*$",
        re.IGNORECASE,
    )
    result: list[Cry] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = pattern.match(raw)
        if match:
            result.append(Cry(len(result) + 1, *match.groups(), line_no))
    return result


def parse_incbin_assets(paths: list[str]) -> dict[str, PictureAsset]:
    result: dict[str, PictureAsset] = {}
    pending_labels: list[str] = []
    label_pattern = re.compile(r"^([A-Za-z0-9_]+)::$")
    incbin_pattern = re.compile(r'^([A-Za-z0-9_]+)::\s+INCBIN\s+"([^"]+)"')
    for source in paths:
        path = ROOT / source
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            inline = incbin_pattern.match(raw)
            if inline:
                symbol, asset = inline.groups()
                picture = PictureAsset(symbol, asset, source, line_no)
                result[symbol] = picture
                for alias in pending_labels:
                    result[alias] = picture
                pending_labels.clear()
                continue
            label = label_pattern.match(raw)
            if label:
                pending_labels.append(label.group(1))
            elif raw.strip() and not raw.lstrip().startswith(";"):
                pending_labels.clear()
    return result


def parse_overworld_sprites(assets: dict[str, PictureAsset]) -> list[OverworldSprite]:
    constants_path = ROOT / "constants/sprite_constants.asm"
    constants: list[tuple[int, str, int]] = []
    pattern = re.compile(r"^\s*const\s+(SPRITE_[A-Z0-9_]+)\s*;\s*\$([0-9a-f]+)", re.I)
    for line_no, raw in enumerate(constants_path.read_text(encoding="utf-8").splitlines(), 1):
        match = pattern.match(raw)
        if match and match.group(1) != "SPRITE_NONE":
            constants.append((int(match.group(2), 16), match.group(1), line_no))

    table_path = ROOT / "data/sprites/sprites.asm"
    rows: list[tuple[str, int, int]] = []
    row_pattern = re.compile(r"^\s*overworld_sprite\s+([A-Za-z0-9_]+),\s*(\d+)")
    for line_no, raw in enumerate(table_path.read_text(encoding="utf-8").splitlines(), 1):
        match = row_pattern.match(raw)
        if match:
            rows.append((match.group(1), int(match.group(2)), line_no))

    assert len(constants) == len(rows)
    result: list[OverworldSprite] = []
    for (sprite_id, identifier, const_line), (symbol, tiles, table_line) in zip(constants, rows):
        asset = assets[symbol].source_asset
        result.append(
            OverworldSprite(sprite_id, identifier, symbol, tiles, asset, const_line, table_line)
        )
    return result


def parse_trainer_pictures(assets: dict[str, PictureAsset]) -> list[TrainerPicture]:
    path = ROOT / "data/trainers/pic_pointers_money.asm"
    pattern = re.compile(r"^\s*pic_money\s+([A-Za-z0-9_]+),\s*(\d+)")
    result: list[TrainerPicture] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = pattern.match(raw)
        if match:
            symbol, reward = match.groups()
            result.append(
                TrainerPicture(
                    len(result) + 1,
                    symbol,
                    int(reward),
                    assets[symbol].source_asset,
                    line_no,
                )
            )
    return result


def parse_character_pictures(assets: dict[str, PictureAsset]) -> list[PictureAsset]:
    unique: dict[tuple[str, str], PictureAsset] = {}
    for picture in assets.values():
        if picture.source_asset.startswith(("gfx/pokemon/", "gfx/trainers/", "gfx/player/", "gfx/battle/oldman")):
            unique[(picture.symbol, picture.source_asset)] = picture
    return sorted(unique.values(), key=lambda item: (item.source_asset, item.symbol))


def parse_graphics_directory_counts() -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for path in (ROOT / "gfx").rglob("*.png"):
        counts[rel(path.parent)] += 1
    return sorted(counts.items())


def sfx_category(identifier: str) -> str:
    if identifier.startswith("SFX_NOISE_INSTRUMENT"):
        return "instrumento de ruido"
    if identifier.startswith("SFX_CRY_"):
        return "grito-base"
    if identifier.startswith("SFX_BATTLE_") or identifier in {
        "SFX_PECK", "SFX_FAINT_FALL", "SFX_POUND", "SFX_DAMAGE",
        "SFX_NOT_VERY_EFFECTIVE", "SFX_VINE_WHIP", "SFX_SUPER_EFFECTIVE",
        "SFX_DOUBLESLAP", "SFX_HORN_DRILL", "SFX_PSYBEAM", "SFX_PSYCHIC_M",
        "SFX_TRAINER_APPEARED",
    }:
        return "batalha"
    if identifier.startswith("SFX_INTRO_") or identifier.startswith("SFX_SLOTS_") or identifier == "SFX_SHOOTING_STAR":
        return "intro/slots"
    if identifier in {
        "SFX_LEVEL_UP", "SFX_BALL_TOSS", "SFX_BALL_POOF", "SFX_FAINT_THUD",
        "SFX_RUN", "SFX_DEX_PAGE_ADDED", "SFX_CAUGHT_MON",
    }:
        return "batalha/fanfara"
    return "interface/mundo"


def normalized_sfx_symbol(symbol: str) -> str:
    return re.sub(r"_[123]$", "", symbol)


def validate(
    music: list[AudioConstant],
    sfx: list[AudioConstant],
    music_headers: list[AudioHeader],
    sfx_headers: list[AudioHeader],
    map_songs: list[MapSong],
    cries: list[Cry],
    sprites: list[OverworldSprite],
    trainers: list[TrainerPicture],
    directory_counts: list[tuple[str, int]],
) -> None:
    assert len(music) == 45, f"Expected 45 addressable music IDs, found {len(music)}"
    assert len(music_headers) == 45, f"Expected 45 music headers, found {len(music_headers)}"
    assert len(sfx) == 161, f"Expected 161 SFX IDs, found {len(sfx)}"
    assert len(sfx_headers) == 317, f"Expected 317 engine-specific SFX headers, found {len(sfx_headers)}"
    assert len(map_songs) == 248, f"Expected 248 map-song rows, found {len(map_songs)}"
    assert len(cries) == 190, f"Expected 190 internal cry rows, found {len(cries)}"
    assert len(sprites) == 72, f"Expected 72 overworld sprite IDs, found {len(sprites)}"
    assert len({sprite.source_asset for sprite in sprites}) == 66
    assert len(trainers) == 47, f"Expected 47 trainer classes, found {len(trainers)}"
    assert len({trainer.source_asset for trainer in trainers}) == 45
    counts = dict(directory_counts)
    assert sum(counts.values()) == 668
    assert counts["gfx/sprites"] == 67
    assert counts["gfx/trainers"] == 45
    assert counts["gfx/pokemon/front"] == 153
    assert counts["gfx/pokemon/front_rg"] == 153
    assert counts["gfx/pokemon/back"] == 151
    assert Counter(track.bank for track in music) == {1: 20, 2: 7, 3: 18}
    assert Counter(header.bank for header in music_headers) == {1: 20, 2: 7, 3: 18}
    assert sum(cry.pokemon == "MissingNo." for cry in cries) == 39


def add_table(lines: list[str], headers: tuple[str, ...], rows: list[tuple[object, ...]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(md(value) for value in row) + " |")
    lines.append("")


def build_document() -> str:
    music, sfx = parse_audio_constants()
    music_headers = parse_headers("music")
    sfx_headers = parse_headers("sfx")
    map_songs = parse_map_songs()
    cries = parse_cries()
    assets = parse_incbin_assets(["gfx/pics.asm", "gfx/sprites.asm", "data/pokemon/mew.asm"])
    sprites = parse_overworld_sprites(assets)
    trainers = parse_trainer_pictures(assets)
    character_pictures = parse_character_pictures(assets)
    directory_counts = parse_graphics_directory_counts()
    validate(
        music, sfx, music_headers, sfx_headers, map_songs, cries, sprites, trainers,
        directory_counts,
    )

    data_sources = audio_data_sources()
    music_header_by_symbol = {header.symbol: header for header in music_headers}
    sfx_availability: dict[str, list[AudioHeader]] = defaultdict(list)
    for header in sfx_headers:
        sfx_availability[normalized_sfx_symbol(header.symbol)].append(header)

    lines: list[str] = []
    lines.extend(
        f"""# Audio, musicas, efeitos sonoros e sprites de Pokemon Red/Blue

## Controle do documento

| Campo | Valor |
|---|---|
| Identificacao | AV-004 |
| Arquivo | `004-2026-08-01-Audio_Musicas_Efeitos_Sonoros_e_Sprites.md` |
| Revisao | 1.0 |
| Data de emissao | 2026-08-01 |
| Situacao | Emitido para revisao e uso tecnico interno |
| Responsavel pelo processo | Equipe de reescrita ASM para C |
| Elaborado por | Gerador deterministico, Graphify e verificacao direta do codigo-fonte |
| Aprovador | Pendente de designacao |
| Baseline do codigo | commit `{BASELINE_COMMIT}` |
| Abrangencia | Audio, musicas, SFX, gritos, sprites, imagens de batalha e fluxo de renderizacao da ROM Red/Blue |
| Classificacao | Informacao documentada interna |

### Historico de revisoes

| Revisao | Data | Alteracao | Autor | Aprovacao |
|---|---|---|---|---|
| 1.0 | 2026-08-01 | Emissao inicial, arquitetura, riscos e inventarios extraidos do codigo | Codex | Pendente |

## 1. Finalidade e relacao com a ISO 9001

Este documento preserva o conhecimento necessario para reescrever gradualmente em C
os subsistemas de audio e apresentacao visual. Ele estabelece escopo, responsaveis,
fontes, criterios verificaveis, riscos, controles de mudanca e evidencias de teste.

A organizacao segue principios de abordagem de processo, pensamento baseado em risco,
rastreabilidade, controle de informacao documentada e melhoria continua inspirados na
ISO 9001. Isso **nao declara certificacao nem conformidade formal** do repositorio,
produto ou documento. Em 2026-08-01, a referencia publicada e a
[ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html); a
[sexta edicao estava em publicacao, prevista para 2026-09](https://www.iso.org/standard/88464.html).
Tambem foram consideradas a orientacao oficial sobre
[informacao documentada](https://www.iso.org/files/live/sites/isoorg/files/standards/docs/en/iso_9001_2015_guidance_documented_information.pdf)
e a [ISO 10013:2021](https://www.iso.org/standard/75736.html).

## 2. Escopo

### 2.1 Incluido

- os tres motores de audio, suas tabelas, comandos, bancos e estado em RAM;
- 45 IDs de musica enderecaveis, 161 IDs de SFX, 38 gritos-base, 190 entradas
  internas de grito e 248 associacoes de mapa para musica;
- selecao de musica de mapa, bicicleta, surfe, batalha, fanfarra e alarme de HP;
- pipeline de PNG para 1bpp/2bpp e `.pic`, compressao e descompressao em runtime;
- 72 IDs de sprite de overworld, 47 classes de treinador e imagens de Pokemon;
- tiles, tilemaps, paletas DMG/SGB, VRAM, shadow OAM, DMA, animacao, scroll e culling;
- o tratamento do mundo e de objetos que estao fora do viewport;
- recomendacoes SOLID, DDD, Refactoring e TDD para modo fiel e melhorias posteriores.

### 2.2 Excluido

- analise musical subjetiva, partitura convencional ou transcricao para formatos MIDI/WAV;
- garantia de comportamento analogico identico em todo emulador ou dispositivo de audio;
- arte de Pokemon Yellow, geracoes posteriores ou recursos que nao participam deste build;
- licenca para redistribuir propriedade intelectual; isso exige avaliacao juridica separada;
- afirmacao de intencao dos autores quando somente o efeito do codigo pode ser observado.

## 3. Objetivos e criterios da qualidade

| ID | Objetivo | Criterio verificavel |
|---|---|---|
| AV-Q01 | Cobertura de audio | 45 musicas, 161 SFX, 317 headers de SFX por motor e 190 gritos inventariados. |
| AV-Q02 | Cobertura visual | 72 IDs de overworld, 47 classes de treinador e 668 PNGs contabilizados. |
| AV-Q03 | Fidelidade | Mesmos eventos e frames produzem os mesmos writes de APU, VRAM, tilemap e OAM no modo fiel. |
| AV-Q04 | Rastreabilidade | Cada processo aponta para arquivo, simbolo, tabela ou inventario de origem. |
| AV-Q05 | Reprodutibilidade | `python3 tools/generate_audio_sprite_document.py --check` nao encontra divergencia. |
| AV-Q06 | Separacao de melhoria | Recursos modernos permanecem sob `ENHANCED`, sem mudar traces de `GEN1_FIDELITY`. |
| AV-Q07 | Controle de contexto | Mudancas relevantes regeneram este documento e o grafo Graphify/HTML. |

## 4. Conclusao executiva

O repositorio nao armazena faixas PCM, MP3, WAV ou MIDI. Musicas, efeitos e gritos
sao **programas compactos de comandos** interpretados uma vez por VBlank e convertidos
em escritas nos quatro canais da APU do Game Boy: dois pulsos, uma forma de onda
programavel e ruido. Quatro canais de software atendem musica (`CHAN1..CHAN4`) e
quatro atendem efeitos (`CHAN5..CHAN8`) sobre o mesmo hardware; o efeito ativo pode
preemptar a voz musical correspondente.

Os graficos-fonte sao PNGs convertidos no build para tiles 1bpp/2bpp. Imagens grandes
de Pokemon e treinadores recebem compressao `.pic`, sao descomprimidas em SRAM/WRAM,
centralizadas em uma area 7x7 e copiadas para VRAM. Pokemon e treinadores exibidos na
batalha usam principalmente o mapa de tiles do **background**, mesmo sendo chamados
de sprites no codigo. Personagens de mapa usam OAM: cada figura 16x16 consome quatro
objetos 8x8 montados a partir de tabelas de direcao e quadro.

Objetos fora da tela nao sao renderizados para um framebuffer oculto. O jogo mantem
estado logico em WRAM, marca sprites fora do viewport com `IMAGEINDEX = $ff`, conserva
um mapa de mundo com bordas/conexoes e atualiza somente faixas que entram no mapa de
background circular 32x32. A tela mostra 20x18 tiles. Portanto, simulacao, conjunto
de tiles residente e visibilidade sao conceitos diferentes.

## 5. Visao arquitetural

```mermaid
flowchart LR
    Event[PlaySound/PlayMusic/PlayCry] --> Bank[Banco de audio ativo]
    Bank --> Header[Header: canais e ponteiros]
    Header --> Seq[Interpretador de comandos]
    Seq --> APU[Registradores APU]
    VBlank[VBlank] --> Seq
    PNG[PNG fonte] --> RGBGFX[rgbgfx: 1bpp/2bpp]
    RGBGFX --> Compress[pkmncompress para .pic]
    Compress --> ROM[Assets em ROM]
    ROM --> Decode[UncompressSpriteData]
    Decode --> VRAM[Patterns em VRAM]
    State[Estado logico WRAM] --> Cull[Visibilidade e facing]
    Cull --> Shadow[Shadow OAM]
    Shadow --> DMA[DMA para OAM]
    VRAM --> LCD[Background/objetos no LCD]
```

| Processo | Fontes principais | Simbolos/artefatos |
|---|---|---|
| API de audio | `home/audio.asm`, `home/pokemon.asm` | `PlaySound`, `PlayMusic`, `PlayDefaultMusic`, `PlayCry`, `GetCryData` |
| Atualizacao | `home/vblank.asm`, `home/fade_audio.asm` | `VBlank`, `FadeOutAudio`, `Audio1/2/3_UpdateMusic` |
| Interpretador | `audio/engine_1.asm`, `engine_2.asm`, `engine_3.asm` | `PlayNextNote`, `GetNextMusicByte`, `PlaySound` de cada motor |
| Linguagem dos dados | `macros/scripts/audio.asm`, `audio/notes.asm` | notas, pausas, tempo, vibrato, loops, chamadas e retorno |
| Catalogos | `constants/music_constants.asm`, `audio/headers/*.asm`, `data/maps/songs.asm` | IDs, headers e banco |
| Gritos | `data/pokemon/cries.asm`, `audio/sfx/cry*.asm` | `CryData`, 38 gritos-base e modificadores |
| Build grafico | `Makefile`, `tools/gfx.c`, `tools/pkmncompress.c` | PNG -> 1bpp/2bpp -> `.pic` |
| Descompressao | `home/uncompress.asm`, `home/pics.asm` | `UncompressSpriteData`, buffers SRAM, merge 2bpp |
| Sprites de mapa | `engine/overworld/map_sprites.asm`, `data/sprites/*.asm` | sets, ponteiros, facings, slots VRAM |
| OAM | `engine/gfx/sprite_oam.asm`, `engine/gfx/oam_dma.asm` | `PrepareOAMData`, `wShadowOAM`, `hDMARoutine` |
| Background | `home/vcopy.asm`, `engine/overworld/load_map.asm` | copia por VBlank e redesenho de linha/coluna |
| Memoria de video | `ram/vram.asm`, `ram/wram.asm` | unions de VRAM, `wTileMap`, estados e buffers |
| Batalha | `engine/battle/core.asm`, `gfx/pics.asm` | `vFrontPic`, `vBackPic`, tilemap 7x7, trainer pics |
| Paletas | `home/palettes.asm`, `engine/gfx/palettes.asm`, `data/sgb/sgb_palettes.asm` | DMG BGP/OBP e pacotes SGB |

## 6. Subsistema de audio

### 6.1 Modelo de execucao

`PlayMusic` registra o novo ID, cancela fade pendente e escolhe o banco. `PlaySound`
preserva registradores, troca temporariamente para `wAudioROMBank`, despacha para
`Audio1_PlaySound`, `Audio2_PlaySound` ou `Audio3_PlaySound` e restaura o banco anterior.
Durante fade, o novo som fica pendente ate `FadeOutAudio` reduzir os dois nibbles do
volume mestre e trocar para `wAudioSavedROMBank`.

No VBlank, depois das transferencias de video, OAM DMA e preparacao do proximo shadow
OAM, a rotina executa fade e uma atualizacao do motor de audio. O motor 2 executa antes
`Music_DoLowHealthAlarm`. `UpdateMusic6Times` adianta o sequenciador ao entrar em mapa,
uma particularidade que deve permanecer em traces de fidelidade.

### 6.2 Canais e concorrencia

| Software | Hardware compartilhado | Uso |
|---|---|---|
| `CHAN1` e `CHAN5` | Pulso 1, com sweep | musica e SFX/grito |
| `CHAN2` e `CHAN6` | Pulso 2 | musica e SFX/grito |
| `CHAN3` e `CHAN7` | Wave RAM | musica e SFX |
| `CHAN4` e `CHAN8` | Ruido | musica, bateria, SFX e grito |

O loop percorre oito estruturas de canal. Quando o SFX correspondente esta ativo,
ele ocupa o canal fisico usado pela musica. A prioridade de substituicao e decidida
pelos IDs nos headers; gritos inicializam os canais 5 a 8 e usam normalmente 5, 6 e 8.
O alarme de HP baixo escreve diretamente no pulso 1 e pode sobrepor outros sons desse
canal. `WaitForSoundToFinish` observa os canais 5, 6 e 8, mas retorna imediatamente
quando o alarme esta habilitado.

### 6.3 Linguagem de comandos

| Grupo | Macros | Efeito |
|---|---|---|
| Headers | `channel_count`, `channel` | numero de vozes e ponteiro inicial de cada canal |
| Notas SFX | `square_note`, `noise_note` | duracao, volume/envelope e frequencia |
| Notas musicais | `note`, `drum_note`, `rest` | pitch/instrumento e comprimento de 1 a 16 unidades |
| Articulacao | `note_type`, `drum_speed`, `octave`, `duty_cycle` | velocidade, envelope, oitava e ciclo de pulso |
| Modulacao | `pitch_sweep`, `vibrato`, `pitch_slide`, `toggle_perfect_pitch` | alteracao temporal da frequencia |
| Mix | `stereo_panning`, `volume`, `execute_music` | roteamento, volume mestre e modo de interpretacao |
| Controle | `tempo`, `duty_cycle_pattern`, `sound_call`, `sound_loop`, `sound_ret` | temporizacao, subrotinas e repeticao |

`PlayNextNote` continua consumindo comandos de duracao zero ate encontrar nota ou
pausa. `GetNextMusicByte` le pelo ponteiro do canal. `CalculateFrequency` consulta
`audio/notes.asm` e ajusta pela oitava. A duracao usa parte inteira e fracionaria por
canal, efetivamente ponto fixo 8.8 baseado em comprimento, velocidade e tempo. O
macro `tempo` grava big-endian e alerta que valores acima de `$100`, combinados com
notas longas/lentas, podem estourar o calculo original.

No canal wave, a saida e desabilitada, 16 bytes (32 amostras de 4 bits) sao copiados
para `_AUD3WAVERAM` e o canal e reativado. Existem seis formas `.wave0` a `.wave5`;
o vetor tem nove ponteiros, dos quais quatro apontam para `.wave5` e tres desses sao
marcados como nao usados. A forma 5 vem dos dados de SFX e difere conforme o banco.

### 6.4 Musica contextual e batalha

`data/maps/songs.asm` define ID e banco para cada mapa. `PlayDefaultMusic` usa essa
associacao ao caminhar, mas substitui por `MUSIC_BIKE_RIDING` ou `MUSIC_SURFING` de
acordo com `wWalkBikeSurfState`. `PlayBattleMusic` escolhe musica selvagem, treinador,
lider ou batalha final e usa o motor 2. Finais de batalha e curas usam musicas curtas
ou fanfarras pelos mesmos headers.

Ha 45 faixas com ID/header: 20 no motor 1, 7 no motor 2 e 18 no motor 3. O arquivo
`audio/music/unusedsong.asm` contem `Music_UnusedSong`, incluido na ROM, mas sem header
e sem constante enderecavel. `Music_PokeFluteInBattle` e outro caso especial: altera
ponteiros do canal diretamente em vez de ser uma musica normal do catalogo.

### 6.5 Gritos de Pokemon

`PlayCry` chama `GetCryData`, que indexa `CryData` pelo indice interno da especie,
carrega grito-base, modificador de frequencia e modificador de tempo, converte o
grito para o deslocamento de header de tres canais e chama `PlaySound`. A tabela tem
190 entradas internas: 151 especies e 39 slots `MissingNo.`. As especies reutilizam
38 programas-base (`SFX_CRY_00` a `SFX_CRY_25`) com pitch e comprimento diferentes;
nao existem 151 gravacoes PCM independentes.

### 6.6 Estado persistente do motor

O bloco inicial de `ram/wram.asm` guarda IDs, flags, ponteiros de comandos e retornos,
duty, vibrato, pitch slide, contadores inteiro/fracionario, oitavas, volumes, tempos,
instrumentos wave, bancos atual/salvo e modificadores de grito. Mais adiante ficam os
contadores de fade e o alarme de HP. `wMuteAudioAndPauseMusic` silencia a saida e pausa
a musica; conforme o contrato documentado no WRAM, SFX continua a ser processado.

## 7. Pipeline de graficos e sprites

### 7.1 Build dos assets

1. O PNG e a fonte controlada e legivel por ferramentas.
2. A regra generica do `Makefile` executa `rgbgfx --colors dmg` para gerar 2bpp ou
   `--depth 1` para 1bpp.
3. Regras especificas chamam `tools/gfx` para trim, remocao de duplicatas, flips,
   interlace ou preservacao de indices quando necessario.
4. Imagens quadradas de Pokemon/treinadores viram `.pic` por `tools/pkmncompress`.
5. Os `.2bpp`, `.1bpp` e `.pic` entram em ROM por `INCBIN`.

`pkmncompress` separa planos, escolhe ordem/modos e aplica codificacao compacta com
RLE e transformacoes diferenciais. `home/uncompress.asm` faz o inverso em runtime:
le dimensoes do primeiro byte, decodifica dois chunks 1bpp nos buffers SRAM
`sSpriteBuffer1/2` e restaura os planos. `LoadUncompressedSpriteData` centraliza cada
plano em 7x7, zera margens e intercala os bytes em 2bpp antes da copia para VRAM.

### 7.2 Imagens de Pokemon e treinadores

`UncompressMonSprite` le o ponteiro do header da especie e seleciona os bancos
`Pics 1` a `Pics 5` por faixa do indice interno, com casos especiais para Mew e o
fossil de Kabutops. `LoadMonFrontSprite` envia a imagem centralizada para `vFrontPic`.
Back pics de Pokemon partem de 4x4 e `ScaleSpriteByTwo` as amplia para a area 7x7.

`_LoadTrainerPic` usa `TrainerPicAndMoneyPointers` para localizar a imagem comprimida;
em link pode carregar `RedPicFront`. `CopyUncompressedPicToTilemap` escreve os 49 IDs
de tile 7x7. Assim, as grandes figuras de batalha sao patterns de background, nao
objetos OAM tradicionais. Durante a transicao, o mapa de background 32x32 e limpo e
somente as 20 colunas visiveis de cada uma das 18 linhas sao copiadas. Em uma etapa
da introducao, o corpo/inimigo permanece no background e a cabeca do jogador usa OAM
para contornar o scroll por scanline.

Os 153 PNGs em `gfx/pokemon/front` sao 151 especies mais os dois fosseis. Os 151
backs ficam em `gfx/pokemon/back`. `gfx/pokemon/front_rg` tambem possui 153 PNGs, mas
nao e referenciado pelo `Makefile`, `gfx/pics.asm` ou headers desta baseline; deve ser
tratado como acervo alternativo, nao como entrada ativa deste build.

### 7.3 Personagens de overworld

Cada personagem movel tem 12 tiles: quatro olhando para baixo, quatro para cima e
quatro para a esquerda. A direita reutiliza a esquerda com X-flip. `facings.asm`
combina quatro tiles em 16x16 e define standing/walking; quadros 0 e 2 compartilham a
pose parada e o quadro 3 usa flips adicionais para passos. Objetos estaticos com ID
a partir de `FIRST_STILL_SPRITE` usam quatro tiles e a mesma composicao em todas as
direcoes.

`InitMapSprites` carrega sets fixos de 11 tipos em mapas externos e os picture IDs
presentes em mapas internos. IDs repetidos compartilham o slot. O jogador ocupa o
primeiro slot; ate dez slots normais de 12 tiles sao alocados, e dois objetos de
quatro tiles usam as regioes `$78` e `$7c`. Metade inferior guarda poses paradas e a
metade superior, deslocada em `$800`, guarda caminhada.

`LoadPlayerSpriteGraphics` escolhe `RedSprite`, `RedBikeSprite` ou `SeelSprite`
conforme caminhar/bicicleta/surfe. Quando a fonte de texto ocupa a metade superior da
VRAM, o movimento de NPC e restringido e os tiles de caminhada sao recarregados por
`CopyVideoData` com o LCD ligado. Isso e um acoplamento de memoria importante para o
modo fiel, mesmo que uma implementacao moderna nao precise reproduzir a escassez.

### 7.4 Paletas

No Game Boy monocromatico, `rBGP`, `rOBP0` e `rOBP1` mapeiam os quatro valores 2bpp
para tons. No Super Game Boy, `engine/gfx/palettes.asm` envia comandos/pacotes apenas
quando `wOnSGB` esta ativo; `MonsterPalettes` associa especies a IDs e
`data/sgb/sgb_palettes.asm` fornece as paletas de quatro cores. Paleta nao altera os
pixels-fonte: ela interpreta os indices dos tiles na exibicao.

## 8. O que acontece fora da tela

### 8.1 Estado logico, viewport e VRAM

| Camada | Estrutura | Comportamento |
|---|---|---|
| Mundo | `wOverworldMap` e `wSurroundingTiles` | blocos do mapa atual, bordas e conexoes permanecem em WRAM |
| Viewport logico | `wTileMap` | buffer de 20x18 tiles usado por menus, batalha e copias automaticas |
| Background fisico | `vBGMap0/vBGMap1` | mapas circulares 32x32, maiores que a tela visivel |
| Objetos logicos | `wSpriteStateData1/2` | 16 estruturas, jogador mais ate 15 objetos de mapa |
| Objetos visiveis | `wShadowOAM` -> OAM | no maximo 40 entradas de hardware; quatro por personagem 16x16 |
| Patterns | `vNPCSprites`, `vSprites`, `vFrontPic`, `vBackPic` | tiles residentes e reutilizados conforme o modo atual |

`CheckSpriteAvailability` calcula posicao relativa ao jogador e verifica flags,
limites e cobertura por texto. Fora da regiao visivel, grava `$ff` no image index.
`PrepareOAMData` ainda pode atualizar coordenadas calculadas, mas nao emite as quatro
entradas OAM; entradas restantes recebem Y invisivel. O estado do objeto continua em
WRAM, e a logica de movimento padrao pode ser limitada pela invisibilidade. Scripts
de mapa continuam capazes de manipular esse estado.

Ao caminhar, `RedrawRowOrColumn` transfere somente a linha ou coluna de dois tiles que
acabou de entrar no viewport e faz wrap no background 32x32. Em telas estaticas,
`AutoBgMapTransfer` copia um terco dos 20x18 tiles por VBlank, completando em tres
frames. `CopyVideoData` agenda no maximo oito tiles por frame e suspende a copia
automatica enquanto trabalha. Agua e flores alteram patterns diretamente na VRAM.

### 8.2 Ordem de OAM e latencia

No VBlank, `hDMARoutine` primeiro copia `wShadowOAM` preparado no frame anterior para
OAM; depois `PrepareOAMData` monta o buffer para o proximo DMA. O codigo da DMA roda
em HRAM porque o barramento restringe outros acessos durante a transferencia. Uma
reescrita fiel precisa modelar essa preparacao em dois estagios; uma reescrita moderna
pode renderizar no mesmo frame somente no modo melhorado e com teste visual explicito.

### 8.3 Reuso por modo

`ram/vram.asm` declara `UNION`: as mesmas faixas fisicas recebem nomes diferentes em
batalha/menu, overworld e titulo. `vFrontPic` pode ocupar o mesmo endereco que parte
de outro conjunto de characters em outro modo. Nao se deve traduzir cada alias para
uma alocacao C independente no emulador fiel sem preservar os efeitos de sobreposicao.
Em um renderer moderno, os aliases podem virar recursos separados se o adaptador de
compatibilidade mantiver os mesmos resultados observaveis.

## 9. Reescrita incremental em C

### 9.1 Contextos DDD e portas

| Contexto | Responsabilidade | Portas recomendadas |
|---|---|---|
| `AudioCatalog` | IDs, headers, mapas, gritos e assets | `AudioAssetSource`, `RomBankReader` |
| `AudioSequencer` | comandos, tempo, loops, prioridade e fade | `FrameClock`, `ApuRegisterSink` |
| `BattlePresentation` | imagens 7x7, HUD e transicoes | `PictureDecoder`, `TileSurface` |
| `OverworldScene` | estado, culling, facing e animacao | `MapView`, `SpriteCatalog` |
| `VideoMemory` | VRAM, tilemaps, OAM e transferencias | `VideoBus`, `DmaSink` |
| `AssetPipeline` | PNG, tiles, compressao e manifests | `ImageConverter`, `AssetWriter` |

No modo fiel, `ApuRegisterSink` e `VideoBus` registram os mesmos writes por frame da
ROM. Em producao moderna, adaptadores transformam eventos em samples de audio,
textures e draw calls. O dominio nao deve conhecer SDL, OpenGL, sistema de arquivos
ou API de som. Interfaces pequenas evitam um `Renderer` ou `AudioManager` monolitico
e aplicam responsabilidade unica, inversao de dependencia e segregacao de interfaces.

### 9.2 Sequencia de extracao por Refactoring/TDD

1. Capture traces dourados de writes APU, VRAM, tilemap, shadow OAM e bancos em ROM.
2. Extraia catalogos tipados sem mudar o ASM; compare IDs, ponteiros e contagens.
3. Implemente o parser de comandos de audio em C sob testes de caracterizacao.
4. Implemente descompressao `.pic` e merge 2bpp; compare byte a byte os buffers 7x7.
5. Extraia facing, culling e montagem OAM; compare cada frame e direcao.
6. Introduza portas de plataforma e execute ASM e C em paralelo sobre os mesmos eventos.
7. Troque um processo por vez somente quando a equivalencia estiver demonstrada.
8. Consolide duplicacao dos tres motores depois de testes cobrirem diferencas do motor 2.

Refatoracoes devem ser pequenas, reversiveis e sem mistura com melhorias de produto.
Cada commit informa requisito AV-Q afetado, evidencia e risco residual. Bugs observados
do original entram como testes no modo fiel antes de qualquer correcao em `ENHANCED`.

### 9.3 Melhorias posteriores, fora do modo fiel

- mixer com buses independentes para musica, SFX, grito e interface, controles de
  volume/mute, ramps sem clique, mono e opcoes de acessibilidade;
- clock de samples independente do FPS, buffer monitorado e telemetria de underrun;
- atlas de textures, batching, escala inteira e profundidade/prioridade explicita;
- cache de imagens descomprimidas e preload por zona, sem bloquear a simulacao;
- camera e culling modernos, mantendo simulacao de NPC independente da visibilidade;
- manifests de assets com IDs estaveis, validacao de schema e suporte controlado a mods;
- sprites opcionais de maior resolucao e animacoes adicionais sob feature flag;
- paletas alternativas, alto contraste, reducao de movimento e controle de flashes;
- ferramentas de debug para canais, notas, OAM, slots VRAM e limites de viewport.

Essas melhorias sao possiveis depois da reescrita, mas nao devem contaminar a trilha
de equivalencia. A recomendacao e manter `GEN1_FIDELITY` e `ENHANCED` sobre os mesmos
eventos de dominio, com renderizadores/mixers e politicas configuraveis.

## 10. Estrategia de testes e aceitacao

| ID | Teste | Evidencia esperada |
|---|---|---|
| AV-T01 | Parser dos 45 headers musicais | bancos, canais e ponteiros iguais ao ASM |
| AV-T02 | Todos os 161 IDs de SFX nos tres motores | disponibilidade, prioridade e canais esperados |
| AV-T03 | 151 especies e 39 slots internos | grito-base, pitch e comprimento identicos |
| AV-T04 | Trace de audio por frame | mesma ordem/valor de writes nos registradores APU |
| AV-T05 | Fade, mute, alarme e preempcao | traces dourados para conflitos e troca de banco |
| AV-T06 | Decoder `.pic` | buffers 1bpp e resultado 2bpp iguais byte a byte |
| AV-T07 | Front/back/trainer pics | hash dos 49 tiles e screenshot de referencia |
| AV-T08 | 72 sprites, quatro direcoes e frames | tile IDs, flips, prioridade e coordenadas OAM iguais |
| AV-T09 | Entrada/saida do viewport | `$ff`, colisao, shadow OAM e redesenho de faixa corretos |
| AV-T10 | Fontes sobre tiles de caminhada | pausa/reload e recuperacao visual caracterizadas |
| AV-T11 | DMG e SGB | registros/pacotes e paleta por especie equivalentes |
| AV-T12 | Geracao documental | `--check`, Graphify atualizado e `git diff --check` limpo |

Testes de audio nao devem depender somente de WAV final: o trace de registradores
localiza divergencias de timing com mais precisao. Testes visuais combinam bytes,
hashes e screenshots; um hash sozinho nao explica falha de alinhamento, flip ou
prioridade. Relogio, banco ROM e fontes de evento devem ser injetaveis e deterministicos.

## 11. Riscos e controles

| Risco | Impacto | Controle preventivo/detectivo |
|---|---|---|
| Deriva entre frame e sample | musica muda tempo ou desafina | clock racional, traces longos e teste de loop |
| Prioridade de SFX alterada | notas somem ou efeitos se sobrepoem | cenarios por par de canais e IDs concorrentes |
| Estado de banco omitido | ponteiro le dados errados | tipo explicito `AudioBank`, asserts e trace de switch |
| Motor 2 tratado como copia exata | alarme/grito/batalha regressam | testes dedicados e consolidacao posterior |
| Assets alternativos incluidos por engano | ROM/visual divergente | manifest ativo derivado de `INCBIN`; `front_rg` excluido |
| Decoder aceita stream corrompido | loop, overflow ou memoria invalida | limites, fuzzing e falha tipada no modo moderno |
| Aliases eliminados | IDs legados mudam | preservar tabela completa de 72/47 entradas |
| Render-all muda logica | NPC fora da tela passa a colidir/mover diferente | separar simulacao, culling e apresentacao |
| Ordem VBlank/DMA alterada | tremor ou frame de atraso diferente | teste de trace por fase do frame |
| Fonte pisa em tiles de caminhada | sprites corrompidos | teste de transicao texto-overworld |
| Async muda gameplay | evento depende de asset ainda nao carregado | preload deterministico e fallback controlado |
| Direitos de assets ignorados | risco de distribuicao | revisao juridica e inventario de proveniencia |

## 12. Matriz de rastreabilidade

| Requisito | Fonte | Testes | Responsavel sugerido |
|---|---|---|---|
| AV-Q01 | constantes/headers/audio/cries | AV-T01 a AV-T05 | Audio |
| AV-Q02 | `gfx/`, tabelas de sprite/treinador | AV-T06 a AV-T11 | Video/assets |
| AV-Q03 | `home/vblank.asm` e traces | AV-T04, AV-T07 a AV-T10 | Compatibilidade |
| AV-Q04 | referencias por secao e anexos | revisao documental | Qualidade tecnica |
| AV-Q05 | este gerador | AV-T12 | Ferramentas |
| AV-Q06 | feature flags e ADRs | suite fiel + melhorada | Arquitetura |
| AV-Q07 | AGENTS/CLAUDE e Graphify | AV-T12 | Mantenedor do repositorio |

## 13. Controle de mudancas

Uma alteracao em `audio/`, `gfx/`, `home/audio.asm`, `home/vblank.asm`, `home/pics.asm`,
`home/vcopy.asm`, `engine/gfx/`, `engine/overworld/map_sprites.asm`, tabelas associadas,
macros ou ferramentas graficas exige avaliar este documento. O fluxo minimo e:

1. regenerar com `python3 tools/generate_audio_sprite_document.py`;
2. executar novamente com `--check`;
3. atualizar Graphify por `python tools/graphify_rgbds.py .` no ambiente registrado;
4. revisar contagens, riscos, criterios e inventarios alterados;
5. registrar revisao, aprovador e evidencias antes da liberacao.

## 14. Inventarios gerados

Os anexos seguintes sao derivados da baseline e nao devem ser editados manualmente.
"Banco" significa motor/banco de audio, nao canal de hardware.

### 14.1 Musicas enderecaveis

""".splitlines()
    )

    music_rows: list[tuple[object, ...]] = []
    for item in music:
        header = music_header_by_symbol[item.target]
        source = data_sources.get(header.pointers[0], "(nao localizado)")
        music_rows.append(
            (
                item.identifier,
                item.bank,
                ", ".join(map(str, header.channels)),
                source,
                source_link("constants/music_constants.asm", item.line),
            )
        )
    add_table(lines, ("ID", "Banco", "Canais", "Dados", "Constante"), music_rows)

    lines.extend(
        """### 14.2 Musica por mapa

O inventario possui uma linha por indice de mapa, inclusive mapas tecnicos e copias
que compartilham musica.

""".splitlines()
    )
    add_table(
        lines,
        ("#", "Mapa", "Musica", "Header/banco", "Fonte"),
        [
            (index, item.map_name, item.music_id, item.bank_symbol, source_link("data/maps/songs.asm", item.line))
            for index, item in enumerate(map_songs, 1)
        ],
    )

    lines.extend(
        """### 14.3 Efeitos, instrumentos e gritos-base

"Disponibilidade" e calculada pela existencia do header correspondente em cada motor.
O mesmo ID pode apontar para implementacoes equivalentes com sufixos `_1`, `_2` e `_3`.

""".splitlines()
    )
    sfx_rows: list[tuple[object, ...]] = []
    for item in sfx:
        normalized = normalized_sfx_symbol(item.target)
        headers = sorted(sfx_availability.get(normalized, []), key=lambda header: header.bank)
        availability = ", ".join(str(header.bank) for header in headers) or str(item.bank)
        channel_sets = "; ".join(
            f"A{header.bank}:" + ",".join(map(str, header.channels)) for header in headers
        ) or "especial"
        source = "-"
        for header in headers:
            if header.pointers and header.pointers[0] in data_sources:
                source = data_sources[header.pointers[0]]
                break
        note = item.comment or "-"
        sfx_rows.append(
            (
                item.identifier,
                sfx_category(item.identifier),
                availability,
                channel_sets,
                source,
                note,
            )
        )
    add_table(
        lines,
        ("ID", "Categoria", "Motores", "Canais", "Dados", "Nota do fonte"),
        sfx_rows,
    )

    lines.extend(
        """### 14.4 Gritos por indice interno

Pitch e comprimento sao bytes modificadores consumidos pelo motor 2; nao equivalem
diretamente a Hertz ou milissegundos sem executar as formulas do sequenciador.

""".splitlines()
    )
    add_table(
        lines,
        ("Indice", "Pokemon/slot", "Grito-base", "Pitch", "Comprimento", "Fonte"),
        [
            (cry.index, cry.pokemon, cry.base, cry.pitch, cry.length, source_link("data/pokemon/cries.asm", cry.line))
            for cry in cries
        ],
    )

    lines.extend(
        """### 14.5 Sprites de overworld

Os aliases/IDs marcados como `UNUSED` continuam presentes para preservar o layout da
tabela. O PNG `red_bike.png` existe no catalogo, mas e selecionado diretamente por
`LoadPlayerSpriteGraphics`, nao por um ID adicional na tabela de 72 entradas.

""".splitlines()
    )
    add_table(
        lines,
        ("ID", "Constante", "Simbolo", "Tiles", "PNG fonte", "Tabela"),
        [
            (
                f"${sprite.sprite_id:02X}",
                sprite.identifier,
                sprite.symbol,
                sprite.tiles,
                sprite.source_asset.replace(".2bpp", ".png"),
                source_link("data/sprites/sprites.asm", sprite.table_line),
            )
            for sprite in sprites
        ],
    )

    lines.extend(
        """### 14.6 Imagens por classe de treinador

O valor BCD de recompensa integra a mesma tabela, embora o foco deste documento seja
a imagem. `ChiefPic` e alias de `ScientistPic`; duas classes usam `JugglerPic`.

""".splitlines()
    )
    add_table(
        lines,
        ("Indice", "Ponteiro", "PNG fonte", "Recompensa-base BCD", "Fonte"),
        [
            (
                trainer.trainer_index,
                trainer.symbol,
                trainer.source_asset.replace(".pic", ".png"),
                trainer.reward,
                source_link("data/trainers/pic_pointers_money.asm", trainer.line),
            )
            for trainer in trainers
        ],
    )

    lines.extend(
        """### 14.7 Imagens comprimidas de personagens ativas

Esta lista vem de `INCBIN` em `gfx/pics.asm` e `data/pokemon/mew.asm`. Os dois fosseis,
o back do jogador e o back do velho aparecem junto das especies por participarem do
mesmo pipeline `.pic`.

""".splitlines()
    )
    add_table(
        lines,
        ("Simbolo", "Asset compilado", "PNG fonte", "Referencia"),
        [
            (
                picture.symbol,
                picture.source_asset,
                picture.source_asset.replace(".pic", ".png"),
                source_link(picture.source, picture.line),
            )
            for picture in character_pictures
        ],
    )

    lines.extend(
        """### 14.8 Cobertura dos PNGs no repositorio

Esta contagem e de arquivos-fonte por diretorio, nao de tiles unicos nem de assets
ativos. Ela torna inclusoes/remocoes detectaveis pelo `--check`.

""".splitlines()
    )
    add_table(
        lines,
        ("Diretorio", "PNGs", "Situacao"),
        [
            (
                directory,
                count,
                "alternativo nao referenciado nesta baseline" if directory == "gfx/pokemon/front_rg" else "fonte versionada; uso definido por ASM/Makefile",
            )
            for directory, count in directory_counts
        ],
    )

    lines.extend(
        """## 15. Evidencias de geracao

- Expansao usada na consulta Graphify: `audio`, `music`, `sound`, `sfx`, `cry`,
  `channel`, `sprite`, `graphics`, `tile`, `oam`, `vram`, `animation`.
- As contagens sao asserts executaveis em `tools/generate_audio_sprite_document.py`.
- O catalogo Graphify e sua visualizacao HTML devem acompanhar a revisao aprovada.
- Baseline documental: commit indicado no controle, antes da inclusao deste documento.

## 16. Aprovacao e pendencias

| Item | Situacao | Evidencia necessaria para encerrar |
|---|---|---|
| Revisao tecnica de audio | Pendente | responsavel confirma comandos, canais e casos especiais |
| Revisao tecnica de video | Pendente | responsavel confirma VRAM/OAM, culling e pipeline `.pic` |
| Revisao de qualidade | Pendente | criterios, riscos e rastreabilidade aprovados |
| Direitos de distribuicao | Fora do escopo tecnico | parecer juridico/proveniencia dos assets |

O documento pode orientar implementacao imediatamente, mas passa a ser baseline
aprovada somente quando os tres revisores tecnicos/qualidade forem designados e a
revisao registrada no historico.
""".splitlines()
    )

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if output differs")
    args = parser.parse_args()

    document = build_document()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != document:
            print(f"out of date: {output.relative_to(ROOT)}")
            return 1
        print(f"up to date: {output.relative_to(ROOT)}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
