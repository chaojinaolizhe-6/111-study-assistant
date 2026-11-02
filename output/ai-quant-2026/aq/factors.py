"""因子库：从「经济假设」到「可计算表达式」。

组织方式
--------
每个因子是一个 `Factor` 数据类，登记 6 件事：

    name      唯一名（小写下划线）
    category  家族（反转/动量/波动/流动性/量价/价值/质量/成长/规模/风险）
    formula   人能读懂的公式，与代码一一对应
    direction +1 表示数值越大预期收益越高，-1 表示越小越好
    window    最长回看交易日，用于构造 PIT 样本与 purge 区间
    func      接收 Wide 面板，返回同形状的因子矩阵

所有计算都在 **宽表**（index=交易日，columns=股票代码）上完成：
- 时序算子（rolling / shift）走 pandas/NumPy 的列向量化，比 groupby 快一个量级；
- 截面算子（rank / zscore / 中性化）沿 axis=1 一次完成，天然对齐同一交易日。

单位约定：金额单位为元，收益率与换手率为小数，市值单位为元。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

# ============================================================================
# 宽表面板
# ============================================================================


class Wide:
    """把长表面板惰性旋转成宽表，按列缓存，避免重复 pivot。"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._cache: dict[str, pd.DataFrame] = {}
        self.dates = pd.Index(sorted(pd.unique(df["date"])))
        self.codes = pd.Index(sorted(pd.unique(df["code"])))

    def __call__(self, col: str) -> pd.DataFrame:
        if col not in self._cache:
            w = self.df.pivot(index="date", columns="code", values=col)
            w = w.reindex(index=self.dates, columns=self.codes)
            # float32：宽表是 800 日 x 4500 股 = 360 万格，用 float64 会有 30MB/列，
            # 40 多个因子同时驻留就会打爆内存；float32 精度对因子排序完全够用。
            self._cache[col] = w.astype("float32")
        return self._cache[col]

    @property
    def ret(self) -> pd.DataFrame:
        if "_ret" not in self._cache:
            c = self("adj_close")
            self._cache["_ret"] = c / c.shift(1) - 1
        return self._cache["_ret"]

    def market_ret(self) -> pd.Series:
        """等权市场收益，作为 beta 与特质波动的基准。"""
        return self.ret.mean(axis=1)


def safe_div(a: pd.DataFrame, b: pd.DataFrame, eps: float = 1e-12) -> pd.DataFrame:
    return a / b.where(b.abs() > eps)


def _roll(f: pd.DataFrame, w: int, how: str = "mean", min_ratio: float = 0.6) -> pd.DataFrame:
    mp = max(2, int(w * min_ratio))
    return getattr(f.rolling(w, min_periods=mp), how)()


def rolling_corr(x: pd.DataFrame, y: pd.DataFrame, w: int) -> pd.DataFrame:
    mp = max(3, int(w * 0.6))
    mx = x.rolling(w, min_periods=mp).mean()
    my = y.rolling(w, min_periods=mp).mean()
    cov = (x * y).rolling(w, min_periods=mp).mean() - mx * my
    vx = (x * x).rolling(w, min_periods=mp).mean() - mx * mx
    vy = (y * y).rolling(w, min_periods=mp).mean() - my * my
    return cov / np.sqrt(vx.clip(lower=1e-24) * vy.clip(lower=1e-24))


def rolling_cov_with_series(x: pd.DataFrame, s: pd.Series, w: int) -> pd.DataFrame:
    mp = max(3, int(w * 0.6))
    mx = x.rolling(w, min_periods=mp).mean()
    ms = s.rolling(w, min_periods=mp).mean()
    xs = x.mul(s, axis=0)
    return xs.rolling(w, min_periods=mp).mean() - mx.mul(ms, axis=0)


def rolling_beta(r: pd.DataFrame, m: pd.Series, w: int = 120) -> pd.DataFrame:
    cov = rolling_cov_with_series(r, m, w)
    var = m.rolling(w, min_periods=max(3, int(w * 0.6))).var()
    return cov.div(var, axis=0)


# ============================================================================
# 因子定义
# ============================================================================


@dataclass
class Factor:
    name: str
    category: str
    formula: str
    direction: int
    window: int
    func: Callable[[Wide], pd.DataFrame]
    desc: str = ""
    tags: list[str] = field(default_factory=list)


FACTORS: dict[str, Factor] = {}


