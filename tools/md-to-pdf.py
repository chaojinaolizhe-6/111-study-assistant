#!/usr/bin/env python3
"""把 Markdown 转成中文排版友好的 PDF（本工作区通用工具）。

流水线：Markdown --(python-markdown)--> HTML --(Chrome 无头 --print-to-pdf)--> PDF

用法（在工作区根目录运行）:
  python -B tools/md-to-pdf.py <输入.md> [输出.pdf] [--title "文档标题"] [--css 附加.css]

约定:
  * 需要本机 Chrome 或 Edge；两者都没有时报错退出，不静默失败。
  * 只用标准库 + markdown 包；不联网、不装依赖。
  * 中文字体走 CSS 字体栈（Windows 下微软雅黑优先），不内嵌字体。
  * 打印版式：A4、16mm 页边距、代码块/表格不跨页断开。

说明（2026-10-16 实测）：Chrome 无头 `--print-to-pdf` 默认会加页眉页脚（含本地文件
路径），故统一加 `--no-pdf-header-footer` 关闭；本机 msedge.exe 存在但未实测，
调用顺序为 Chrome → Edge。
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
html { -webkit-text-size-adjust: 100%; }
body {
  font-family: "Microsoft YaHei", "微软雅黑", "Noto Sans CJK SC", "Source Han Sans SC",
               "PingFang SC", "Segoe UI", sans-serif;
  font-size: 10.8pt; line-height: 1.75; color: #1c1e24; margin: 0;
}
h1 { font-size: 19pt; line-height: 1.4; color: #0c52a0; margin: 0 0 10px 0;
     padding-bottom: 8px; border-bottom: 3px solid #0c52a0; }
h2 { font-size: 14.5pt; color: #0c52a0; margin: 22px 0 8px 0; padding-left: 9px;
     border-left: 5px solid #0c52a0; page-break-after: avoid; }
h3 { font-size: 12.4pt; color: #123c68; margin: 16px 0 6px 0; page-break-after: avoid; }
h4 { font-size: 11.2pt; color: #123c68; margin: 13px 0 5px 0; page-break-after: avoid; }
p { margin: 7px 0; }
ul, ol { margin: 7px 0 7px 0; padding-left: 22px; }
li { margin: 4px 0; }
li > ul, li > ol { margin: 4px 0; }
strong { color: #101418; }
em { color: #2a2f38; }
code {
  font-family: Consolas, "Cascadia Mono", "Courier New", monospace;
  font-size: 0.92em; background: #f2f5f9; border: 1px solid #e2e8f0;
  border-radius: 3px; padding: 0 3px; color: #123c68;
}
pre { background: #f6f8fb; border: 1px solid #dde4ee; border-radius: 6px;
      padding: 9px 11px; overflow-wrap: break-word; white-space: pre-wrap;
      page-break-inside: avoid; }
pre code { background: none; border: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.8pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #cfd8e3; padding: 5px 8px; text-align: left;
         vertical-align: top; }
th { background: #eaf1fa; color: #0c52a0; }
blockquote { margin: 10px 0; padding: 8px 13px; background: #f4f8fd;
             border-left: 4px solid #7ba7d4; color: #333a45; }
blockquote p { margin: 4px 0; }
hr { border: none; border-top: 1px solid #d8dee7; margin: 16px 0; }
a { color: #0c52a0; text-decoration: none; }
img { max-width: 100%; }
.toc { background: #f7fafd; border: 1px solid #dde4ee; border-radius: 6px;
       padding: 8px 16px 10px 16px; margin: 14px 0 18px 0; font-size: 10pt;
       page-break-inside: avoid; }
.toc-title { font-weight: 700; color: #0c52a0; margin: 6px 0 2px 0; }
.toc ul { list-style: none; padding-left: 14px; margin: 2px 0; }
.toc > ul { padding-left: 0; }
.toc li { margin: 2px 0; }
"""


