"""雅思资料下载器（学科专用；不改共用 tools/）。

用法：
    python -B subjects/11-英语-雅思/scripts/fetch_materials.py pdfs
    python -B subjects/11-英语-雅思/scripts/fetch_materials.py ted-index [页数]
    python -B subjects/11-英语-雅思/scripts/fetch_materials.py ted <slug> [<slug> ...]
    python -B subjects/11-英语-雅思/scripts/fetch_materials.py ted-batch [数量]
    python -B subjects/11-英语-雅思/scripts/fetch_materials.py verify

背景（2026-10-03 实测）：
    本机沙箱在 Windows Schannel 层拦截 TLS 凭证 → curl.exe / Invoke-WebRequest /
    web_fetch 全部失败（SEC_E_NO_CREDENTIALS）。
    但 Python 走自带 OpenSSL + certifi CA，HTTPS 正常 → 这是本项目唯一可用的下载通道。

产出目录：subjects/11-英语-雅思/资料/
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUBJ = ROOT / "subjects" / "11-英语-雅思"
MAT = SUBJ / "资料"
TED_DIR = MAT / "TED"
INDEX_JSON = TED_DIR / "_index.json"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def get(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def next_data(html: str) -> dict:
    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S
    )
    if not m:
        raise ValueError("no __NEXT_DATA__ in page")
    return json.loads(m.group(1))


def save(rel: str, data: bytes) -> Path:
    p = MAT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return p


# ------------------------------------------------------------------ PDFs

PDFS = {
    "评分标准-官方-写作-band-descriptors.pdf":
        "https://ielts.org/cdn/ielts-guides/ielts-writing-band-descriptors.pdf",
    "评分标准-官方-口语-band-descriptors.pdf":
        "https://ielts.org/cdn/ielts-guides/ielts-speaking-band-descriptors.pdf",
}


def cmd_pdfs() -> None:
    for name, url in PDFS.items():
        try:
            b = get(url)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__} {e}")
            continue
        if not b.startswith(b"%PDF"):
            print(f"FAIL {name}: not a PDF ({len(b)}B)")
            continue
        p = save(name, b)
        print(f"OK   {p.relative_to(ROOT)}  {len(b)}B")


# ------------------------------------------------------------------ TED index

def build_index(pages: int = 4) -> list[dict]:
    talks: list[dict] = []
    seen: set[str] = set()
    for page in range(1, pages + 1):
        try:
            html = get(f"https://www.ted.com/talks?page={page}").decode("utf-8", "replace")
            data = next_data(html)
            rows = data["props"]["pageProps"]["talks"]
        except Exception as e:  # noqa: BLE001
            print(f"  page {page}: FAIL {type(e).__name__} {str(e)[:80]}")
            continue
        for t in rows:
            cu = t.get("canonicalUrl") or ""
            slug = cu.rstrip("/").split("/")[-1]
            if not slug or slug in seen:
                continue
            seen.add(slug)
            talks.append(
                {
                    "slug": slug,
                    "title": (t.get("title") or "").strip(),
                    "duration": t.get("duration"),
                    "presenter": t.get("presenterDisplayName"),
                    "url": cu,
                }
            )
        print(f"  page {page}: +{len(rows)} (total unique {len(talks)})")
        time.sleep(0.8)
    return talks


def cmd_ted_index(pages: int = 4) -> None:
    talks = build_index(pages)
    TED_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(json.dumps(talks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"index: {len(talks)} talks -> {INDEX_JSON.relative_to(ROOT)}")
    for t in talks[:10]:
        print(f"   {t['duration']:>6}  {t['slug'][:52]:52s} {t['title'][:44]}")


def load_index() -> list[dict]:
    if not INDEX_JSON.is_file():
        print("no index yet; run: ted-index")
        return []
    return json.loads(INDEX_JSON.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ TED transcript

def ms_to_srt(ms: int | None) -> str:
    ms = int(ms or 0)
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, msec = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{msec:03d}"


def fetch_transcript(slug: str) -> tuple[dict, list[str], list[tuple[int, str]]] | None:
    html = get(f"https://www.ted.com/talks/{slug}/transcript").decode("utf-8", "replace")
    data = next_data(html)
    pp = data["props"]["pageProps"]
    td = pp.get("transcriptData") or {}
    tr = td.get("translation") or {}
    paras = tr.get("paragraphs") or []
    if not paras:
        return None

    meta = {
        "slug": slug,
        "title": (pp.get("title") or pp.get("talkTitle") or slug).strip(),
        "speaker": pp.get("presenterDisplayName") or "",
        "duration": pp.get("duration") or "",
        "recorded": pp.get("recordedOn") or pp.get("publishedAt") or "",
        "url": f"https://www.ted.com/talks/{slug}",
        "language": tr.get("language") or "en",
    }

    blocks: list[str] = []
    cues_flat: list[tuple[int, str]] = []
    for p in paras:
        cues = p.get("cues") or []
        txt = " ".join((c.get("text") or "").replace("\n", " ").strip() for c in cues)
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt:
            blocks.append(txt)
        for c in cues:
            t = (c.get("text") or "").replace("\n", " ").strip()
            if t:
                cues_flat.append((int(c.get("time") or 0), t))
    return meta, blocks, cues_flat


def write_transcript(meta: dict, blocks: list[str], cues: list[tuple[int, str]]) -> Path:
    head = [
        f"# {meta['title']}",
        "",
        f"- 来源：TED（{meta['url']}）",
        f"- 讲者：{meta['speaker']}",
        f"- 时长：{meta['duration']}",
        f"- 录制：{meta['recorded']}",
        "- 用途：雅思听力解码训练／兴趣泛听（用途区分见 subjects/11-英语-雅思/资源清单-20261003.md §7）",
        "- 获取方式：公开页面官方 transcript，个人学习使用",
        "",
        "---",
        "",
    ]
    body = "\n\n".join(blocks)
    txt = "\n".join(head) + body + "\n"
    p = TED_DIR / f"{meta['slug']}.txt"
    p.write_text(txt, encoding="utf-8")

    # SRT（时间码由相邻 cue 推出；末条 +4s）
    lines = []
    for i, (t, txt_i) in enumerate(cues):
        end = cues[i + 1][0] if i + 1 < len(cues) else t + 4000
        lines += [str(i + 1), f"{ms_to_srt(t)} --> {ms_to_srt(end)}", txt_i, ""]
    (TED_DIR / f"{meta['slug']}.srt").write_text("\n".join(lines), encoding="utf-8")
    return p


def cmd_ted(slugs: list[str]) -> None:
    ok = skipped = failed = 0
    for i, slug in enumerate(slugs, 1):
        if (TED_DIR / f"{slug}.txt").is_file():
            skipped += 1
            continue
        try:
            r = fetch_transcript(slug)
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(slugs)}] FAIL {slug}: {type(e).__name__} {str(e)[:70]}")
            failed += 1
            time.sleep(1.0)
            continue
        if r is None:
            print(f"[{i}/{len(slugs)}] NO-TRANSCRIPT {slug}")
            failed += 1
            time.sleep(1.0)
            continue
        meta, blocks, cues = r
        try:
            write_transcript(meta, blocks, cues)
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(slugs)}] WRITE-FAIL {slug}: {type(e).__name__} {str(e)[:70]}")
            failed += 1
            time.sleep(1.0)
            continue
        words = sum(len(b.split()) for b in blocks)
        print(f"[{i}/{len(slugs)}] OK {slug[:44]:44s} {str(meta['duration']):>7} {words:>5} words")
        ok += 1
        time.sleep(1.0)
    print(f"\n下载 {ok} / 跳过(已存在) {skipped} / 失败 {failed}")


def cmd_ted_batch(n: int) -> None:
    talks = load_index()
    if not talks:
        return
    cmd_ted([t["slug"] for t in talks[:n]])
    write_ted_index_md()


def write_ted_index_md() -> None:
    talks = load_index()
    rows = []
    got = 0
    for t in talks:
        has = (TED_DIR / f"{t['slug']}.txt").is_file()
        got += has
        rows.append(
            f"| {'✓' if has else '—'} | {t['title'][:58]} | {t['duration']} | "
            f"[{t['slug']}](TED/{t['slug']}.txt) |"
        )
    md = [
        "# TED transcript 库",
        "",
        f"> 建立：2026-10-03。共 **{len(talks)}** 条索引，已下载 **{got}** 条。",
        "> 来源：TED 公开页面官方 transcript（个人学习使用）。由 `scripts/fetch_materials.py` 生成。",
        "> ⚠ **用途区分**（重要）：见 [资源清单](../资源清单-20261003.md) §7——",
        "> **泛听**看过的，**不能再拿来做正式听写**（听写前看过原文＝污染标记）。",
        "",
        "| 已下载 | 标题 | 时长 | 文本 |",
        "|---|---|---|---|",
        *rows,
        "",
    ]
    (TED_DIR / "INDEX.md").write_text("\n".join(md), encoding="utf-8")
    print(f"index md -> {(TED_DIR / 'INDEX.md').relative_to(ROOT)}  ({got}/{len(talks)} 已下载)")


def cmd_verify() -> None:
    print("资料目录：", MAT.relative_to(ROOT))
    if not MAT.is_dir():
        print("  (不存在)")
        return
    for p in sorted(MAT.rglob("*")):
        if p.is_file():
            print(f"  {p.stat().st_size:>9,}B  {p.relative_to(MAT)}")


def cmd_probe_ted4() -> None:
    # 1) sitemap 索引里是什么
    try:
        h = get("https://www.ted.com/sitemap.xml").decode("utf-8", "replace")
        locs = re.findall(r"<loc>(.*?)</loc>", h)
        print("sitemap locs:", len(locs))
        for x in locs[:12]:
            print("   ", x)
    except Exception as e:  # noqa: BLE001
        print("sitemap FAIL", e)

    # 2) go.ted.com 重定向能否解析出 slug
    print("--- redirect resolve ---")
    try:
        req = urllib.request.Request("http://go.ted.com/zachdeboer", headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            print("final url:", r.geturl())
    except Exception as e:  # noqa: BLE001
        print("redirect FAIL", type(e).__name__, str(e)[:120])

    # 3) 其它可能的服务端列表入口
    print("--- other listings ---")
    for url in [
        "https://www.ted.com/talks?sort=newest&page=2",
        "https://www.ted.com/playlists/browse",
        "https://www.ted.com/topics",
    ]:
        try:
            h = get(url).decode("utf-8", "replace")
            d = next_data(h)
            talks = d["props"]["pageProps"].get("talks")
            print(f"{url}\n   len={len(h)} talks={len(talks) if talks else None}")
            if not talks:
                print("   pageProps keys:", list(d["props"]["pageProps"].keys())[:18])
            else:
                print("   first:", talks[0].get("canonicalUrl"))
        except Exception as e:  # noqa: BLE001
            print(f"{url}\n   FAIL {type(e).__name__} {str(e)[:90]}")


def cmd_ted_rss(n: int = 55) -> None:
    """从 TED Talks Daily RSS（按 pubDate 倒序）取最近 N 期，解析重定向拿到 slug。"""
    h = get("https://www.ted.com/talks/rss").decode("utf-8", "replace")
    items = re.findall(r"<item>(.*?)</item>", h, re.S)
    print(f"rss items: {len(items)}")

    def tag(block: str, name: str) -> str:
        m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, re.S)
        return m.group(1).strip() if m else ""

    talks: list[dict] = []
    seen: set[str] = set()
    for it in items:
        if len(talks) >= n:
            break
        link = tag(it, "link").replace("&amp;", "&")
        if not link:
            continue
        try:
            req = urllib.request.Request(link, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                final = r.geturl()
        except Exception as e:  # noqa: BLE001
            print(f"  resolve FAIL {link[:50]}: {str(e)[:60]}")
            continue
        m = re.search(r"/talks/([a-z0-9_]+)", final)
        if not m:
            print(f"  skip (not a talk page): {final[:70]}")
            continue
        slug = m.group(1)
        if slug in seen:
            continue
        seen.add(slug)
        talks.append(
            {
                "slug": slug,
                "title": tag(it, "title"),
                "duration": tag(it, "itunes:duration"),
                "pubDate": tag(it, "pubDate"),
                "url": final,
            }
        )
        print(f"  [{len(talks):>2}/{n}] {talks[-1]['duration']:>7}  {slug[:56]}")
        time.sleep(0.4)

    TED_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(json.dumps(talks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"index -> {len(talks)} talks at {INDEX_JSON.relative_to(ROOT)}")


def cmd_ted_audio(n: int = 12) -> None:
    """按 RSS 的 title→enclosure 映射，为已下载 transcript 的 talk 抓 mp3 音频。

    为什么值得下音频：在 TED 网站上听会**自动显示字幕**，有误看原文的风险
    （听写前看过原文＝污染标记）。用本地播放器放 mp3 可以彻底避免。
    """
    rss = get("https://www.ted.com/talks/rss").decode("utf-8", "replace")
    items = re.findall(r"<item>(.*?)</item>", rss, re.S)
    by_title: dict[str, str] = {}
    for it in items:
        mt = re.search(r"<title>(.*?)</title>", it, re.S)
        me = re.search(r'<enclosure url="([^"]+)"', it)
        if mt and me:
            by_title[mt.group(1).strip()] = me.group(1)

    talks = load_index()
    out = TED_DIR / "audio"
    out.mkdir(parents=True, exist_ok=True)
    ok = skip = miss = fail = 0
    for t in talks:
        if ok + skip >= n:
            break
        if not (TED_DIR / f"{t['slug']}.txt").is_file():
            continue
        url = by_title.get(t["title"].strip())
        if not url:
            print(f"  no-mp3-in-feed {t['slug'][:52]}")
            miss += 1
            continue
        dest = out / f"{t['slug']}.mp3"
        if dest.is_file() and dest.stat().st_size > 100_000:
            skip += 1
            continue
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=180) as r, dest.open("wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {t['slug'][:48]}: {type(e).__name__} {str(e)[:60]}")
            fail += 1
            continue
        mb = dest.stat().st_size / 1e6
        print(f"  OK {t['slug'][:50]:50s} {mb:6.1f}MB")
        ok += 1
        time.sleep(0.4)
    print(f"\n音频：新下 {ok} / 已存在 {skip} / feed无mp3 {miss} / 失败 {fail}")
    print(f"目录：{out.relative_to(ROOT)}")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    cmd, rest = args[0], args[1:]
    if cmd == "pdfs":
        cmd_pdfs()
    elif cmd == "ted-index":
        cmd_ted_index(int(rest[0]) if rest else 4)
    elif cmd == "ted-rss":
        cmd_ted_rss(int(rest[0]) if rest else 55)
    elif cmd == "ted":
        cmd_ted(rest)
    elif cmd == "ted-batch":
        cmd_ted_batch(int(rest[0]) if rest else 50)
    elif cmd == "ted-audio":
        cmd_ted_audio(int(rest[0]) if rest else 12)
    elif cmd == "ted-indexmd":
        write_ted_index_md()
    elif cmd == "verify":
        cmd_verify()
    elif cmd == "probe-ted4":
        cmd_probe_ted4()
    else:
        print(f"unknown command: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