def factor(name: str, category: str, formula: str, direction: int, window: int,
           desc: str = "") -> Callable:
    def deco(fn: Callable[[Wide], pd.DataFrame]):
        FACTORS[name] = Factor(name, category, formula, direction, window, fn, desc)
        return fn
    return deco


# ---------------------------------------------------------------- 反转 / 动量
@factor("rev_1", "反转", "-(C_t / C_{t-1} - 1)", +1, 2,
        "一日反转：隔日过度反应的直接体现")
def _rev_1(w: Wide):
    return -w.ret


@factor("rev_5", "反转", "-(C_t / C_{t-5} - 1)", +1, 7,
        "周度反转：A 股最强的短周期效应之一")
def _rev_5(w: Wide):
    c = w("adj_close")
    return -(c / c.shift(5) - 1)


@factor("rev_10", "反转", "-(C_t / C_{t-10} - 1)", +1, 12)
def _rev_10(w: Wide):
    c = w("adj_close")
    return -(c / c.shift(10) - 1)


@factor("mom_20", "动量", "C_t / C_{t-20} - 1", +1, 22)
def _mom_20(w: Wide):
    c = w("adj_close")
    return c / c.shift(20) - 1


@factor("mom_60", "动量", "C_t / C_{t-60} - 1", +1, 62)
def _mom_60(w: Wide):
    c = w("adj_close")
    return c / c.shift(60) - 1


@factor("mom_120", "动量", "C_t / C_{t-120} - 1", +1, 122)
def _mom_120(w: Wide):
    c = w("adj_close")
    return c / c.shift(120) - 1


@factor("mom_12_1", "动量", "C_{t-20} / C_{t-240} - 1", +1, 242,
        "跳过最近一个月的年度动量，规避短期反转污染")
def _mom_12_1(w: Wide):
    c = w("adj_close")
    return c.shift(20) / c.shift(240) - 1


@factor("beta_60", "风险", "-Beta(r, r_mkt; 120d)", +1, 122,
        "低 beta 异象：高 beta 股票的风险调整后收益更差")
def _beta_60(w: Wide):
    return -rolling_beta(w.ret, w.market_ret(), 120)


@factor("resid_mom_60", "动量", "mom_60 - beta * mkt_mom_60", +1, 130,
        "残差动量：剥离市场 beta 后的个股动量，比裸动量稳定")
def _resid_mom_60(w: Wide):
    c = w("adj_close")
    mom = c / c.shift(60) - 1
    beta = rolling_beta(w.ret, w.market_ret(), 120)
    m = w.market_ret()
    mkt_mom = (1 + m).rolling(60, min_periods=36).apply(np.prod, raw=True) - 1
    return mom - beta.mul(mkt_mom, axis=0)


# ---------------------------------------------------------------- 波动
@factor("vol_20", "波动", "-Std(r, 20)", +1, 22, "低波动异象")
def _vol_20(w: Wide):
    return -w.ret.rolling(20, min_periods=12).std()


@factor("vol_60", "波动", "-Std(r, 60)", +1, 62)
def _vol_60(w: Wide):
    return -w.ret.rolling(60, min_periods=36).std()


@factor("ivol_60", "波动", "-Std(r - beta*r_mkt, 60)", +1, 125,
        "特质波动率：剥离市场后的残差波动，比总波动更干净")
def _ivol_60(w: Wide):
    r = w.ret
    m = w.market_ret()
    beta = rolling_beta(r, m, 120)
    resid = r - beta.mul(m, axis=0)
    return -resid.rolling(60, min_periods=36).std()


@factor("skew_20", "波动", "-Skew(r, 20)", +1, 22,
        "负偏度厌恶：正偏（彩票型）股票系统性被高估")
def _skew_20(w: Wide):
    return -w.ret.rolling(20, min_periods=12).skew()


@factor("kurt_20", "波动", "-Kurt(r, 20)", +1, 22)
def _kurt_20(w: Wide):
    return -w.ret.rolling(20, min_periods=12).kurt()


@factor("max_ret_20", "波动", "-Max(r, 20)", +1, 22,
        "最大单日收益：彩票偏好的最直接代理变量")
def _max_ret_20(w: Wide):
    return -w.ret.rolling(20, min_periods=12).max()


@factor("amp_20", "波动", "-Mean((H-L)/C, 20)", +1, 22)
def _amp_20(w: Wide):
    h, l, c = w("adj_high"), w("adj_low"), w("adj_close")
    return -((h - l) / c.where(c > 0)).rolling(20, min_periods=12).mean()