def find_browser() -> str:
    for cand in CHROME_CANDIDATES:
        if Path(cand).exists():
            return cand
    for name in ("chrome", "msedge", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit(
        "找不到 Chrome/Edge，无法转 PDF。已试路径：\n  " + "\n  ".join(CHROME_CANDIDATES)
    )


# 列表规范化（2026-10-16 实测踩坑）：Python-Markdown 判定「子列表」要求缩进 ≥ 4 空格，
# 而 3 空格缩进的子项（常见的「序号 + 加粗标题」写法）会被当成上一级的兄弟项，渲染成
# 一行里的字面星号。这里统一：
#   ① 同一层的相邻列表项之间补空行（保证不会把下一个主项粘进子列表）；
#   ② 子列表与其父项之间补空行；
# 再配合 markdown(tab_length=2)（缩进 ≥2 即算下一层），使 2/3/4 空格缩进都能正确嵌套。
# 只调整空行与解析参数，不改动任何文字内容。
LIST_ITEM = re.compile(r"^(?P<indent>[ \t]*)(?:\d+\.|[*+-])[ \t]+\S")
ANY_ITEM = re.compile(r"^[ \t]*(?:\d+\.|[*+-])[ \t]+\S")


def normalize_markdown(md_text: str) -> str:
    lines = md_text.split("\n")
    out: list[str] = []
    for line in lines:
        m = LIST_ITEM.match(line)
        if m:
            indent = len(m.group("indent").expandtabs(2))
            prev = out[-1] if out else ""
            j = len(out) - 1
            while j >= 0 and out[j].strip() == "":
                j -= 1
            prev_content = out[j] if j >= 0 else ""
            pm = LIST_ITEM.match(prev_content)
            need = False
            if prev.strip() == "":
                need = True  # 已有空行：保留（放行本行即可）
            elif pm:
                parent = len(pm.group("indent").expandtabs(2))
                # 同级相邻项：必须空行分开；更深层（子项紧跟父项）：也必须空行分开。
                need = indent <= parent
            elif ANY_ITEM.match(prev_content) or indent >= 2:
                need = True  # 父项后紧跟子项，或段落/连续文本后紧跟子项
            if need and prev.strip() != "":
                out.append("")
            # 缩进夹到 2–3 空格：tab_length=2 下 ≥2 即视为下一层，而 ≥4 会被
            # Python-Markdown 当缩进代码块（实测 n=10 + 4 空格 → <pre> 字面星号）。
            new_indent = " " * min(max(indent, 2) if indent > 0 else 0, 3)
            line = new_indent + line[len(m.group("indent")):]
        out.append(line)
    return "\n".join(out)


def build_html(md_text: str, title: str, extra_css: str) -> str:
    try:
        import markdown
    except ImportError:
        raise SystemExit("缺少 markdown 包：请先 python -m pip install markdown")
    body = markdown.markdown(
        normalize_markdown(md_text),
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"],
        extension_configs={"toc": {"title": "目录", "toc_depth": "2-3"}},
        tab_length=2,
    )
    # python-markdown 的 toc 扩展把目录 div 放在正文最前，这里标记成自定义类
    body = body.replace('<div class="toc">', '<div class="toc"><p class="toc-title">目录</p>', 1)
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">\n"
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{CSS}\n{extra_css}</style></head>\n<body>\n{body}\n</body></html>\n"
    )


def to_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="md2pdf-") as profile:
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-sync",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            f"--user-data-dir={profile}",
            # 必须绝对路径：Chrome 把 --print-to-pdf 的相对路径解析到它自己的 cwd
            f"--print-to-pdf={pdf_path.resolve()}",
            html_path.resolve().as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=180)
    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        sys.stderr.write((proc.stdout or "") + "\n" + (proc.stderr or "") + "\n")
        raise SystemExit(f"PDF 生成失败（exit {proc.returncode}），未写出有效文件：{pdf_path}")


def pdf_pages(pdf_path: Path) -> int:
    """数一下 PDF 页数，用于回报（不引入第三方库）。"""
    try:
        data = pdf_path.read_bytes()
    except OSError:
        return 0
    return len(re.findall(rb"/Type\s*/Page[^s]", data))


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown → PDF（Chrome 无头）")
    ap.add_argument("input", help="输入 .md 路径")
    ap.add_argument("output", nargs="?", help="输出 .pdf 路径（默认与输入同名同目录）")
    ap.add_argument("--title", default=None, help="PDF 标题（默认取 Markdown 首个一级标题）")
    ap.add_argument("--css", default=None, help="附加 CSS 文件路径")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise SystemExit(f"输入文件不存在：{src}")
    md_text = src.read_text(encoding="utf-8")
    if not md_text.strip():
        raise SystemExit(f"输入文件是空的：{src}")

    title = args.title
    if not title:
        m = re.search(r"^#\s+(.+)$", md_text, flags=re.M)
        title = m.group(1).strip() if m else src.stem

    extra_css = Path(args.css).read_text(encoding="utf-8") if args.css else ""
    html_text = build_html(md_text, title, extra_css)

    pdf = Path(args.output) if args.output else src.with_suffix(".pdf")
    html_out = pdf.with_suffix(".html")
    html_out.write_text(html_text, encoding="utf-8")

    to_pdf(find_browser(), html_out, pdf)
    print(f"OK  markdown: {src}  ({len(md_text)} chars)")
    print(f"    html    : {html_out}")
    print(f"    pdf     : {pdf}  ({pdf.stat().st_size} bytes, 约 {pdf_pages(pdf)} 页)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
