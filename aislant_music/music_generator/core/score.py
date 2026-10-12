import re
import os

from .event import *
from .meta import ScoreMeta, TrackMeta
from .note import Note

__all__ = [
    "Score",
]


class Score:
    def __init__(self, meta=None):
        self.meta = meta or ScoreMeta()
        # 每个 Track 包含单音，和弦，休止等音乐事件
        self.tracks: dict[str, list[MusicEvent]] = {}

    def parse_score_from_folder(self, folder_path):
        """
        默认 folder 中包含如下文件
            meta.json， 歌曲元信息
            xxx.txt,  track 的文件
        """
        meta_path = os.path.join(folder_path, 'meta.json')
        track_file_paths = {}
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                track_file_paths[filename.split('.txt')[0].strip()] = os.path.join(folder_path, filename)

        self.meta = ScoreMeta.from_json(meta_path)
        for track_file_name, track_file_path in track_file_paths.items():
            track_events = self.parse_score_from_file(track_file_path)
            self.tracks[track_file_name] = track_events

    def parse_score_from_file(self, file_path) -> list[MusicEvent]:
        """
        从文本文件中解析音符，每个音符由 (音名, 时长, 音量*) 组成
        分隔符支持：逗号 / 中文逗号 / 换行
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.parse_score_from_text(text)

    def parse_score_from_text(self, text: str) -> list[MusicEvent]:
        """
        从文本文件中解析音符，每个音符由 (音名, 时长, 音量*) 组成
        分隔符支持：逗号 / 中文逗号 / 换行
            一般小节内的音符用逗号分割，小节之间用换行分割
        休止符需要将音符命名为 R 或者 Rest
        和弦需要多个音名用 + 拼接即可
        琶音支持：
            ~C4+E4+G4 0.5 (120)            # 琶音（up，默认 spacing）
            ~C4-E4-G4 0.5 (120)             # 琶音（down，默认 spacing）
            ~(0.08)C4+E4+G4 0.5 (120)       # 琶音（up，spacing=0.08）
            ~(0.08)C4-E4-G4 0.5 (120)       # 琶音（down，spacing=0.08）
            ~(-0.08)C4+E4+G4 0.5 (120)       # 琶音（down，spacing=0.08）
            ~(-)C4+E4+G4 0.5 (120)       # 琶音（down，默认 spacing）
        """
        # 首先解析 track meta 信息
        track_meta = TrackMeta.from_text(text)
        if track_meta.instrument is None:
            # 使用默认的乐器代替
            track_meta.instrument = self.meta.instrument
        if track_meta.default_velocity is None:
            track_meta.default_velocity = self.meta.default_velocity

        print(track_meta)
        events = [
            ProgramChangeEvent(track_meta.instrument),
            DefaultVelocityChangeEvent(track_meta.default_velocity),
        ]

        # 按 , ， 或 换行 分割
        parts = re.split(r"[,\n，]+", text)

        for part in parts:
            part = part.strip()
            if part.startswith('#') or not part:
                continue

            tokens = part.split()

            if len(tokens) not in (2, 3):
                raise ValueError(f"非法音符格式: {part}")

            symbol = tokens[0].capitalize()
            duration = float(tokens[1])
            velocity = (
                int(tokens[2])
                if len(tokens) == 3
                else self.meta.default_velocity
            )

            # 1️⃣ REST 休止符
            if symbol in ("R", "REST"):
                events.append(RestEvent(duration))
                continue

            # 2️⃣ 琶音
            if symbol.startswith("~"):
                direction = "up"  # 默认向上
                spacing = 0.1  # 默认 spacing
                note_part = symbol[1:]  # 去掉 ~

                # 1️⃣ 检查括号参数 ~(...) 格式
                m = re.match(r"\(([^)]+)\)(.+)", note_part)
                if m:
                    param_str, notes_str = m.groups()
                    param_str = param_str.strip()

                    # 特殊情况：~(-) -> down，默认 spacing
                    if param_str == "-":
                        direction = "down"
                        spacing = 0.1
                    # ~(-0.08) -> down，spacing = 0.08
                    elif param_str.startswith("-"):
                        direction = "down"
                        spacing = abs(float(param_str))
                    # ~(0.08) -> up，spacing = 0.08
                    else:
                        spacing = float(param_str)

                    note_part = notes_str  # 去掉括号部分

                # 判断方向 + / -
                if "-" in note_part:
                    direction = "down"
                    note_names = note_part.split("-")
                else:
                    note_names = note_part.split("+")

                notes = [Note(name=n, duration=duration, velocity=velocity) for n in note_names]
                events.append(ArpeggioEvent(notes, duration, direction=direction, spacing=spacing))
                continue

            # 3️⃣ Chord 和弦
            if "+" in symbol:
                note_names = symbol.split("+")
                notes = [
                    Note(name=n, duration=duration, velocity=velocity)
                    for n in note_names
                ]
                events.append(ChordEvent(notes, duration))
                continue

            # 4️⃣ Single note  单音事件
            note = Note(symbol, duration, velocity)
            events.append(NoteEvent(note))

        return events
