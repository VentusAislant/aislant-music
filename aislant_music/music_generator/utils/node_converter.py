import re
from ..core import ScoreMeta

__all__ = [
    "NoteConverter"
]


class NoteConverter:
    """
    音符转换器，将音名(如C4, D#4, Gb5)根据乐谱超参转化成数值画音高尽可 (MIDI number)

    解析规则，对于 note_name = 'Gb5'
        音级 (step): G (CDEFGAB)
        升降号 (accidentals)： b (#, n)  n表示 natural 还原调号的影响
        八度编号 (octave)： 4
        pitch_class 是十二平均律中的索引
            C       0
            C#/Db   1
            D       2
            D#/Eb   3
            E       4
            F       5
            F#/Gb   6
            G       7
            G#/Ab   8
            A       9
            A#/Bb   10
            B       11

        midi = (octave + 1) * 12 + pitch_class
        C4 = (4+1)*12 + 0 = 60
        Gb5 = (5+1)*12 + 6 = 78
    """
    NOTE_BASE = {
        "C": 0,
        # "C#": 1,
        # "Db": 1,
        "D": 2,
        # "D#": 3,
        # "Eb": 3,
        "E": 4,
        "F": 5,
        # "F#": 6,
        # "Gb": 6,
        "G": 7,
        # "G#": 8,
        # "Ab": 8,
        "A": 9,
        # "A#": 10,
        "B": 11
    }

    # 分为三个部分
    # ([A-G]) 表示 音级 取值为 CDEFGAB
    # ([#b]*) 表示 升降号 可以支持若干个连续的 # 或 b
    # (-?\d+) 表示 八度编号 是一个或多个数字， -? 可以支持负数
    NOTE_PATTERN = re.compile(r"^([A-G])([#bn]*)(-?\d+)$")

    def __init__(self, meta: ScoreMeta):
        self.meta = meta
        self.key_map = self.meta.key_signature_map()
        print(f'调号: {meta.key}{meta.scale} -> {self.key_map}')

    def note2midi(self, note_name: str) -> int:
        note_name = note_name.strip().capitalize()
        match = NoteConverter.NOTE_PATTERN.match(note_name)
        if not match:
            raise ValueError(f"非法音符名: {note_name}")
        note, accidentals, octave = match.groups()
        octave = int(octave)

        if note not in NoteConverter.NOTE_BASE:
            raise ValueError(f"非法音符名: {note_name}")
        pitch = NoteConverter.NOTE_BASE[note]
        # 升降号处理，这里我们支持多个升降号，例如 C## = D
        for acc in accidentals:
            if acc == '#':
                pitch += 1
            else:
                pitch -= 1

        # 调号处理
        if 'n' not in note_name and note in self.key_map:
            pitch += self.key_map[note]

        midi = (octave + 1) * 12 + pitch

        if not 0 <= midi <= 127:
            raise ValueError(f"MIDI 音高越界 {midi} ({note_name})")

        return midi
