from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage

from ..core import *
from ..utils import *

__all__ = [
    "MidiGenerator"
]


class MidiGenerator:
    """
    将 Score 类对象转化为可以播放的 midi 音乐文件
    """

    def __init__(self, score: Score, ticks_per_beat=480):
        """
        :param score: 乐谱对象，包含 meta 信息和音乐事件列表 all_events
        :param ticks_per_beat: MIDI 文件内部的时间单位不是秒也不是拍 beat, 而是 tick
            注意 ticks_per_beat 不影响演奏快慢，演奏快慢还是由 bpm 决定，tick 只是 midi 的一个时间单位
            可以把一拍分成若干个 tick，也就是说一拍的持续时长
            假设 bpm = 120, ticks_per_beat = 480, 则
                每个 beat 的时长为 60 / 120 = 0.5s,
                每个 tick 的时长为 0.5s / 480 = 1.04 ms
        """
        self.ticks_per_beat = ticks_per_beat
        self.score = score
        self.bpm = score.meta.bpm  # 每分钟节拍数

        """
        mido.bpm2tempo(bpm) 会
            把 BPM 转换成 MIDI 文件里的 tempo（microseconds per beat）
        """
        self.tempo = bpm2tempo(self.bpm)  # 告诉播放器每拍多长时间

        self.note_converter = NoteConverter(score.meta)

        self.instrument = score.meta.instrument
        self.default_velocity = score.meta.default_velocity

    def generate(self, output_path: str = "./aislant.midi"):
        """
        将乐谱转化成 midi 文件输出到 output_path
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        for channel, (_, events) in enumerate(self.score.tracks.items()):
            track = MidiTrack()
            mid.tracks.append(track)

            program_change_event = events[0]
            default_velocity_change_event = events[1]

            assert isinstance(program_change_event, ProgramChangeEvent)
            assert isinstance(default_velocity_change_event, DefaultVelocityChangeEvent)

            # 设置节奏
            track.append(MetaMessage('set_tempo', tempo=self.tempo, time=0))

            # 设置乐器
            track.append(Message(
                'program_change', program=program_change_event.instrument, channel=channel, time=0
            ))

            # 设置默认音量
            self.default_velocity = default_velocity_change_event.default_velocity

            # 加入音乐
            total_len = 0
            for event in events[2:]:
                total_len += event.duration * self.ticks_per_beat
            print(int(total_len))

            for event in events[2:]:
                duration_ticks = int(event.duration * self.ticks_per_beat)

                if isinstance(event, NoteEvent):
                    note_num = self.note_converter.note2midi(event.note.name)
                    velocity = getattr(event.note, 'velocity', self.default_velocity)
                    track.append(Message('note_on', note=note_num, channel=channel, velocity=velocity, time=0))
                    track.append(
                        Message('note_off', note=note_num, channel=channel, velocity=velocity, time=duration_ticks))

                elif isinstance(event, ChordEvent):
                    velocity = getattr(event.notes[0], 'velocity', self.default_velocity)
                    # 所有 note_on 同时按下
                    for note in event.notes:
                        note_num = self.note_converter.note2midi(note.name)
                        track.append(Message('note_on', note=note_num, channel=channel, velocity=velocity, time=0))

                    # 所有 note_off 同时释放
                    note_0_num = self.note_converter.note2midi(event.notes[0].name)
                    track.append(
                        Message('note_off', note=note_0_num, channel=channel, velocity=velocity, time=duration_ticks))
                    for note in event.notes[1:]:
                        note_num = self.note_converter.note2midi(note.name)
                        track.append(Message('note_off', note=note_num, channel=channel, velocity=velocity, time=0))

                elif isinstance(event, ArpeggioEvent):
                    velocity = getattr(event.notes[0], 'velocity', self.default_velocity)
                    # 计算每个音符开始的时间（tick）
                    # direction 不影响 MIDI 数值，只是顺序，up=正序，down=逆序
                    notes = event.notes if event.direction == "up" else list(reversed(event.notes))

                    note_durations = [int(d * self.ticks_per_beat) for d in event.durations if d != -1]
                    note_durations.append(duration_ticks - sum(note_durations))

                    for i, note in enumerate(notes):
                        note_num = self.note_converter.note2midi(note.name)
                        note_vel = getattr(note, 'velocity', velocity)
                        track.append(Message('note_on', note=note_num, channel=channel, velocity=note_vel, time=0))
                        track.append(Message('note_off', note=note_num, channel=channel, velocity=note_vel,
                                             time=note_durations[i]))


                elif isinstance(event, RestEvent):
                    # 休止符只推进时间
                    track.append(Message('note_off', note=0, channel=channel, velocity=0, time=duration_ticks))

        mid.save(output_path)
        print(f"MIDI 文件生成完成: {output_path}")
