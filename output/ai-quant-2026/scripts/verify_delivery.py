"""交付物自检：逐条核对目标里承诺的东西是否真的存在且可用。

用法: python scripts/verify_delivery.py
退出码 0 表示全部通过。
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aq.config import DB_PATH, REPORTS, DATA  # noqa: E402
from aq.factors import FACTORS  # noqa: E402

ok, fail = [], []


def check(name: str, cond: bool, detail: str = "") -> None:
    (ok if cond else fail).append(f"{'PASS' if cond else 'FAIL'}  {name}"
                                  + (f"  [{detail}]" if detail else ""))


def pdf_pages(p: Path) -> int:
    """页数取自 LaTeX 日志（xelatex 的 PDF 用了对象流，直接解析不可靠）。"""
    if not p.exists():
        return 0
    log = p.with_suffix(".log")
    if not log.exists():
        log = p.parent / "report.log"   # 报告编译产物名固定为 report.log
    if log.exists():
        m = re.search(r"Output written on .*?\((\d+) pages?\)",
                      log.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return int(m.group(1))
    d = p.read_bytes()
    nums = [int(x) for x in re.findall(rb"/Count\s+(\d+)", d)]
    return max(nums) if nums else 0


# ---------------- ① 讲义 ----------------
lec = ROOT / "lectures" / "main.pdf"
check("讲义 PDF 存在", lec.exists(), f"{lec.name}")
check("讲义页数 >= 60", pdf_pages(lec) >= 60, f"{pdf_pages(lec)} 页")
chapters = sorted((ROOT / "lectures").glob("ch*.tex"))
check("讲义章节文件 >= 13", len(chapters) >= 13, f"{len(chapters)} 个")
check("外部意见交叉核验章节存在",
      (ROOT / "lectures" / "appendix_cross.tex").exists())

# ---------------- ② 数据库 ----------------
conn = sqlite3.connect(str(DB_PATH))
q = lambda s: conn.execute(s).fetchone()[0]  # noqa: E731

need = {"stock": 5000, "bar": 10_000_000, "fin": 200_000, "valuation": 300_000,
        "index_bar": 10_000, "index_member": 500, "trade_calendar": 5_000,
        "shm_bar": 5_000_000, "shm_moneyflow": 5_000_000, "shm_valuation": 9_000_000}
for t, least in need.items():
    try:
        n = q(f"SELECT COUNT(*) FROM {t}")
        check(f"表 {t} 行数 >= {least:,}", n >= least, f"{n:,}")
    except sqlite3.Error as e:
        check(f"表 {t} 存在", False, str(e))

check("行情覆盖 >= 5000 只", q("SELECT COUNT(DISTINCT code) FROM bar") >= 5000,
      f"{q('SELECT COUNT(DISTINCT code) FROM bar')} 只")
check("财报带公告日（PIT）", q("SELECT COUNT(*) FROM fin WHERE notice_date IS NOT NULL") > 100_000,
      f"{q('SELECT COUNT(*) FROM fin WHERE notice_date IS NOT NULL'):,} 条")
check("复权因子齐全", q("SELECT COUNT(*) FROM bar WHERE adj_factor IS NULL") == 0)
check("收盘价无异常", q("SELECT COUNT(*) FROM bar WHERE close IS NULL OR close<=0") == 0)
bar_cols = {r[1] for r in conn.execute("PRAGMA table_info(bar)")}
check("行情表含股票池过滤所需字段",
      {"volume", "amount", "turnover", "adj_factor", "pre_close"} <= bar_cols,
      f"缺 {sorted({'volume','amount','turnover','adj_factor','pre_close'} - bar_cols)}")

# ---------------- ③ 因子库 ----------------
check("因子数 >= 35", len(FACTORS) >= 35, f"{len(FACTORS)} 个")
missing_meta = [f.name for f in FACTORS.values()
                if not f.formula or f.direction not in (-1, 1) or f.window < 1]
check("每个因子都有公式/方向/回看期", not missing_meta, f"缺字段: {missing_meta}")
check("因子面板已落盘", len(list((DATA / "factors").glob("*.parquet"))) >= 15,
      f"{len(list((DATA / 'factors').glob('*.parquet')))} 个年度文件")
fe = REPORTS / "factor_eval.csv"
check("单因子评价表存在", fe.exists())
if fe.exists():
    import pandas as pd
    ev = pd.read_csv(fe)
    check("评价表覆盖 >= 35 个因子", len(ev) >= 35, f"{len(ev)} 行")
    check("含中性化后 IC 列", "ic_mean_neu" in ev.columns)

# ---------------- ④ 拟合精度报告 ----------------
rep = REPORTS / "拟合精度报告.pdf"
check("拟合精度报告 PDF 存在", rep.exists(), f"{rep.name}")
check("报告页数 >= 5", pdf_pages(rep) >= 5, f"{pdf_pages(rep)} 页")
diag_f = REPORTS / "diagnostics.json"
check("diagnostics.json 存在", diag_f.exists())
if diag_f.exists():
    d = json.loads(diag_f.read_text(encoding="utf-8"))
    for k, desc in [("best_ic", "样本外 Rank IC"), ("pbo", "PBO"),
                    ("rc_p", "Reality Check p"), ("dsr", "Deflated Sharpe")]:
        check(f"报告含 {desc}", k in d)
    check("DSR 数值在 [0,1]", 0 <= d.get("dsr", {}).get("dsr", -1) <= 1,
          f"{d.get('dsr', {}).get('dsr'):.3f}")
    check("PBO 数值在 [0,1]", 0 <= d.get("pbo", -1) <= 1, f"{d.get('pbo'):.3f}")
for f, desc in [("flow_factor_eval.csv", "资金流因子评价"),
                ("quality_factor_eval.csv", "质量因子评价")]:
    check(f"{desc}存在", (REPORTS / f).exists())

mt = REPORTS / "model_tests.csv"
check("多协议测试结果存在", mt.exists())
if mt.exists():
    import pandas as pd
    t = pd.read_csv(mt)
    check("覆盖三种验证协议", t["protocol"].nunique() >= 3,
          str(sorted(t["protocol"].unique())))

# ---------------- ⑤ 修订口径与产物新鲜度 ----------------
from aq.audit import file_hash
from aq import metrics
import numpy as np

for family, filename in [("main", "factor_eval.csv"), ("flow", "flow_factor_eval.csv"),
                         ("quality", "quality_factor_eval.csv")]:
    path = REPORTS / filename
    if path.exists():
        frame = pd.read_csv(path)
        fields = {"n", "n_eff", "nw_lags", "t_naive", "summary_method", "label"}
        check(f"{family} 含统一有效样本字段", fields <= set(frame.columns))
        if fields <= set(frame.columns):
            check(f"{family} 从完整 IC 汇总", frame.summary_method.eq("pooled_daily_ic_h5_bartlett_hac").all())
            check(f"{family} 标签为开盘到开盘", frame.label.eq("adj_open_t6_over_t1_minus_1").all())
            check(f"{family} 有效样本为正", frame.n_eff.dropna().gt(0).all())

if diag_f.exists():
    check("DSR 不作完整搜索通过判定", d.get("dsr_status") == "sensitivity_only_search_history_incomplete")
    check("DSR 使用五日收益年化", np.isclose(d["dsr"]["sr_ann"], d["dsr"]["sr"] * np.sqrt(252 / 5)))
    check("诊断未把缺失收益填零", d.get("diagnostic_return_policy") == "complete_case_common_dates_no_zero_fill")
    check("Bootstrap 95% 采用正确分位", {"p025", "p975"} <= set(d.get("bootstrap", {})))
    check("PBO 明示五候选边界", d.get("pbo_scope") == "observed_5_candidates_only_not_full_research_search")

for name, folder, pdf in [("report", REPORTS, rep), ("lecture", ROOT, lec)]:
    manifest_file = REPORTS / f"{name}_inputs.json"
    check(f"{name} 存在输入哈希清单", manifest_file.exists())
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        stale = [f for f, digest in manifest["inputs_sha256"].items()
                 if not (folder / f).exists() or file_hash(folder / f) != digest]
        check(f"{name} 与最新输入一致", not stale, str(stale))
        check(f"{name} PDF 与清单一致", file_hash(pdf) == manifest["pdf_sha256"])

check("DSR 敏感性表存在", (REPORTS / "dsr_sensitivity.csv").exists())
check("IC 带宽与采样敏感性表存在", (REPORTS / "ic_inference_sensitivity.csv").exists())
check("质量原始与增量 IC 可追溯", (DATA / "quality_ic.parquet").exists()
      and (DATA / "quality_ic_inc.parquet").exists())

# ---------------- 汇总 ----------------
print("\n".join(ok))
if fail:
    print("\n".join(fail))
    print(f"\n结果: {len(ok)} 项通过, {len(fail)} 项失败")
    sys.exit(1)
print(f"\n结果: 全部 {len(ok)} 项通过")
