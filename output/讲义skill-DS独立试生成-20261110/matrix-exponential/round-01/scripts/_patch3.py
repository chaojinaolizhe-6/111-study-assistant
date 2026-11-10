from pathlib import Path
p=Path(r"matrix-exponential/round-01/scripts/check_layout.py")
s=p.read_text(encoding="utf-8")
old='''    # 页底孤立标题：最后两行是短标题样式
    tail = sorted(body, key=lambda b: b[1])[-2:]
    for x0, y0, x1, y1, text in tail:
        t = text.strip()
        if y0 > H - 150 and len(t) < 42 and re.match(r"^(§|附录|[0-9]+\\.[0-9]+|B\\.[0-9])", t):
            fail(f"p{i+1} 页底疑似孤立标题：{t!r}")'''
new='''    # 页底孤立标题：按行合并后，最后两行若以节号开头且很短，则提示
    lines = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            y0 = min(s["bbox"][1] for s in spans)
            if y0 > 784:
                continue
            lines.append((y0, text))
    for y0, text in sorted(lines)[-2:]:
        if y0 > H - 150 and len(text) < 42 and re.match(r"^(§|附录|[0-9]+\\.[0-9]+\\s|B\\.[0-9])", text):
            fail(f"p{i+1} 页底疑似孤立标题：{text!r}")'''
assert old in s
s=s.replace(old,new)
p.write_text(s,encoding="utf-8")
print("patched")
