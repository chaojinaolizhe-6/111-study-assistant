import unittest

import numpy as np
import pandas as pd
from scipy.stats import norm

from aq.labels import forward_open_return
from aq import metrics, stats


class InferenceTests(unittest.TestCase):
    def test_open_label_and_security_boundaries(self):
        prices = pd.Series([10., 20., 25., 30., 100., 120., 150., 180.])
        groups = pd.Series(["a"] * 4 + ["b"] * 4)
        actual = forward_open_return(prices, 2, groups)
        self.assertAlmostEqual(actual[0], .5)
        self.assertAlmostEqual(actual[4], .5)
        self.assertTrue(actual[[1, 2, 3, 5, 6, 7]].isna().all())

    def test_missing_open_is_not_filled(self):
        p = pd.Series([10., np.nan, 13., 14.])
        self.assertTrue(np.isnan(forward_open_return(p, 1).iloc[0]))
        self.assertAlmostEqual(forward_open_return(p, 1).iloc[1], 14 / 13 - 1)

    def test_hac_against_bartlett_matrix(self):
        x = np.random.default_rng(42).normal(.02, .1, 80)
        e = x - x.mean()
        lag = 8
        distances = np.abs(np.arange(len(x))[:, None] - np.arange(len(x)))
        kernel = np.maximum(0, 1 - distances / (lag + 1))
        var_mean = e @ kernel @ e / len(x) ** 2
        d = metrics.mean_inference(pd.Series(x), lag)
        self.assertAlmostEqual(d["t_nw"], x.mean() / np.sqrt(var_mean), places=10)
        self.assertAlmostEqual(d["n_eff"], np.mean(e ** 2) / var_mean, places=10)

    def test_pooling_does_not_average_t(self):
        x = pd.DataFrame({"f": np.random.default_rng(4).normal(.01, .1, 100)})
        old = pd.DataFrame({"factor": ["f"], "t_nw": [999.]})
        out = metrics.pooled_factor_summary(old, x).iloc[0]
        self.assertAlmostEqual(out.t_nw, metrics.mean_inference(x.f)["t_nw"])
        self.assertEqual(out.n, 100)

    def test_dsr_monotonic_and_annualization(self):
        x = np.random.default_rng(3).normal(.005, .025, 400)
        a = stats.deflated_sharpe(x, n_trials=15, sigma_sr=.05, periods=50.4)
        b = stats.deflated_sharpe(x, n_trials=100, sigma_sr=.05, periods=50.4)
        self.assertGreater(a["dsr"], b["dsr"])
        self.assertAlmostEqual(b["sr_ann"], stats.sharpe(x, 50.4))
        benchmark = .05 * ((1 - stats.EULER) * norm.ppf(.99)
                           + stats.EULER * norm.ppf(1 - 1 / (100 * np.e)))
        self.assertAlmostEqual(b["sr0"], benchmark)

    def test_pbo_ties_are_order_invariant(self):
        x = np.random.default_rng(7).normal(size=120)
        r = np.column_stack([x, x, x])
        a = stats.pbo_cscv(r, n_blocks=4)
        self.assertTrue(np.allclose(a["oos_rank"], .5))


if __name__ == "__main__":
    unittest.main()
