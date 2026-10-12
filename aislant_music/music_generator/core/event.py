from .note import Note

__all__ = [
    "MusicEvent",
    "NoteEvent",
    "ChordEvent",
    "RestEvent",
    "ArpeggioEvent",
    "ProgramChangeEvent",
    "DefaultVelocityChangeEvent"
]


class MusicEvent:
    """
    抽象基类
    """

    def __init__(self, duration: float):
        self.duration = duration


class NoteEvent(MusicEvent):
    """
    单个音符事件
        C4 0.5 (120)  # 音阶，时长，(音量)
    """

    def __init__(self, note: Note):
        super().__init__(note.duration)
        self.note = note
        self.velocity = getattr(note, 'velocity', 64)


class ChordEvent(MusicEvent):
    """
    和弦事件
        C4+E4+G4 0.5 (120)     # 普通和弦（同时）
    """

    def __init__(self, notes: list[Note], duration: float):
        super().__init__(duration)
        self.notes = notes


class ArpeggioEvent(MusicEvent):
    """
    琶音事件 (多个音符快速依次弹奏)
        ~C4+E4+G4 0.5 (120)            # 琶音（up，默认 spacing）
        ~C4-E4-G4 0.5 (120)             # 琶音（down，默认 spacing）
        ~(0.08)C4+E4+G4 0.5 (120)       # 琶音（up，spacing=0.08）
        ~(0.08)C4-E4-G4 0.5 (120)       # 琶音（down，spacing=0.08）
        ~(-0.08)C4+E4+G4 0.5 (120)       # 琶音（down，spacing=0.08）
        ~(-)C4+E4+G4 0.5 (120)       # 琶音（down，默认 spacing）
    """

    def __init__(self, notes: list[Note], duration: float, direction: str = 'up', spacing: float = 0.1):
        super().__init__(duration)
        self.notes = notes
        self.direction = direction

        # 每个音符时长
        self.durations = [spacing] * (len(notes) - 1)
        self.durations.append(-1)


class RestEvent(MusicEvent):
    """
    休止事件
        R 0.5   # 休止半拍
        REST 1  # 休止一拍
    """
    pass


class ProgramChangeEvent(MusicEvent):
    def __init__(self, instrument: int, duration=0):
        super().__init__(duration)
        self.instrument = instrument


class DefaultVelocityChangeEvent(MusicEvent):
    def __init__(self, default_velocity: int, duration=0):
        super().__init__(duration)
        self.default_velocity = default_velocity