@factor("range_60", "波动", "-(Max(H,60) - Min(L,60)) / C", +1, 62)
def _range_60(w: Wide):
    h, l, c = w("adj_high"), w("adj_low"), w("adj_close")
    hh = h.rolling(60, min_periods=36).max()
    ll = l.rolling(60, min_periods=36).min()
    return -(hh - ll) / c.where(c > 0)


# ---------------------------------------------------------------- 流动性
@factor("turn_20", "流动性", "-Mean(Turnover, 20)", +1, 22,
        "换手率：高换手 = 高投机 / 高拥挤")
def _turn_20(w: Wide):
    return -w("turnover").rolling(20, min_periods=12).mean()


@factor("turn_std_20", "流动性", "-Std(Turnover, 20)", +1, 22)
def _turn_std_20(w: Wide):
    return -w("turnover").rolling(20, min_periods=12).std()


@factor("turn_chg", "流动性", "-[Mean(Turn,5)/Mean(Turn,60) - 1]", +1, 62,
        "换手骤升：短期关注度放大，通常预示反转")
def _turn_chg(w: Wide):
    t = w("turnover")
    return -(_roll(t, 5, "mean", 0.8) / _roll(t, 60, "mean") - 1)


@factor("amihud_20", "流动性", "Mean(|r| / Amount, 20) x 1e8", +1, 22,
        "Amihud 非流动性：单位成交额引起的价格冲击")
def _amihud_20(w: Wide):
    amt = w("amount")
    x = w.ret.abs() / amt.where(amt > 0) * 1e8
    return x.rolling(20, min_periods=12).mean()


@factor("ln_amount_20", "流动性", "-ln(Mean(Amount,20))", +1, 22,
        "成交额规模：小成交额股票的流动性溢价")
def _ln_amount_20(w: Wide):
    a = w("amount").rolling(20, min_periods=12).mean()
    return -np.log(a.where(a > 0))


@factor("vol_ratio", "流动性", "-[Mean(V,5)/Mean(V,60) - 1]", +1, 62,
        "成交量放大：与换手骤升同源")
def _vol_ratio(w: Wide):
    v = w("volume")
    return -(_roll(v, 5, "mean", 0.8) / _roll(v, 60, "mean") - 1)


# ---------------------------------------------------------------- 量价
@factor("pv_corr_20", "量价", "-Corr(r, dV/V, 20)", +1, 22,
        "量价背离：放量上涨的持续性更差")
def _pv_corr_20(w: Wide):
    v = w("volume")
    dv = v / v.shift(1) - 1
    return -rolling_corr(w.ret, dv, 20)


@factor("gap_20", "量价", "-Mean(O_t / C_{t-1} - 1, 20)", +1, 22,
        "隔夜跳空：开盘过度反应后回补")
def _gap_20(w: Wide):
    o, pc = w("adj_open"), w("adj_pre_close")
    return -(o / pc.where(pc > 0) - 1).rolling(20, min_periods=12).mean()


@factor("hl_20", "量价", "-Mean(H/L - 1, 20)", +1, 22)
def _hl_20(w: Wide):
    h, l = w("adj_high"), w("adj_low")
    return -(h / l.where(l > 0) - 1).rolling(20, min_periods=12).mean()


# ---------------------------------------------------------------- 价值
@factor("bp", "价值", "BPS / C", +1, 1, "账面市值比：每股净资产 / 收盘价")
def _bp(w: Wide):
    return safe_div(w("bps"), w("close"))


@factor("ep_ttm", "价值", "EPS_TTM / C", +1, 1, "盈利收益率")
def _ep_ttm(w: Wide):
    return safe_div(w("eps_ttm"), w("close"))


@factor("sp_ttm", "价值", "Revenue_TTM / MktCap", +1, 1, "市销率倒数")
def _sp_ttm(w: Wide):
    return safe_div(w("revenue_ttm"), w("mktcap"))


@factor("cfp", "价值", "CFO_PS_TTM / C", +1, 1, "现金流价格比")
def _cfp(w: Wide):
    return safe_div(w("ocf_ps_ttm"), w("close"))


@factor("div_yield", "价值", "股息率(%)", +1, 1)
def _div_yield(w: Wide):
    return w("div_yield")


# ---------------------------------------------------------------- 质量
@factor("roe", "质量", "加权 ROE(%)", +1, 1)
def _roe(w: Wide):
    return w("roe")


