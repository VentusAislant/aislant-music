import argparse
import os.path

from .core import Score
from .generator import AudioGenerator, MidiGenerator


def main():
    parser = argparse.ArgumentParser(description="从文本乐谱生成 MIDI 文件")

    # 必选参数
    parser.add_argument("--input", "-i", required=True, help="输入乐谱文本文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 MIDI 文件路径")

    # 可选 ScoreMeta 参数
    parser.add_argument("--bpm", type=int, default=None, help="每分钟节拍数 (BPM)")
    parser.add_argument("--key", type=str, default=None, help="调 (key)")
    parser.add_argument("--scale", type=str, default=None, help="音阶 (scale)")
    parser.add_argument("--time_signature", type=str, default=None, help="拍号，例如 4/4")
    parser.add_argument("--instrument", type=int, default=None, help="MIDI 乐器编号 (0=钢琴)")
    parser.add_argument("--default_velocity", type=int, default=None, help="默认音量 (velocity)")

    args = parser.parse_args()

    # 解析 time_signature 字符串
    try:
        ts_numerator, ts_denominator = map(int, args.time_signature.split('/'))
        time_signature = (ts_numerator, ts_denominator)
    except Exception:
        print(f"拍号格式错误: {args.time_signature}，使用默认 (4,4)")
        time_signature = (4, 4)

    # 1. 创建 Score , 传入的超参可以覆盖文件中的解析文件
    score = Score()
    if os.path.isdir(args.input):
        score.parse_score_from_folder(args.input)
    elif os.path.isfile(args.input):
        score.parse_score_from_file(args.input)
    else:
        raise FileNotFoundError(args.input)

    # 覆盖规则：CLI != None 才覆盖
    if args.bpm is not None:
        score.meta.bpm = args.bpm

    if args.key is not None:
        score.meta.key = args.key

    if args.scale is not None:
        score.meta.scale = args.scale

    if args.instrument is not None:
        score.meta.instrument = args.instrument

    if args.default_velocity is not None:
        score.meta.default_velocity = args.default_velocity

    if args.time_signature is not None:
        try:
            n, d = map(int, args.time_signature.split('/'))
            score.meta.time_signature = (n, d)
        except Exception:
            raise ValueError(f"非法拍号: {args.time_signature}")

    # 2. 调用 MidiGenerator 生成 MIDI
    if args.output.endswith(".mid") or args.output.endswith(".midi"):
        generator = MidiGenerator(score)
        generator.generate(args.output)
    elif args.output.endswith(".wav") or args.output.endswith(".mp3"):
        generator = AudioGenerator(score)
        generator.generate(args.output)


if __name__ == "__main__":
    #  python -m aislant_music.music_generator.generate -i xxx.txt -o xxx.mid
    main()
