"""下载 ielts.org 官方免费样题与评分标准（学科专用；官方公开资源）。

用法：
    python -B subjects/11-英语-雅思/scripts/fetch_ielts_official.py probe
    python -B subjects/11-英语-雅思/scripts/fetch_ielts_official.py download

产出：subjects/11-英语-雅思/资料/官方样题/
"""
from __future__ import annotations

import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "subjects" / "11-英语-雅思" / "资料" / "官方样题"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

PAGES = [
    "https://ielts.org/take-a-test/preparation-resources/sample-test-questions/academic-test",
    "https://ielts.org/take-a-test/preparation-resources/writing-test-resources",
]


def get(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def collect() -> tuple[list[str], list[str]]:
    pdfs: list[str] = []
    media: list[str] = []
    for page in PAGES:
        try:
            h = get(page).decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"page FAIL {page}: {type(e).__name__} {str(e)[:90]}")
            continue
        for x in re.findall(r'href="([^"]+)"', h):
            if x.endswith(".pdf") and x not in pdfs:
                pdfs.append(x)
            elif re.search(r"\.(mp3|m4a|mp4|wav)(\?|$)", x, re.I) and x not in media:
                media.append(x)
        # 页面里出现的任何音频引用（含 data-* 与 JSON）
        for x in re.findall(r'https?://[^"\'\s]+\.(?:mp3|m4a|mp4)', h):
            if x not in media:
                media.append(x)
    return pdfs, media


def cmd_probe() -> None:
    pdfs, media = collect()
    print(f"PDF: {len(pdfs)}   AUDIO/VIDEO: {len(media)}")
    for x in pdfs:
        print("  PDF  ", x.replace("https://ielts.org/cdn/", "")[:120])
    for x in media[:20]:
        print("  MEDIA", x[:120])


def cmd_download() -> None:
    pdfs, media = collect()
    OUT.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for url in pdfs:
        name = url.split("/")[-1]
        # 加前缀避免不同目录同名
        if "listening" in url:
            name = "听力-" + name
        elif "reading" in url:
            name = "阅读-" + name
        p = OUT / name
        if p.is_file() and p.stat().st_size > 1000:
            ok += 1
            continue
        try:
            b = get(url)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__} {str(e)[:70]}")
            fail += 1
            continue
        if not b.startswith(b"%PDF"):
            print(f"FAIL {name}: not PDF ({len(b)}B)")
            fail += 1
            continue
        p.write_bytes(b)
        print(f"OK   {name}  {len(b):,}B")
        ok += 1
        time.sleep(0.5)
    print(f"\nPDF 下载 {ok} / 失败 {fail}")
    if media:
        (OUT / "_media_urls.txt").write_text("\n".join(media), encoding="utf-8")
        print(f"音频/视频链接 {len(media)} 条 -> _media_urls.txt")
    else:
        print("页面内未发现音频直链（音频可能由播放器 JS 另行请求）")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == "probe":
        cmd_probe()
    elif cmd == "download":
        cmd_download()
    else:
        print(f"unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
