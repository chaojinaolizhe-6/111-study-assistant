"""数据源：东方财富（数据中心 + 历史行情）。

选择理由（2026-10 实测）
  * push2his（历史 K 线）直连可用，支持 fqt=0/1/2 三种复权口径；
  * push2（实时快照）在本机被网络拦截，因此股票列表改由 datacenter 的
    「业绩报表」接口获得 —— 它本身带公告日，天然是 point-in-time 的；
  * datacenter-web 直连可用，单页 500 条，分页稳定。
"""
from __future__ import annotations

import math
from typing import Any

from .http import FetchError, get_json

DATACENTER = "https://datacenter-web.eastmoney.com/api/data/v1/get"
KLINE = "https://push2his.eastmoney.com/api/qt/stock/kline/get"

# 财务字段映射：东财列名 -> 本地列名
FIN_COLUMNS = {
    "SECURITY_CODE": "code",
    "REPORTDATE": "report_date",
    "NOTICE_DATE": "notice_date",
    "BASIC_EPS": "eps",
    "BPS": "bps",
    "WEIGHTAVG_ROE": "roe",
    "TOTAL_OPERATE_INCOME": "revenue",
    "PARENT_NETPROFIT": "net_profit",
    "MGJYXJJE": "ocf_ps",
    "XSMLL": "gross_margin",
    "ZXGXL": "div_yield",
    "YSTZ": "rev_yoy",
    "SJLTZ": "np_yoy",
    "DATATYPE": "data_type",
    "SECURITY_NAME_ABBR": "name",
    "BOARD_NAME": "board",
    "BOARD_CODE": "board_code",
    "SECURITY_TYPE": "sec_type",
    "TRADE_MARKET": "market",
    "EITIME": "eitime",
}


def _num(x: Any) -> float | None:
    if x is None or x == "" or x == "-":
        return None
    try:
        v = float(x)
        return None if math.isnan(v) or math.isinf(v) else v
    except (TypeError, ValueError):
        return None


def fin_period(report_date: str, page_size: int = 500) -> list[dict[str, Any]]:
    """取某一财报期的全部记录（含已退市公司的历史记录）。"""
    out: list[dict[str, Any]] = []
    page = 1
    pages = 1
    while page <= pages:
        params = {
            "reportName": "RPT_LICO_FN_CPD",
            "columns": "ALL",
            "pageNumber": page,
            "pageSize": page_size,
            "sortColumns": "SECURITY_CODE",
            "sortTypes": 1,
            "filter": f"(REPORTDATE='{report_date}')",
            "source": "WEB",
            "client": "WEB",
        }
        j = get_json(DATACENTER, params, timeout=25)
        res = j.get("result") or {}
        pages = int(res.get("pages") or 0)
        data = res.get("data") or []
        if not data:
            break
        for r in data:
            if r.get("SECURITY_TYPE") != "A股":
                continue
            rec = {v: r.get(k) for k, v in FIN_COLUMNS.items()}
            rec["report_date"] = (rec["report_date"] or "")[:10]
            rec["notice_date"] = (rec["notice_date"] or "")[:10] or None
            for k in ("eps", "bps", "roe", "revenue", "net_profit", "ocf_ps",
                      "gross_margin", "div_yield", "rev_yoy", "np_yoy"):
                rec[k] = _num(rec[k])
            out.append(rec)
        page += 1
    return out


def kline(secid: str, fqt: int = 0, beg: str = "19900101",
          end: str = "20501231") -> list[list[str]]:
    """取日线。fqt: 0=不复权, 1=前复权, 2=后复权。

    返回每行: [date, open, close, high, low, volume, amount, amplitude, pct_chg, chg, turnover]
    """
    params = {
        "secid": secid,
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": 101,
        "fqt": fqt,
        "beg": beg.replace("-", ""),
        "end": end.replace("-", ""),
    }
    j = get_json(KLINE, params, timeout=20)
    data = j.get("data") or {}
    return data.get("klines") or []


def index_kline(secid: str, beg: str = "19900101", end: str = "20501231") -> list[list[str]]:
    params = {
        "secid": secid,
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",
        "klt": 101,
        "fqt": 0,
        "beg": beg.replace("-", ""),
        "end": end.replace("-", ""),
    }
    j = get_json(KLINE, params, timeout=20)
    data = j.get("data") or {}
    return data.get("klines") or []


def to_secid(code: str) -> str | None:
    """A 股代码 -> 东财 secid。"""
    c = code.strip()
    if len(c) != 6 or not c.isdigit():
        return None
    if c[0] in "69":            # 6xxxxx 沪市 / 9xxxxx B 股（沪）
        return f"1.{c}"
    if c[0] in "03":            # 0/3 开头深市
        return f"0.{c}"
    if c[0] in "48" or c[:2] in ("92",):
        return f"0.{c}"         # 北交所（东财归在 0 市场）
    return None


__all__ = ["fin_period", "kline", "index_kline", "to_secid", "FetchError"]
