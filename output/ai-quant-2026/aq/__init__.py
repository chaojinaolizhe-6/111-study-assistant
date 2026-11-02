"""A 股 AI 量化研究工作区。

模块
----
config      路径、时间范围、股票池口径
http        双通道 HTTP（直连 / 系统代理）
sources     数据源适配（东财数据中心、东财行情、baostock）
db          SQLite 读写封装
schema      SQLite 表结构
panel       研究面板（复权价、PIT 财务、标签、可交易标记）
universe    股票池与可交易过滤
factors     因子库（注册表 + 分组实现）
neutralize  去极值、标准化、行业市值中性化
metrics     因子评价（IC / ICIR / 分层 / 换手 / 衰减）
cv          Purged K-Fold / CPCV / Walk-forward
stats       Deflated Sharpe / PBO / Bootstrap
"""
__version__ = "1.0.0"
