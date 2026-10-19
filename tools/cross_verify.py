#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""双角色交叉审校工具（Generator vs. Skeptical Examiner，基于 ICML 2024 / EMNLP 2023 交叉质询机制）

用途：
  在向学习者发送复杂讲解、例题解答、H1-H3 提示或新编讲义前，用独立的“挑刺审稿人（Skeptical Examiner）”
  视角做一次零注意力成本的后台自检，拦截三类高频问题：
  1. 未学幻觉（把未讲/0次作答/三态表 ❌ 的内容当成“你已经学过”直接布置作业）；
  2. 符号/正负支/留数/边界条件等数理推导漏洞（配合 tools/verify_math.py）；
  3. 提示不好读（复杂 Unicode 公式挤在正文行内、电报体半截话、把系统记账词塞进教学正文）。

密钥读取优先级（绝不硬编码入库）：
  1. 环境变量 DEEPSEEK_API_KEY
  2. 本地桌面文件 C:/Users/M/Desktop/DSH-api.txt

用法：
  python -B tools/cross_verify.py --text "待检查的回复草稿" [--context "题干与当前三态背景"] [--rewrite]
  python -B tools/cross_verify.py --file path/to/draft.md [--context "题干与当前三态背景"] [--rewrite]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_KEY_FILE = Path("C:/Users/M/Desktop/DSH-api.txt")
API_URL = "https://api.deepseek.com/chat/completions"


def load_api_key() -> str:
    env_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if env_key:
        return env_key
    if DEFAULT_KEY_FILE.is_file():
        raw = DEFAULT_KEY_FILE.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"(sk-[a-zA-Z0-9]+)", raw)
        if match:
            return match.group(1)
    raise RuntimeError(
        "未找到 DeepSeek API Key（请设置环境变量 DEEPSEEK_API_KEY 或确认桌面 DSH-api.txt 存在）"
    )


EXAMINER_SYSTEM_PROMPT = """你是一位严苛但务实的大学理工科教学审稿人（Skeptical Examiner）。
你的唯一任务是对导师准备发给学生的【回复草稿】做交叉质询（Cross-Examination），逐项核查以下 4 条红线：

1. 【未学门禁与防幻觉】：
   - 若背景中标明某考点 `attempts=0`（未开始）、三态表为 `❌ / 未讲 / 未学`，草稿是否错误地假定学生已经学过，或直接让学生做题而没有先讲物理/数学动机、核心公式与最小数字例题？
2. 【数理推导与条件严密性】：
   - 公式符号、正负号分支（如 ±√）、积分上下限、奇点/留数阶数、透镜焦距正负、适用条件是否有误或遗漏？
3. 【可读性与认知负荷（防电报体 & 公式独立成行）】：
   - 凡含分式、根号、积分、求和或嵌套括号的纯 Unicode 公式，是否做到了**单独成行并缩进**？（严禁把长公式嵌在中文长句行内！）
   - 提示是否遵循清晰的「① 定位已对部分 → ② 核心支点/同类最简数字小例子 → ③ 唯一明确的下一步动作」？（严禁说半截话猜谜，也严禁在一次回复里塞入多个追问或四步清单）。
4. 【记账元信息隔离】：
   - 是否把 `exposure=partial`、`needs_verify`、`[教学归纳，非课件原文]`、`（错因假说，待验证）` 等系统审计词塞进了教学段落正文中？（必须统一折叠在回复最末尾的单行 `> 📊 状态记录：...`）。

请严格按以下格式输出审校结果：
结论：[PASS] 或 [NEEDS_FIX]
检查明细：
- 未学门禁：<通过 / 具体问题>
- 数理严密性：<通过 / 具体问题>
- 可读性与公式排版：<通过 / 具体问题>
- 元信息隔离：<通过 / 具体问题>
修改建议：<若为 PASS 写“无”；若为 NEEDS_FIX 给出精炼的逐条修正指令>"""


REWRITE_SYSTEM_PROMPT = """你是大学课程金牌导师。请根据审稿人的【检查明细与修改建议】，将【原回复草稿】重写为清晰、自然、好读的最终教学回复：
- 严格遵守纯 Unicode 数学符号（禁用 $...$ 与 \\frac 等 TeX 命令）；
- 复杂公式单独成行并缩进 2 格；
- 结构清晰：① 肯定已有进展/定位卡点 → ② 直觉支点或最简数字小例子（不剧透原题待算步骤） → ③ 唯一明确的下一步动作；
- 记账/来源声明全部收拢到最底部单行：`> 📊 状态记录：...`。"""


def call_deepseek(system_prompt: str, user_prompt: str, api_key: str, temperature: float = 0.1) -> str:
    payload = {
        "model": "deepseek-chat",
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek API HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Dual-role cross-verification for tutor responses and handouts.")
    parser.add_argument("--text", help="Draft tutor response text to verify.")
    parser.add_argument("--file", help="Path to file containing draft tutor response.")
    parser.add_argument("--context", default="未提供额外背景", help="Problem statement and learner three-state context.")
    parser.add_argument("--rewrite", action="store_true", help="Automatically rewrite the draft if issues are found.")
    args = parser.parse_args()

    if not args.text and not args.file:
        parser.error("必须提供 --text 或 --file")
    draft = args.text if args.text else Path(args.file).read_text(encoding="utf-8")

    try:
        api_key = load_api_key()
        user_msg = f"【题干与当前三态背景】\n{args.context}\n\n【待审校回复草稿】\n{draft}"
        critique = call_deepseek(EXAMINER_SYSTEM_PROMPT, user_msg, api_key, temperature=0.1)
        print("== Skeptical Examiner 交叉审校报告 ==")
        print(critique)
        passed = "[PASS]" in critique.splitlines()[0] if critique else False
        if not passed and args.rewrite:
            print("\n== 自动重写后的可读回复 ==")
            rewrite_msg = f"{user_msg}\n\n【审稿人意见】\n{critique}"
            improved = call_deepseek(REWRITE_SYSTEM_PROMPT, rewrite_msg, api_key, temperature=0.2)
            print(improved)
        return 0 if passed else 1
    except Exception as exc:  # noqa: BLE001
        print(f"CROSS_VERIFY ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
