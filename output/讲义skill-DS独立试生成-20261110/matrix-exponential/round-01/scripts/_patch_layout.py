from pathlib import Path
p=Path(r"matrix-exponential/round-01/scripts/check_layout.py")
s=p.read_text(encoding="utf-8")
s=s.replace('if y1 < 52 or y0 > H - 34:  # 页眉/页脚', 'if y1 < 52 or y0 > H - 45:  # 页眉/页脚（页脚基线约 805pt）')
s=s.replace('    tol = 2.0\n', '    tol = 12.0  # ctex 标点悬挂可伸出边界约 8pt\n')
s=s.replace('[f"课件例题 {i}" for i in range(1, 9)]', '[f"课件例题{i}" for i in range(1, 9)]')
p.write_text(s,encoding="utf-8")
print("patched")
