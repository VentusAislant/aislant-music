# Aislant Music

> A music intelligence lab created by Ventus Aislant.

Aislant Music 是一个面向音乐创作、记谱、演奏表达与生成式工具的代码实验室。它不追求把音乐压缩成冰冷的按钮，而是尝试让代码成为一种可以理解旋律、组织乐谱、生成声音、辅助表达的创作介质。

这里会持续沉淀围绕音乐的工具、模型、格式和工作流：从文本乐谱到 MIDI，从和弦图到吉他六线谱，从规则化生成到更智能的音乐辅助创作。每个模块都可以独立使用，也可以在未来组合成更完整的音乐创作系统。🎼

## Development Map

- [x] Text score to MIDI generation
- [x] Text score to audio rendering workflow
- [ ] Guitar chord diagram generation
- [ ] Guitar tab rendering from chord patterns
- [ ] Shared music notation and rhythm utilities
- [ ] Music analysis and generation experiments
- [ ] Higher-level creative composition workflows

## Project Structure

```text
aislant_music/
├── music_generator/  # Text score -> MIDI/audio
└── guitar/           # Guitar chords, diagrams, and tab tools

playground/           # Experiments, notebooks, and song materials
```

## Installation

Python 3.10 is recommended.

```shell
conda create -n aislant-music python=3.10 -y
conda activate aislant-music
pip install -e .
```

Install the music generator extras:

```shell
pip install -e .[music-generator]
```

Install notebook support:

```shell
pip install -e .[notebook]
```

## Modules

### 🎹 Music Generator

`music_generator` turns a lightweight text score into MIDI or audio. It is designed for quick sketching: write notes, rests, chords, and arpeggios in text, then render them into playable output.

Generate MIDI:

```shell
python -m aislant_music.music_generator.generate \
  -i aislant_music/music_generator/recipes/happy_birthday_to_you.txt \
  -o happy_birthday.mid
```

Generate audio:

```shell
python -m aislant_music.music_generator.generate \
  -i aislant_music/music_generator/recipes/happy_birthday_to_you.txt \
  -o happy_birthday.wav
```

Audio rendering uses `fluidsynth`, so make sure it is installed on your system when exporting `.wav` or `.mp3` files.

### 🎸 Guitar

`guitar` is the home for guitar-oriented notation tools: chord shapes, chord diagrams, picking patterns, and six-line tab rendering.

The intended workflow is expressive and compact:

```text
C  53231323
G  53231323
Em 63231323
```

The module is designed around two core ideas:

- turn chord names such as `C`, `G`, and `Em` into readable chord diagrams
- turn chord progressions and picking patterns into guitar tablature

## Playground

`playground/` is where experiments live: notebooks, song materials, rough scripts, and ideas that are still becoming tools. Once an experiment becomes reusable, it can graduate into `aislant_music/`.

## License

This repository is publicly visible for learning and reference, but it is not open source. Commercial use, redistribution, sublicensing, hosting, or publishing derivative works requires explicit written permission from Ventus Aislant.

See [LICENSE](./LICENSE) for details.
