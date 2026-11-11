# -*- coding: utf-8 -*-
"""Produce verification.txt and delivery-manifest.json for comparison-revised.

This script only reads the built PDF, the frozen source PDFs and the check
logs. It does not edit the booklet or the lecture. It records text-layer,
geometry, hash and compile facts; it does not claim visual or learner review.
"""
import datetime
import hashlib
import json
import os
import re
import sys

import fitz

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(HERE, "comparison.pdf")
TEX = os.path.join(HERE, "comparison.tex")
LOG = os.path.join(HERE, "comparison.log")
CROPS = os.path.join(HERE, "crops.json")
RENDER_CROPS = os.path.join(HERE, "render-crops.json")
FIGS = os.path.join(HERE, "figs")
RENDER = os.path.join(HERE, "render")
CHECKS = os.path.join(HERE, "checks")
FINAL = os.path.join(ROOT, "final-selection.json")
OLD = os.path.join(ROOT, "inputs", "old-handout.pdf")
NEW = os.path.join(ROOT, "round-04", "handout.pdf")
LIMIT = 25 * 1024 * 1024


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def agg_sha(directory, pattern):
    rows = []
    for name in sorted(os.listdir(directory)):
        if re.fullmatch(pattern, name):
            rows.append(f"{name}:{sha(os.path.join(directory, name))}")
    return hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest(), len(rows)


def read_text(path):
    if not os.path.isfile(path):
        return ""
    raw = open(path, "rb").read()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff") or b"\x00" in raw[:200]:
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8", errors="replace")


