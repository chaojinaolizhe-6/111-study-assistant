#!/usr/bin/env python3
"""学习时区（中国大陆 UTC+8）——**所有"今天/截止/排期"判定的唯一入口**。

规则来源：`.tutor/config/time-environment.yml`（2026-09-27 学习者确认）。
- 客户端/系统时钟是**英国时间**（`clientTimeZone: Europe/London`），学习者在**中国大陆**；
- 差值随夏令时变化（BST 期间 +7h，GMT 期间 +8h）→ **不写死差值**，一律用 IANA 时区换算；
- 排期、`plan/today-<日期>.md`、截止日一律用**中国日期**。

为什么做成模块：此前每个工具各自 `dt.date.today()`（= 英国日期），
英国 17:00 之后中国已进入次日 → 会把"明天"排成"今天"，也让"当天未完成事项结转"算错一天。

用法:
  from timebase import learning_today, learning_now
  today = learning_today()            # 'YYYY-MM-DD'（中国日期）
  today = learning_today("2026-09-30")  # 显式覆盖（参数优先）
"""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

LEARNING_TZ = ZoneInfo("Asia/Shanghai")   # 中国大陆（UTC+8）；Windows 上 zoneinfo 若无 tzdata 会回退
FALLBACK_OFFSET = dt.timedelta(hours=8)   # 仅在 zoneinfo 库不可用时使用


def learning_now() -> dt.datetime:
    """当前中国时间（tz-aware）。"""
    return dt.datetime.now(LEARNING_TZ)


def learning_today(override: str | None = None) -> str:
    """中国日期 'YYYY-MM-DD'；`override` 非空时原样返回（调用方显式指定优先）。"""
    if override:
        return override
    return learning_now().date().isoformat()


def uk_date_now() -> str:
    """系统（英国）日期——**只用于诊断**，不要用于排期。"""
    return dt.datetime.now(ZoneInfo("Europe/London")).date().isoformat()


def add_days(date_text: str, days: int) -> str:
    return (dt.date.fromisoformat(date_text) + dt.timedelta(days=days)).isoformat()


def days_between(a: str, b: str) -> int:
    """b − a（天）；任一侧不合法时返回 0。"""
    try:
        return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days
    except ValueError:
        return 0


def main() -> int:
    import sys

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"学习时区: {LEARNING_TZ}（中国大陆 UTC+8）")
    print(f"中国时间: {learning_now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"英国时间: {dt.datetime.now(ZoneInfo('Europe/London')).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"学习日(今天): {learning_today()}")
    if learning_today() != uk_date_now():
        print(f"⚠ 与系统（英国）日期不同：英国 {uk_date_now()} ≠ 中国 {learning_today()} —— 排期必须用中国日期")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
