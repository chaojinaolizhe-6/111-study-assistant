import io, re
p = r"_scratch\check-ru-20261023\content_body.py"
lines = io.open(p, encoding="utf-8").read().split("\n")
for i, ln in enumerate(lines, 1):
    if re.search(r"^\s*P\s*=|^P\s*=|\{\s*$|'sec':|'head':", ln):
        if "'sec'" in ln or "'head'" in ln:
            print(f"{i:5d}: {ln.strip()[:110]}")
print("TOTAL LINES", len(lines))
