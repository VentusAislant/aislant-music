__all__ = [
    "ScoreMeta",
]

class ScoreMeta:
    """
    乐谱的超参数
    """
    def __init__(
            self,
            bpm=80,
            key='C',
            scale='major',
            time_signature=(4,4),
            instrument=0,
            default_velocity=64
    ):
        """
        乐谱的超参
        :param bpm: Beats Per Minute， 每分钟的节拍数量
        :param key:  调性
        :param scale:  音阶  major/minor/...
        :param time_signature:  拍号 (4,4) → 4/4 拍
        :param instrument:  MIDI Program Number  MIDI乐器号
        :param default_velocity:  音符力度默认值
        """
        self.bpm = bpm
        self.key = key
        self.scale = scale
        self.time_signature = time_signature
        self.instrument = instrument
        self.default_velocity = default_velocity
