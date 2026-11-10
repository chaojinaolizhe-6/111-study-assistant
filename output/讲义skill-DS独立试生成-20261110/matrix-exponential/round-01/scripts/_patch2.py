from pathlib import Path
p=Path(r"matrix-exponential/round-01/scripts/check_layout.py")
s=p.read_text(encoding="utf-8")
s=s.replace('if y1 < 52 or y0 > H - 45:', 'if y1 < 52 or y0 > 784:')
p.write_text(s,encoding="utf-8")
print('patched')
