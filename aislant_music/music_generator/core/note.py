__all__ = [
    "Note",
]

class Note:
    """
    单个音符
    """
    def __init__(self, name, duration, velocity=None):
        self.name = name
        self.duration = duration
        if velocity:
            self.velocity = velocity  # 可覆盖默认音量