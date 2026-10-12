def parse_blocks(lines):
    blocks = []
    block = []
    for line in lines:
        line = line.strip()
        if not line:  # 空行表示块结束
            if block:
                blocks.append(block)
                block = []
        else:
            block.append(line)
    if block:
        blocks.append(block)
    return blocks

def line_durations(line):
    durations = []
    notes = line.split(',')
    for note in notes:
        note = note.strip()
        if not note:
            continue
        parts = note.split()
        try:
            dur = float(parts[-1])
            durations.append(dur)
        except:
            print(f"无法解析音符: {note}")
    return durations

def blocks_durations(blocks):
    all_blocks = []
    for block in blocks:
        block_durs = []
        for line in block:
            block_durs.append(line_durations(line))
        all_blocks.append(block_durs)
    return all_blocks

def compare_blocks(bass_blocks, sharp_blocks):
    for i, (b_block, s_block) in enumerate(zip(bass_blocks, sharp_blocks)):
        # 计算每块总时长
        b_sum = sum(sum(line) for line in b_block)
        s_sum = sum(sum(line) for line in s_block)
        if b_sum != s_sum:
            print(f"\n=== 块 {i+1} 时长不一致 ===")
            print(f"总时长: Bass={b_sum}, Sharp={s_sum}")
            print("Bass:")
            for j, line in enumerate(b_block):
                print(f"  行 {j+1}: {line} => sum={sum(line)}")
            print("Sharp:")
            for j, line in enumerate(s_block):
                print(f"  行 {j+1}: {line} => sum={sum(line)}")

# 读取你的 bass 和 sharp 文件
with open("bass.txt") as f:
    bass_lines = f.readlines()
with open("sharp.txt") as f:
    sharp_lines = f.readlines()

bass_blocks = parse_blocks(bass_lines)
sharp_blocks = parse_blocks(sharp_lines)

bass_durations = blocks_durations(bass_blocks)
sharp_durations = blocks_durations(sharp_blocks)

compare_blocks(bass_durations, sharp_durations)
