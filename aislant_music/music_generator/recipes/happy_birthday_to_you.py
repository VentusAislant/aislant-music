from ..core import Score, ScoreMeta, NoteEvent, ChordEvent, RestEvent, Note
from ..generator import MidiGenerator

# 创建乐谱
score = Score()
score.meta = ScoreMeta(
    bpm=120,
    key='C',
    scale='major',
    time_signature=(3, 4),
    instrument=0,  # 钢琴
    default_velocity=100
)

# 生日快乐旋律（C 大调）
# 每个元素: (音符名, 时长)
melody = [
    ("G4", 0.5), ("G4", 0.5), ("A4", 1), ("G4", 1), ("C5", 1), ("B4", 2),  # Happy birthday to you
    ("G4", 0.5), ("G4", 0.5), ("A4", 1), ("G4", 1), ("D5", 1), ("C5", 2),  # Happy birthday to you
    ("G4", 0.5), ("G4", 0.5), ("G5", 1), ("E5", 1), ("C5", 1), ("B4", 1), ("A4", 1),
    ("F5", 0.5), ("F5", 0.5), ("E5", 1), ("C5", 1), ("D5", 1), ("C5", 1.5)
]

# 添加事件
for i, (note_name, duration) in enumerate(melody):
    score.events.append(NoteEvent(Note(note_name, duration)))

# 休止符可选
score.events.append(RestEvent(duration=1.5))

# 生成 MIDI 文件
generator = MidiGenerator(score)
generator.generate("happy_birthday.mid")

# python -m aislant_music.music_generator.recipes.happy_birthday_to_you