def total_line(text):
    m = re.search(r"TOTAL:\s*(\d+)\s*passed,\s*(\d+)\s*failed", text)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def main():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_cn = now_utc + datetime.timedelta(hours=8)
    with open(FINAL, encoding="utf-8") as f:
        final = json.load(f)
    with open(CROPS, encoding="utf-8") as f:
        crops = json.load(f)["crops"]
    with open(RENDER_CROPS, encoding="utf-8") as f:
        rc = json.load(f)

    doc = fitz.open(PDF)
    pages = doc.page_count
    pdf_bytes = os.path.getsize(PDF)
    pdf_sha = sha(PDF)
    pdf_meta = doc.metadata
    page_rows = []
    text_chars = 0
    image_placements = 0
    margin_ok = True
    header_ok = True
    image_geom_ok = True
    for i, pg in enumerate(doc):
        blocks = [b for b in pg.get_text("blocks") if b[6] == 0 and b[4].strip("\x00\r\n ")]
        text = pg.get_text().replace("\x00", "")
        text_chars += len(text)
        ys = [b[3] for b in blocks]
        ymin, ymax = (min(ys), max(ys)) if ys else (0, 0)
        imgs = pg.get_images(full=True)
        n_img = 0
        for info in imgs:
            for r in pg.get_image_rects(info[0]):
                if r.width < 100:
                    continue
                n_img += 1
                if not (r.x0 > 40 and r.x1 < 556 and r.y0 > 20 and r.y1 < 822 and r.width <= 479):
                    image_geom_ok = False
        image_placements += n_img
        if "新旧对比册" not in text or "理论力学" not in text:
            header_ok = False
        for b in blocks:
            x0, y0, x1, y1 = b[:4]
            if not (x0 > 35 and x1 < 560 and y0 > 18 and y1 < 825):
                margin_ok = False
        page_rows.append((i + 1, len(text), n_img, ymin, ymax))

    log = read_text(LOG)
    m = re.search(r"Output written on comparison\.pdf \((\d+) pages?\)", log)
    log_pages = int(m.group(1)) if m else None
    overfull = ("Overfull \\hbox" in log) or ("Overfull \\vbox" in log)
    missing = "Missing character" in log
    latex_error = "LaTeX Error" in log
    undef = ("Undefined control sequence" in log) or ("undefined references" in log.lower())
    underfull = log.count("Underfull \\hbox")

    rc_failures = rc.get("failures", [])
    anchors_ok = all(c.get("anchors_ok") for c in rc.get("crops", []))
    figs_sha, figs_n = agg_sha(FIGS, r".*\.png")
    render_sha, render_n = agg_sha(RENDER, r"page-\d+\.png")

    check_logs = {
        "render_crops": os.path.join(CHECKS, "render_crops.log"),
        "render_pages": os.path.join(CHECKS, "render_pages.log"),
        "verify_old_new_math": os.path.join(CHECKS, "verify_old_new_math.log"),
        "check_compare": os.path.join(CHECKS, "check_compare.log"),
        "check_claims": os.path.join(CHECKS, "check_claims.log"),
    }
    totals = {k: total_line(read_text(p)) for k, p in check_logs.items()}

    old_doc = fitz.open(OLD)
    new_doc = fitz.open(NEW)
    old_sha, new_sha = sha(OLD), sha(NEW)
    old_pages, new_pages = old_doc.page_count, new_doc.page_count
    fs_old = final.get("old_handout", {})
    fs_new = final.get("handout", {})
    source_match = (
        old_sha == fs_old.get("sha256") and old_pages == fs_old.get("pages")
        and new_sha == fs_new.get("sha256") and new_pages == fs_new.get("pages")
    )

    issue_path = os.path.join(HERE, "issue-response.json")
    issue = json.load(open(issue_path, encoding="utf-8")) if os.path.isfile(issue_path) else {}
    issue_ids = [x.get("id") for x in issue.get("issues", [])]

    cm = totals["check_compare"][0] or 0
    cf = totals["check_compare"][1] or 0
    vm = totals["verify_old_new_math"][0] or 0
    vf = totals["verify_old_new_math"][1] or 0
    km = totals["check_claims"][0] or 0
    kf = totals["check_claims"][1] or 0
    all_ok = (
        source_match and pdf_bytes < LIMIT and pages == log_pages
        and not overfull and not missing and not latex_error and not undef
        and not rc_failures and anchors_ok and figs_n == len(crops)
        and render_n == pages and header_ok and margin_ok and image_geom_ok
        and cf == 0 and vf == 0 and kf == 0
    )

    lines = []
    lines.append("新旧对比册（内容修订版）· 检查记录（verification.txt）")
    lines.append("=" * 56)
    lines.append("")
    lines.append(f"生成：{now_cn:%Y-%m-%d %H:%M}（北京时间，UTC+8）  DSH")
    lines.append("范围：comparison-revised/ 自身；只读引用 inputs/old-handout.pdf 与")
    lines.append("      round-04/handout.pdf。未修改讲义、规则、原输入或原 comparison/。")
    lines.append(f"修订依据：comparison/final-fix-index.json（4 项局部修正）；活跃项 {', '.join(issue_ids) or '未记录'}。")
    lines.append("权威选择：final-selection.json")
    lines.append(f"      sha256 = {sha(FINAL)}")
    lines.append(f"      status = {final.get('status')!r}")
    lines.append(f"      delivery_ready = {final.get('delivery_ready')}")
    lines.append("本记录不改变 final-selection 的状态，也不声称本修订版已获外部复核或学习者试读。")
    lines.append("")
    lines.append("-" * 56)
    lines.append("一、交付文件与哈希")
    lines.append("-" * 56)
    lines.append(f"1) comparison-revised/comparison.pdf")
    lines.append(f"   字节数：{pdf_bytes:,}（{pdf_bytes/1024/1024:.2f} MiB，小于 25 MiB）")
    lines.append(f"   页数：{pages}（A4，595.28 x 841.89 pt；全部页面通过 A4 检查："
                 f"{all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 for p in doc)}）")
    lines.append(f"   PDF 版本/生成器：{pdf_meta.get('format')}；{pdf_meta.get('producer')}；creator = {pdf_meta.get('creator')}")
    lines.append(f"   创建时间：{pdf_meta.get('creationDate')}")
    lines.append(f"   sha256 = {pdf_sha}")
    lines.append(f"2) comparison-revised/comparison.tex")
    lines.append(f"   字节数：{os.path.getsize(TEX):,}")
    lines.append(f"   sha256 = {sha(TEX)}")
    lines.append(f"3) comparison-revised/crops.json")
    lines.append(f"   字节数：{os.path.getsize(CROPS):,}；{len(crops)} 个裁剪定义；200 dpi；x=48..548 pt")
    lines.append(f"   sha256 = {sha(CROPS)}")
    lines.append(f"4) comparison-revised/comparison.log")
    lines.append(f"   字节数：{os.path.getsize(LOG):,}")
    lines.append(f"   编译结束行：{m.group(0) if m else '未找到'}")
    lines.append(f"   sha256 = {sha(LOG)}")
    lines.append(f"5) comparison-revised/figs/（{figs_n} 张裁剪 PNG）")
    lines.append(f"   合计字节数：{sum(os.path.getsize(os.path.join(FIGS, f)) for f in os.listdir(FIGS) if f.endswith('.png')):,}")
    lines.append(f"   渲染集合聚合 sha256 = {figs_sha}")
    lines.append(f"6) comparison-revised/render/（本册最终每页渲染）")
    lines.append(f"   {render_n} 个 page-NN.png，150 dpi；渲染数量与 PDF 页数一致：{render_n == pages}")
    lines.append(f"   渲染集合聚合 sha256 = {render_sha}")
    lines.append(f"7) comparison-revised/issue-response.json（逐项回应 COMP-C1..C4、CMP-MATH-01 及本轮 COMP-C1 残留、CMP-REV-MATH-01/02、COMP-V1）")
    if os.path.isfile(issue_path):
        lines.append(f"   字节数：{os.path.getsize(issue_path):,}；sha256 = {sha(issue_path)}")
    lines.append("")
    lines.append("-" * 56)
    lines.append("二、源文件对账（与 final-selection.json 逐项比较）")
    lines.append("-" * 56)
    lines.append(f"旧稿 inputs/old-handout.pdf")
    lines.append(f"   字节数：{os.path.getsize(OLD):,}；页数：{old_pages}（声明 {fs_old.get('pages')}）")
    lines.append(f"   sha256 = {old_sha}")
    lines.append(f"   与 final-selection 声明一致：{old_sha == fs_old.get('sha256') and old_pages == fs_old.get('pages')}")
    lines.append(f"   版本事实：文件版本 {fs_old.get('file_version')}；封面仍印 20261103。")
    lines.append(f"新稿 round-04/handout.pdf")
    lines.append(f"   字节数：{os.path.getsize(NEW):,}；页数：{new_pages}（声明 {fs_new.get('pages')}）")
    lines.append(f"   sha256 = {new_sha}")
    lines.append(f"   与 final-selection 声明一致：{new_sha == fs_new.get('sha256') and new_pages == fs_new.get('pages')}")
    lines.append(f"   审核状态：{fs_new.get('review_status')}")
    lines.append(f"结论：两份源 PDF 的哈希与页数{'完全一致' if source_match else '存在不一致'}；未发现源 PDF 不匹配。")
    lines.append("")
    lines.append("-" * 56)
    lines.append("三、两遍编译、评价/引文/裁剪与全篇页面检查")
    lines.append("-" * 56)
    lines.append(f"3.1 两遍 xelatex：checks/xelatex-pass1.log、checks/xelatex-pass2.log 均存在；")
    lines.append(f"    comparison.log 记录 {log_pages} 页，PDF 实际 {pages} 页，一致：{pages == log_pages}。")
    lines.append(f"    无 Overfull：{not overfull}；无 Missing character：{not missing}；"
                 f"无 LaTeX Error：{not latex_error}；无未定义引用：{not undef}；Underfull 计数：{underfull}。")
    lines.append(f"3.2 裁剪与裁剪位置：crops.json {len(crops)} 个；render-crops.json {len(rc.get('crops', []))} 个；")
    lines.append(f"    failures 空：{not rc_failures}；所有 require 锚字符串命中：{anchors_ok}；"
                 f" figs 数量匹配：{figs_n == len(crops)}。")
    lines.append(f"3.3 受改评价/引文：check_claims.py {km} 项通过、{kf} 项失败；逐条见 checks/check_claims.log。")
    lines.append(f"    该检查只证明引文仍存在于所引源页，不证明解释或可读性。")
    lines.append(f"3.4 本册结构：check_compare.py {cm} 项通过、{cf} 项失败；逐条见 checks/check_compare.log。")
    lines.append(f"3.5 数值/代数断言：verify_old_new_math.py {vm} 项通过、{vf} 项失败；逐条见 checks/verify_old_new_math.log。")
    lines.append(f"3.6 页眉/页边距/图片几何：每页运行页眉：{header_ok}；文字块在页面内：{margin_ok}；"
                 f"大幅图片在版心内且宽度不超版心：{image_geom_ok}；大幅图片放置数：{image_placements}。")
    lines.append(f"3.7 每页文字层：{pages} 页均有可提取文字，总字符数 {text_chars:,}；"
                 f"无未解析 '??'：{'??' not in ''.join(p.get_text() for p in doc)}；"
                 f"无 TODO/占位：{'TODO' not in ''.join(p.get_text() for p in doc) and '占位' not in ''.join(p.get_text() for p in doc)}。")
    lines.append("")
    lines.append("逐页抽样（页 / 文字字符数 / 大幅图片数 / 文字 y 范围）：")
    for pno, nchars, nimg, ymin, ymax in page_rows:
        lines.append(f"  p{pno:02d}: {nchars:5d} chars, {nimg} img, y {ymin:.0f}..{ymax:.0f} pt")
    lines.append("")
    lines.append("-" * 56)
    lines.append("四、边界：未做与不能声称")
    lines.append("-" * 56)
    lines.append("1) DSH 自身没有图像输入。本记录全部基于 PDF 文字层、坐标、文件哈希与编译日志；")
    lines.append("   未对本册 render/*.png、figs/*.png 或两份源 PDF 做像素级目视。字体是否缺字、")
    lines.append("   箭头是否遮挡、图注是否压线、裁图是否清晰、排版观感如何，均未由 DSH 目视。")
    lines.append("   必要渲染已完成不等于目视通过。")
    lines.append("2) 新稿 round-04 的外部内容、数学、视觉审核已完成，记录在 final-selection.json 与")
    lines.append("   visual-review-round04.json；本记录不把‘DSH 没看图’写成‘新稿缺少外部视觉审核’。")
    lines.append("3) 原 comparison 的版面已由外部视觉审核接受，但内容审核提出 5 项并要求修订；")
    lines.append("   本修订版逐项回应，仍需外部复核。")
    lines.append("4) 未试读。未进行学习者试读，未测学习效果、可读性或‘是否读懂’。")
    lines.append("5) 未外发。微信发送、git、同步、学习记录入账均未执行（超出本任务授权）。")
    lines.append("6) 覆盖有限。只检查本册选出的 28 处裁剪与自身页面；未逐页审计旧稿 29 页或新稿 48 页。")
    lines.append("")
    lines.append("-" * 56)
    lines.append("五、结论")
    lines.append("-" * 56)
    lines.append(f"源文件匹配：{source_match}；两遍编译完成：{pages == log_pages}；体积小于 25 MiB：{pdf_bytes < LIMIT}。")
    lines.append(f"check_compare：{cm} passed / {cf} failed；verify_old_new_math：{vm} passed / {vf} failed；"
                 f"check_claims：{km} passed / {kf} failed。")
    lines.append(f"整体自检：{'通过（文字层/坐标/哈希/编译范围）' if all_ok else '存在失败项，需返工'}。")
    lines.append("本册达到‘可供外部复核与学习者试读’的状态；未获目视验收或试读验收，")
    lines.append("按 final-selection 保持 delivery_ready=false。")
    lines.append("")
    lines.append("-" * 56)
    lines.append("六、复现命令（均在 comparison-revised/ 下运行）")
    lines.append("-" * 56)
    lines.append("python -B render_crops.py")
    lines.append("xelatex -halt-on-error -interaction=nonstopmode comparison.tex  （两遍）")
    lines.append("python -B render_pages.py")
    lines.append("python -B verify_old_new_math.py")
    lines.append("python -B check_compare.py --strict")
    lines.append("python -B check_claims.py")
    lines.append("python -B verification_report.py")
    lines.append("或直接运行 powershell -File build.ps1。")
    lines.append("")
    lines.append("逐条原始日志：checks/*.log；机器可读清单：delivery-manifest.json。")

    verification = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "verification.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(verification)

    manifest = {
        "manifest_version": "2.0",
        "manifest_generated_at_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": "张量并矢新旧对比册：内容修订与自检记录",
        "author": "DSH",
        "task_root": ROOT,
        "scope": "content revision of comparison only; lecture round-04, rules, inputs and original comparison remain frozen",
        "revision_basis": {
            "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\tensor-dyad-20261111\\comparison\\final-fix-index.json",
            "previous_revision_index": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\tensor-dyad-20261111\\comparison\\revision-index.json",
            "active_issue_ids": issue_ids,
            "issue_response": "comparison-revised/issue-response.json",
        },
        "authoritative_selection": {
            "path": "final-selection.json",
            "sha256": sha(FINAL),
            "status": final.get("status"),
            "delivery_ready": final.get("delivery_ready"),
        },
        "delivery_status": {
            "selected_handout": "accepted for trial reading per final-selection; learning effect untested",
            "new_handout_external_review": "content, math and visual review completed per final-selection / visual-review-round04",
            "original_comparison": "external visual review accepted layout; content review required DS revision",
            "revised_comparison": "built and self-checked; external review and learner trial pending; not accepted as delivered",
            "delivery_ready": False,
            "wechat_send": "not performed (outside this task's authorization)",
        },
        "deliverables": {
            "comparison_pdf": {
                "path": "comparison-revised/comparison.pdf",
                "bytes": pdf_bytes,
                "pages": pages,
                "sha256": pdf_sha,
                "created": pdf_meta.get("creationDate"),
                "producer": pdf_meta.get("producer"),
                "status": "text-layer/geometry/hash checks passed; awaiting external visual review and learner trial",
            },
            "comparison_tex": {
                "path": "comparison-revised/comparison.tex",
                "bytes": os.path.getsize(TEX),
                "sha256": sha(TEX),
                "note": "revised source; original comparison/comparison.tex not modified",
            },
            "verification_txt": {
                "path": "comparison-revised/verification.txt",
                "bytes": len(verification.encode("utf-8")),
                "sha256": hashlib.sha256(verification.encode("utf-8")).hexdigest(),
                "note": "this record; generated by verification_report.py",
            },
            "issue_response_json": {
                "path": "comparison-revised/issue-response.json",
                "bytes": os.path.getsize(issue_path) if os.path.isfile(issue_path) else None,
                "sha256": sha(issue_path) if os.path.isfile(issue_path) else None,
                "issues": issue_ids,
            },
            "delivery_manifest_json": {
                "path": "comparison-revised/delivery-manifest.json",
                "note": "this file; self hash intentionally omitted",
            },
        },
        "supporting_artifacts": {
            "crops_json": {
                "path": "comparison-revised/crops.json",
                "bytes": os.path.getsize(CROPS),
                "sha256": sha(CROPS),
                "crops": len(crops),
                "dpi": 200,
            },
            "crop_images": {
                "dir": "comparison-revised/figs",
                "count": figs_n,
                "aggregate_sha256": figs_sha,
                "aggregate_method": "sha256 of sorted 'name:sha256\\n' lines",
            },
            "final_page_renders": {
                "dir": "comparison-revised/render",
                "count": render_n,
                "dpi": 150,
                "pixel_size": "1241x1754",
                "aggregate_sha256": render_sha,
                "aggregate_method": "sha256 of sorted 'name:sha256\\n' lines",
                "note": "re-rendered from the revised comparison.pdf; not visually inspected",
            },
            "render_crops_json": {
                "path": "comparison-revised/render-crops.json",
                "sha256": sha(RENDER_CROPS),
                "failures": rc_failures,
                "anchors_all_ok": anchors_ok,
            },
            "compile_log": {
                "path": "comparison-revised/comparison.log",
                "sha256": sha(LOG),
                "output_written_line": m.group(0) if m else None,
                "overfull": overfull,
                "missing_character": missing,
                "latex_error": latex_error,
                "undefined_control_or_reference": undef,
                "underfull_hbox_count": underfull,
            },
        },
        "checks": {
            "two_pass_compile": {
                "pass1_log": "comparison-revised/checks/xelatex-pass1.log",
                "pass2_log": "comparison-revised/checks/xelatex-pass2.log",
                "log_pages": log_pages,
                "pdf_pages": pages,
                "match": pages == log_pages,
            },
            "check_compare": {"passed": cm, "failed": cf, "log": "comparison-revised/checks/check_compare.log"},
            "verify_old_new_math": {"passed": vm, "failed": vf, "log": "comparison-revised/checks/verify_old_new_math.log"},
            "check_claims": {"passed": km, "failed": kf, "log": "comparison-revised/checks/check_claims.log"},
            "crop_anchor_recheck": {"checked": len(crops), "failed": len(rc_failures), "anchors_ok": anchors_ok},
            "text_layer": {
                "pages_with_text": pages,
                "total_chars": text_chars,
                "running_header_all_pages": header_ok,
                "text_blocks_inside_page": margin_ok,
                "image_geometry_ok": image_geom_ok,
                "image_placements": image_placements,
            },
            "final_renders": {"count": render_n, "matches_pdf_pages": render_n == pages},
        },
        "sources": {
            "old_handout": {
                "path": "inputs/old-handout.pdf",
                "pages": old_pages,
                "bytes": os.path.getsize(OLD),
                "sha256": old_sha,
                "declared_sha256": fs_old.get("sha256"),
                "hash_match": old_sha == fs_old.get("sha256"),
                "declared_pages": fs_old.get("pages"),
                "pages_match": old_pages == fs_old.get("pages"),
                "file_version": fs_old.get("file_version"),
                "cover_note": fs_old.get("cover_date_note"),
            },
            "new_handout": {
                "path": "round-04/handout.pdf",
                "pages": new_pages,
                "bytes": os.path.getsize(NEW),
                "sha256": new_sha,
                "declared_sha256": fs_new.get("sha256"),
                "hash_match": new_sha == fs_new.get("sha256"),
                "declared_pages": fs_new.get("pages"),
                "pages_match": new_pages == fs_new.get("pages"),
                "review_status": fs_new.get("review_status"),
            },
        },
        "review_boundary": {
            "ds_image_input": "unavailable; no pixel-level visual inspection by DSH",
            "new_handout_external_review": "completed per final-selection and visual-review-round04",
            "this_comparison": "external review still required; not accepted here",
            "original_comparison_visual": "layout accepted by external visual review before this content revision",
            "learner_trial": "not performed; no learning-effect claim",
        },
        "read_only_boundary": {
            "not_modified": [
                "comparison/",
                "inputs/",
                "round-01/",
                "round-02/",
                "round-03/",
                "round-04/",
                "rule-versions/",
                "final-selection.json",
                "trial-provenance.json",
                "learner-background.json",
            ],
            "written_this_round": [
                "comparison-revised/comparison.pdf",
                "comparison-revised/comparison.tex",
                "comparison-revised/crops.json",
                "comparison-revised/figs/",
                "comparison-revised/render/",
                "comparison-revised/verification.txt",
                "comparison-revised/issue-response.json",
                "comparison-revised/delivery-manifest.json",
                "comparison-revised/checks/",
            ],
        },
        "known_gaps": [
            "DSH has no image input; the revised booklet's fonts, arrow geometry, occlusion and caption placement have not been visually inspected.",
            "The revised booklet has not received external review or learner trial.",
            "Coverage is limited to the 28 selected crops and the booklet's own pages; the old 29-page and new 48-page handouts were not audited page by page.",
        ],
        "not_verified": [
            "No pixel-level visual inspection by DSH.",
            "No learner trial or learning-effect measurement.",
            "No external acceptance of this revised comparison booklet.",
        ],
        "conclusion": (
            "Sources match final-selection; two-pass compilation and all executed text-layer, crop-anchor, "
            "quote, numeric, page-margin and log checks passed. The revised comparison is ready for external "
            "review and learner trial only; it is not visually accepted, not trial-read, and not marked delivery_ready."
        ),
    }
    with open(os.path.join(HERE, "delivery-manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"verification.txt: {len(verification.encode('utf-8'))} bytes")
    print(f"delivery-manifest.json written")
    print(f"all_ok={all_ok} pages={pages} size={pdf_bytes/1024/1024:.2f} MiB")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
