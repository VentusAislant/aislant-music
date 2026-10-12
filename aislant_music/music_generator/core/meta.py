import re
from dataclasses import dataclass

__all__ = [
    "ScoreMeta",
    "TrackMeta"
]


@dataclass
class ScoreMeta:
    """
    乐谱的超参数
        :param bpm: Beats Per Minute， 每分钟的节拍数量
        :param key:  调性
        :param scale:  音阶  major/minor/...
        :param time_signature:  拍号 (4,4) → 4/4 拍
        :param instrument:  MIDI Program Number  MIDI乐器号
        :param default_velocity:  音符力度默认值
    """

    bpm: int = 66
    key: str = "C"
    scale: str = "major"
    time_signature: tuple[int, int] = (4, 4)
    instrument: int = 0
    default_velocity: int = 120

    def key_signature_map(self) -> dict[str, int]:
        major_flat_keys = {
            'F': ['B'],
            'Bb': ['B', 'E'],
            'Eb': ['B', 'E', 'A'],
            'Ab': ['B', 'E', 'A', 'D'],
            'Db': ['B', 'E', 'A', 'D', 'G'],
            'Gb': ['B', 'E', 'A', 'D', 'G', 'C'],
            'Cb': ['B', 'E', 'A', 'D', 'G', 'C', 'F'],
        }
        major_sharp_keys = {
            'G': ['F'],
            'D': ['F', 'C'],
            'A': ['F', 'C', 'G'],
            'E': ['F', 'C', 'G', 'D'],
            'B': ['F', 'C', 'G', 'D', 'A'],
            'F#': ['F', 'C', 'G', 'D', 'A', 'E'],
            'C#': ['F', 'C', 'G', 'D', 'A', 'E', 'B'],
        }

        mapping = {}
        for n in major_flat_keys.get(self.key, []):
            mapping[n] = -1
        for n in major_sharp_keys.get(self.key, []):
            mapping[n] = 1
        return mapping

    def update_from_dict(self, data: dict):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: dict) -> "ScoreMeta":
        bpm = int(data.get("bpm", 80))
        if bpm <= 0:
            raise ValueError("bpm 必须为正数")

        key = str(data.get("key", "C"))
        scale = str(data.get("scale", "major"))

        ts = data.get("time_signature", "4/4")
        if isinstance(ts, str):
            n, d = map(int, ts.split("/"))
            time_signature = (n, d)
        elif isinstance(ts, (list, tuple)):
            time_signature = (int(ts[0]), int(ts[1]))
        else:
            raise ValueError(f"非法 time_signature: {ts}")

        instrument = int(data.get("instrument", 0))
        default_velocity = int(data.get("default_velocity", 64))

        return cls(
            bpm=bpm,
            key=key,
            scale=scale,
            time_signature=time_signature,
            instrument=instrument,
            default_velocity=default_velocity,
        )

    @classmethod
    def from_json(cls, path: str) -> "ScoreMeta":
        import json
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


@dataclass
class TrackMeta:
    instrument: int | None = None  # Program Change  乐器转换
    default_velocity: int | None = None  # note_on velocity  默认音量

    @classmethod
    def from_text(cls, text: str) -> "TrackMeta":
        meta = cls()

        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("#"):
                continue

            # 去掉 #
            content = line[1:].strip()

            # key = value
            m = re.match(r"(\w+)\s*=\s*(.+)", content)
            if not m:
                continue

            key, value = m.groups()
            key = key.lower()

            if key == "instrument":
                meta.instrument = int(value)
            elif key in ("default_velocity", "velocity"):
                meta.default_velocity = int(value)
            # 其他 key：忽略
        return meta

    @classmethod
    def from_file(cls, file_path: str) -> "TrackMeta":
        with open(file_path, "r", encoding="utf-8") as f:
            return cls.from_text(f.read())
