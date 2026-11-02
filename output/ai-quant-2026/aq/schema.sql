-- ============================================================
-- A 股 AI 量化研究数据库（SQLite）
-- 设计原则
--   1) 只存"原始事实"，派生量（收益、因子）一律不进库，避免口径漂移；
--   2) 所有价格同时保留不复权价与复权因子，任何时刻可还原后复权价；
--   3) 财务数据必须带公告日 notice_date，这是 point-in-time 的唯一入口；
--   4) 每张表都有主键，写入用 upsert，可反复增量更新而不产生重复。
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = -200000;

-- 证券主表 -----------------------------------------------------
CREATE TABLE IF NOT EXISTS stock (
    code        TEXT PRIMARY KEY,          -- 6 位代码，如 600000
    secid       TEXT NOT NULL,             -- 东财行情 secid，如 1.600000
    exchange    TEXT NOT NULL,             -- SH / SZ / BJ
    name        TEXT,                      -- 最新证券简称
    board       TEXT,                      -- 东财行业板块名
    board_code  TEXT,
    list_date   TEXT,                      -- 上市日（由首个交易日推断）
    delist_date TEXT,                      -- 退市日（由最后交易日推断，仍在市为 NULL）
    is_active   INTEGER DEFAULT 1,
    updated_at  TEXT
);

-- 交易日历 -----------------------------------------------------
CREATE TABLE IF NOT EXISTS trade_calendar (
    date TEXT PRIMARY KEY,                 -- YYYY-MM-DD
    is_open INTEGER NOT NULL
);

-- 日线行情 -----------------------------------------------------
-- open/high/low/close/pre_close 均为【不复权】原始价；
-- adj_factor 为累计复权因子：后复权价 = 原始价 * adj_factor。
CREATE TABLE IF NOT EXISTS bar (
    code      TEXT NOT NULL,
    date      TEXT NOT NULL,
    open      REAL, high REAL, low REAL, close REAL,
    pre_close REAL,
    volume    REAL,                        -- 股
    amount    REAL,                        -- 元
    turnover  REAL,                        -- 换手率 %
    pct_chg   REAL,                        -- 涨跌幅 %
    adj_factor REAL,
    is_st     INTEGER,                     -- 当日是否 ST，1/0，来自交易状态字段
    trade_status INTEGER,                  -- 1=正常交易, 0=停牌
    PRIMARY KEY (code, date)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_bar_date ON bar(date);

-- 指数行情 -----------------------------------------------------
CREATE TABLE IF NOT EXISTS index_bar (
    code TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL, high REAL, low REAL, close REAL,
    volume REAL, amount REAL, pct_chg REAL,
    PRIMARY KEY (code, date)
) WITHOUT ROWID;

-- 财务报表（point-in-time）-------------------------------------
CREATE TABLE IF NOT EXISTS fin (
    code        TEXT NOT NULL,
    report_date TEXT NOT NULL,             -- 报告期，如 2025-06-30
    notice_date TEXT,                      -- 公告日，PIT 关键字段
    eps         REAL,                      -- 基本每股收益
    bps         REAL,                      -- 每股净资产
    roe         REAL,                      -- 加权平均 ROE %
    revenue     REAL,                      -- 营业总收入
    net_profit  REAL,                      -- 归母净利润
    ocf_ps      REAL,                      -- 每股经营现金流
    gross_margin REAL,                     -- 销售毛利率 %
    div_yield   REAL,                      -- 股息率 %
    rev_yoy     REAL,                      -- 营收同比 %
    np_yoy      REAL,                      -- 净利同比 %
    data_type   TEXT,                      -- 一季报/中报/三季报/年报
    name        TEXT,                      -- 该期披露时的证券简称（用于还原 ST 历史）
    PRIMARY KEY (code, report_date)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_fin_notice ON fin(notice_date);

-- 指数成分股（时点快照）---------------------------------------
CREATE TABLE IF NOT EXISTS index_member (
    index_code TEXT NOT NULL,
    code       TEXT NOT NULL,
    in_date    TEXT NOT NULL,
    out_date   TEXT,
    PRIMARY KEY (index_code, code, in_date)
) WITHOUT ROWID;

-- 抓取日志（断点续抓）-----------------------------------------
CREATE TABLE IF NOT EXISTS fetch_log (
    task TEXT NOT NULL,
    key  TEXT NOT NULL,
    status TEXT,                           -- ok / empty / err
    n_rows INTEGER,
    ts TEXT,
    err TEXT,
    PRIMARY KEY (task, key)
) WITHOUT ROWID;

-- 元数据 -------------------------------------------------------
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
