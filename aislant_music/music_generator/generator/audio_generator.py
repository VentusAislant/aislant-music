import os
import shutil
import tempfile
from pydub import AudioSegment  # 用于 WAV -> MP3
import subprocess
from importlib import resources

from .midi_generator import MidiGenerator  # 你现有的 MidiGenerator


class AudioGenerator:
    """
    将 Score 对象直接生成 WAV 或 MP3 音频文件
    """

    def __init__(
            self,
            score,
            soundfont_path: str | None = None,
            ticks_per_beat=480
    ):
        """
        :param score: Score 对象
        :param soundfont_path: SoundFont 文件路径（.sf2）
        """
        self.score = score
        self.soundfont = soundfont_path or str(
            resources.files("aislant_music.music_generator.resources").joinpath("GeneralUser-GS.sf2")
        )
        self.ticks_per_beat = ticks_per_beat

    def generate(self, output_path: str, format: str = "wav"):
        """
        生成音频文件
        :param output_path: 输出路径，比如 "./out.wav" 或 "./out.mp3"
        :param format: "wav" 或 "mp3"
        """

        # 1️⃣ 生成临时 MIDI
        with tempfile.NamedTemporaryFile(suffix=".midi", delete=False) as tmp_midi:
            midi_path = tmp_midi.name

        try:
            midi_gen = MidiGenerator(self.score, ticks_per_beat=self.ticks_per_beat)
            midi_gen.generate(midi_path)

            # 2️⃣ MIDI -> WAV
            tmp_wav_path = midi_path.replace(".midi", ".wav")
            subprocess.run(
                [
                    "fluidsynth",
                    "-ni",
                    self.soundfont,
                    midi_path,
                    "-F",
                    tmp_wav_path,
                    "-r",
                    "44100",
                ],
                check=True,
            )

            # 3️⃣ WAV -> 最终格式
            if format.lower() == "mp3":
                audio = AudioSegment.from_wav(tmp_wav_path)
                audio.export(output_path, format="mp3")
                os.remove(tmp_wav_path)
            else:
                # ✅ 关键修复：跨文件系统安全移动
                shutil.move(tmp_wav_path, output_path)

            print(f"音频文件生成完成: {output_path}")

        finally:
            # 4️⃣ 清理临时 MIDI（即使中途报错也能清）
            if os.path.exists(midi_path):
                os.remove(midi_path)
