"""Rebuild both PDFs and shared empirical tables from current CSV/JSON outputs."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aq import config
from aq.audit import file_hash
from aq.reporting import factor_table, dsr_table, inference_note, table, esc

import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables-only", action="store_true")
    args = ap.parse_args()
    rep, lec = config.REPORTS, config.ROOT / "lectures"
    main = pd.read_csv(rep / "factor_eval.csv")
    flow = pd.read_csv(rep / "flow_factor_eval.csv")
    quality = pd.read_csv(rep / "quality_factor_eval.csv")
    sens = pd.read_csv(rep / "dsr_sensitivity.csv")
    diag = json.loads((rep / "diagnostics.json").read_text(encoding="utf-8"))
    cand = pd.read_csv(rep / "candidates_oos.csv")
    for name, frame, supplemental in [("factor", main, False), ("flow", flow, True),
                                       ("quality", quality, True)]:
        tex = "{\\small\n" + factor_table(frame, supplemental, long=True) + "\n}\n"
        (lec / f"generated_{name}_table.tex").write_text(tex, encoding="utf-8")
    (lec / "generated_inference_note.tex").write_text(inference_note(), encoding="utf-8")
    (lec / "generated_dsr_table.tex").write_text(dsr_table(sens), encoding="utf-8")
    crows = [[esc(r.label), str(r.n_dates), f"{r.ic_mean:.4f}",
              f"{r.icir_ann:.2f}", f"{r.t_nw:.2f}", f"{r.ls_ann_net*100:.1f}" + r"\%",
              f"{r.sharpe_net:.2f}"] for r in cand.itertuples()]
    (lec / "generated_candidates.tex").write_text(table(
        ["候选", "IC 日期数", "IC", "ICIR", r"NW $t$", "年化", "夏普"], crows, "lrrrrrr"), encoding="utf-8")
    f = flow.set_index("factor")
    q = quality.set_index("factor")
    d100 = sens[(sens.n_trials_assumed == 100) & (sens.sigma_source == "observed_candidates")].iloc[0]
    values = {
        "DSRStress": f"{diag['dsr']['dsr']:.4f}", "DSRHundred": f"{d100.dsr:.4f}",
        "PBO": f"{diag['pbo']:.3f}", "CommonN": str(diag["wf_periods"]),
        "CorrMin": f"{diag['candidate_corr_min']:.3f}", "CorrMax": f"{diag['candidate_corr_max']:.3f}",
        "FlowMfr": f"{f.loc['mfr', 'ic_mean']:+.4f}",
        "FlowPos": f"{f.loc['mfr_pos_20', 'ic_inc']:+.4f}",
        "FlowPosT": f"{f.loc['mfr_pos_20', 't_inc']:.2f}",
        "QCfoN": f"{q.loc['q_cfo_ni', 'n_eff']:.0f}",
        "QCfoCount": f"{q.loc['q_cfo_ni', 'n']:.0f}",
        "QCfoT": f"{q.loc['q_cfo_ni', 't_nw']:.2f}",
        "QCfoNaive": f"{q.loc['q_cfo_ni', 't_naive']:.2f}",
        "BPLower": f"{diag['bootstrap']['p025']:.2f}",
        "BPUpper": f"{diag['bootstrap']['p975']:.2f}",
    }
    macros = "\n".join(r"\newcommand{\Audit" + k + "}{" + v + "}" for k, v in values.items())
    (lec / "generated_audit_values.tex").write_text(macros + "\n", encoding="utf-8")
    readme = config.ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if "<!-- AUDIT-RESULTS:START -->" in text:
        a = text.index("<!-- AUDIT-RESULTS:START -->")
        b = text.index("<!-- AUDIT-RESULTS:END -->", a) + len("<!-- AUDIT-RESULTS:END -->")
        body = f"""<!-- AUDIT-RESULTS:START -->
修订后的两批因子均使用次日开盘到第六日开盘标签，原始/调整后 IC 从完整序列汇总：

- 资金流 `mfr` IC **{values['FlowMfr']}**；`mfr_pos_20` 增量 IC **{values['FlowPos']}**，HAC t **{values['FlowPosT']}**。这是补充池的条件关联，尚未加入模型重训。
- 撤回质量因子“全部不显著”和“只有 14 个有效样本”的旧结论：旧表误将年度 t 的平均当全样本 t。现表包含 `n`、`nw_lags`、`n_eff` 和调整后有效样本量；`q_cfo_ni` 的方差等价样本量为 **{values['QCfoN']}**（{values['QCfoCount']} 个有值日期），依赖带宽选择。
- DSR 压力情景 **{values['DSRStress']}**（假定 603 个独立试验及零假设离散度下限）。603 是情景，完整搜索史未知，不能声称整个研究通过多重检验。
- PBO **{values['PBO']}** 仅覆盖五候选、{values['CommonN']} 个共同有效日期；相关系数范围 {values['CorrMin']}–{values['CorrMax']}。缺失收益不再填零。
- `reports/dsr_sensitivity.csv` 和 `reports/ic_inference_sensitivity.csv` 保存完整敏感性结果；所有结果均属被反复查看过的历史数据内验证。
<!-- AUDIT-RESULTS:END -->"""
        readme.write_text(text[:a] + body + text[b:], encoding="utf-8")
    if args.tables_only:
        return 0
    subprocess.run([sys.executable, "-X", "utf8", str(config.ROOT / "scripts/08_report.py")], check=True)
    exe = shutil.which("xelatex")
    if not exe:
        raise RuntimeError("xelatex is required")
    for i in range(2):
        run = subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                             cwd=lec, capture_output=True)
        (rep / f"lecture-compile-{i+1}.txt").write_bytes(run.stdout + run.stderr)
        run.check_returncode()
    manifest = {"inputs_sha256": {str(p.relative_to(config.ROOT)): file_hash(p)
                                  for p in lec.glob("*.tex")},
                "pdf_sha256": file_hash(lec / "main.pdf")}
    for name in ("factor_eval.csv", "flow_factor_eval.csv", "quality_factor_eval.csv",
                 "dsr_sensitivity.csv", "diagnostics.json", "candidates_oos.csv"):
        manifest["inputs_sha256"]["reports/" + name] = file_hash(rep / name)
    for name in ("scripts/13_refresh_documents.py", "aq/reporting.py", "research_search.json"):
        manifest["inputs_sha256"][name] = file_hash(config.ROOT / name)
    (rep / "lecture_inputs.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("[documents] both report and lecture rebuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