@factor("gross_margin", "质量", "销售毛利率(%)", +1, 1)
def _gross_margin(w: Wide):
    return w("gross_margin")


@factor("ocf_to_eps", "质量", "CFO_PS_TTM / |EPS_TTM|", +1, 1,
        "利润的现金含量：越高说明利润越扎实")
def _ocf_to_eps(w: Wide):
    eps = w("eps_ttm")
    return safe_div(w("ocf_ps_ttm"), eps.abs().where(eps.abs() > 1e-6))


@factor("accrual", "质量", "-(EPS_TTM - CFO_PS_TTM)/|EPS_TTM|", +1, 1,
        "应计项：会计利润里尚未变现的部分，越高越差")
def _accrual(w: Wide):
    eps = w("eps_ttm")
    a = eps.abs().where(eps.abs() > 1e-6)
    return -(eps - w("ocf_ps_ttm")) / a


# ---------------------------------------------------------------- 成长
@factor("rev_yoy", "成长", "营业总收入同比(%)", +1, 1)
def _rev_yoy(w: Wide):
    return w("rev_yoy")


@factor("np_yoy", "成长", "归母净利润同比(%)", +1, 1)
def _np_yoy(w: Wide):
    return w("np_yoy")


@factor("rev_accel", "成长", "本期营收同比 - 60 交易日前营收同比", +1, 62,
        "成长加速度：二阶变化比一阶更接近预期差")
def _rev_accel(w: Wide):
    y = w("rev_yoy")
    return y - y.shift(60)


# ---------------------------------------------------------------- 规模
@factor("size", "规模", "-ln(流通市值)", +1, 1,
        "规模因子：仅在最微小的 30% 市值里有效；剔除该段后 IC 翻负（见讲义附录 H），"
        "判定为不可用，保留代码仅供复现")
def _size(w: Wide):
    return -w("ln_mktcap")


# ============================================================================
# 计算入口
# ============================================================================
PRICE_COLS = ["adj_open", "adj_high", "adj_low", "adj_close", "adj_pre_close"]
BASE_COLS = PRICE_COLS + [
    "date", "code", "open", "close", "pre_close", "high", "low",
    "volume", "amount", "turnover", "pct_chg", "is_st", "trade_status",
    "is_tradable", "can_buy_next", "can_sell_next", "limit_up", "limit_down",
    "ln_mktcap", "mktcap", "listed_days",
    "eps_ttm", "bps", "roe", "revenue_ttm", "ocf_ps_ttm", "net_profit_ttm",
    "gross_margin", "div_yield", "rev_yoy", "np_yoy",
    "fwd_ret_1", "fwd_ret_5", "fwd_ret_10", "fwd_ret_20",
    "next_open", "next_ret",
]


def _stack(df: pd.DataFrame) -> pd.Series:
    try:
        return df.stack(future_stack=True)
    except TypeError:
        return df.stack()


def compute_all(df: pd.DataFrame, names: list[str] | None = None,
                valid_only: bool = False) -> pd.DataFrame:
    """计算因子，返回长表 [date, code, factor...]。

    valid_only=True 时把「当日不可交易」的样本置为 NaN，
    保证因子评价不被 ST / 停牌 / 新股污染。
    """
    w = Wide(df)
    use = names or list(FACTORS)
    mats: dict[str, pd.DataFrame] = {}
    for n in use:
        try:
            mats[n] = FACTORS[n].func(w)
        except Exception as e:  # noqa: BLE001
            print(f"  [factor] {n} FAILED: {type(e).__name__}: {e}")
    if not mats:
        return pd.DataFrame(columns=["date", "code"])
    long = pd.DataFrame({k: _stack(v) for k, v in mats.items()})
    long.index.names = ["date", "code"]
    long = long.reset_index()
    long = long.replace([np.inf, -np.inf], np.nan)

    if valid_only:
        valid = df.loc[df["is_tradable"], ["date", "code"]]
        long = long.merge(valid, on=["date", "code"], how="inner")
    return long


def factor_table() -> pd.DataFrame:
    rows = [{
        "因子": f.name, "家族": f.category,
        "方向": "越大越好" if f.direction > 0 else "越小越好",
        "最长回看(交易日)": f.window, "公式": f.formula, "说明": f.desc,
    } for f in FACTORS.values()]
    return pd.DataFrame(rows)
