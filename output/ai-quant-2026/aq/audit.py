"""Recompute inference from saved observations, without fitting new models."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from aq import config, metrics, stats


def search_diagnostics(R: pd.DataFrame, best: str, periods=252 / 5) -> dict:
    # A missing strategy return is not a zero-return cash position.
    R = R.replace([np.inf, -np.inf], np.nan).dropna(how="any")
    if len(R) < 80 or best not in R:
        raise ValueError("Insufficient common candidate return observations")
    inventory = json.loads((config.ROOT / "research_search.json").read_text(encoding="utf-8"))
    sr = R.mean() / R.std(ddof=1)
    sigma_candidates = float(sr.std(ddof=1))
    sigma_floor = max(sigma_candidates, 1 / np.sqrt(len(R) - 1))
    cases = []
    for n in inventory["sensitivity_n_trials"]:
        for source, sigma in [("observed_candidates", sigma_candidates),
                              ("iid_null_floor_scenario", sigma_floor)]:
            d = stats.deflated_sharpe(R[best], n_trials=n, sigma_sr=sigma, periods=periods)
            cases.append({"sigma_source": source, "n_trials_assumed": n, **d})
    sens = pd.DataFrame(cases)
    sens.to_csv(config.REPORTS / "dsr_sensitivity.csv", index=False, encoding="utf-8-sig")
    stress = next(x for x in cases if x["n_trials_assumed"] == inventory["stress_n_trials"]
                  and x["sigma_source"] == "iid_null_floor_scenario")
    pbo = stats.pbo_cscv(R.to_numpy(), n_blocks=16)
    rc = stats.reality_check(R.to_numpy(), n_boot=400, block=8)
    corr = R.corr()
    off = corr.to_numpy()[~np.eye(len(corr), dtype=bool)]
    corr.to_csv(config.REPORTS / "candidate_correlation.csv", encoding="utf-8-sig")
    return {
        "dsr": stress, "dsr_status": "sensitivity_only_search_history_incomplete",
        "search_inventory": inventory, "dsr_sensitivity": cases,
        "sr_ann_correct": stress["sr_ann"], "wf_periods": len(R),
        "diagnostic_return_policy": "complete_case_common_dates_no_zero_fill",
        "candidate_corr_mean": float(off.mean()),
        "candidate_corr_min": float(off.min()), "candidate_corr_max": float(off.max()),
        "candidate_effective_rank": stats.effective_n_trials(R),
        "pbo_scope": "observed_5_candidates_only_not_full_research_search",
        "pbo": float(pbo["pbo"]), "pbo_combos": pbo["n_combos"],
        "pbo_detail": {"pbo": float(pbo["pbo"]), "logits": pbo["logits"].tolist()},
        "rc_p": float(rc["p_value"]), "rc_n_boot": 400,
        "rc_scope": "simplified_zero_benchmark_bootstrap_observed_candidates_only",
        "bootstrap": stats.block_bootstrap_sharpe(R[best], periods=periods),
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def refresh_ic_inference():
    d = pd.read_parquet(config.DATA / "ic_series.parquet")
    raw = d.pivot(index="date", columns="factor", values="ic").sort_index()
    neu = d.pivot(index="date", columns="factor", values="ic_neu").sort_index()
    ev = pd.read_csv(config.REPORTS / "factor_eval.csv")
    ev = metrics.pooled_factor_summary(ev, raw, neu, "_neu")
    ev.to_csv(config.REPORTS / "factor_eval.csv", index=False, encoding="utf-8-sig")
    families = [("main", raw, neu)]
    for name in ("flow", "quality"):
        path = config.DATA / f"{name}_ic.parquet"
        adjusted = config.DATA / f"{name}_ic_inc.parquet"
        if path.exists() and adjusted.exists():
            families.append((name, pd.read_parquet(path), pd.read_parquet(adjusted)))
    rows = []
    for family, a, b in families:
        for kind, frame in [("raw", a), ("adjusted", b)]:
            for name in frame:
                series = frame[name].sort_index()
                # Subsample before dropping missing values to preserve the date grid.
                for step, bandwidths in [(1, [5, 20, 60]), (5, [4, 12])]:
                    s = series.iloc[::step]
                    for lag in bandwidths:
                        rows.append({"family": family, "factor": name, "kind": kind,
                                     "step": step, "ic_mean": s.mean(),
                                     **metrics.mean_inference(s, lag)})
    pd.DataFrame(rows).to_csv(config.REPORTS / "ic_inference_sensitivity.csv",
                             index=False, encoding="utf-8-sig")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
