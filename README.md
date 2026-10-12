# Aislant Music

我的私人音乐小工具仓库。

这个仓库会逐步沉淀一些和音乐相关的小工具。目前包含从文本乐谱生成 MIDI/音频的 `music_generator`，并预留了 `guitar` 模块用于后续吉他和弦图、六线谱等功能。

## 目录结构

```text
aislant_music/
├── music_generator/  # 文本乐谱 -> MIDI/音频
└── guitar/           # 吉他相关工具，暂时只预留模块

playground/           # 临时实验、notebook、歌曲素材
```

## 安装

建议使用 Python 3.10。

```shell
conda create -n aislant-music python=3.10 -y
conda activate aislant-music
pip install -e .
```

安装音乐生成器依赖：

```shell
pip install -e .[music-generator]
```

如果需要运行 notebook：

```shell
pip install -e .[notebook]
```

## 使用

生成 MIDI：

```shell
python -m aislant_music.music_generator.generate \
  -i aislant_music/music_generator/recipes/happy_birthday_to_you.txt \
  -o happy_birthday.mid
```

生成音频时需要本机安装 `fluidsynth`：

```shell
python -m aislant_music.music_generator.generate \
  -i aislant_music/music_generator/recipes/happy_birthday_to_you.txt \
  -o happy_birthday.wav
```

## 模块规划

`music_generator` 先保持独立，不急着抽公共 core。后续 `guitar` 如果也需要复用音符、节奏、小节、调式等概念，再把真实共享的部分抽到公共模块。
