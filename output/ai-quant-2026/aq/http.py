"""双通道 HTTP：直连优先，失败自动回落到系统代理。

背景：本机存在系统级代理（127.0.0.1:2xxxx），但代理对部分域名不稳定；
而 push2his / datacenter 直连可用。因此对每个请求做「直连 <-> 代理」交替重试，
既不会把网络抖动当成限流，也不会在代理挂掉时整体失败。
"""
from __future__ import annotations

import json
import random
import threading
import time
from typing import Any

import requests

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

_TLS = threading.local()


def system_proxy() -> str | None:
    """读取 Windows 注册表中的系统代理（requests 的 trust_env 之外再兜一层）。"""
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if not enable:
            return None
        server, _ = winreg.QueryValueEx(key, "ProxyServer")
        if not server:
            return None
        if "=" in server:  # 形如 http=...;https=...
            parts = dict(p.split("=", 1) for p in server.split(";") if "=" in p)
            server = parts.get("https") or parts.get("http") or server
        if not server.startswith("http"):
            server = "http://" + server
        return server
    except Exception:
        return None


def _session(direct: bool) -> requests.Session:
    """每个线程各自持有一个 session，避免连接池串扰。"""
    cache: dict[bool, requests.Session] = getattr(_TLS, "sessions", {})
    if direct in cache:
        return cache[direct]
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": UA,
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
    )
    if direct:
        s.trust_env = False
        s.proxies = {"http": None, "https": None}
    else:
        px = system_proxy()
        if px:
            s.proxies = {"http": px, "https": px}
        s.trust_env = False
    cache[direct] = s
    _TLS.sessions = cache
    return s


class FetchError(RuntimeError):
    pass


def get_json(url: str, params: dict[str, Any] | None = None, *, tries: int = 6,
             timeout: float = 15.0) -> Any:
    """GET 返回 JSON。直连与代理交替重试，指数退避。"""
    last: Exception | None = None
    for i in range(tries):
        direct = (i % 2 == 0)
        try:
            r = _session(direct).get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                txt = r.text.strip()
                if txt[:1] in "{[":
                    return json.loads(txt)
                raise FetchError(f"non-json payload: {txt[:120]}")
            last = FetchError(f"HTTP {r.status_code}")
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(min(0.4 * (2 ** i), 6.0) * (0.6 + random.random() * 0.8))
    raise FetchError(f"{url} failed after {tries} tries: {last}")


def get_text(url: str, params: dict[str, Any] | None = None, *, tries: int = 5,
             timeout: float = 20.0, headers: dict[str, str] | None = None) -> str:
    last: Exception | None = None
    for i in range(tries):
        direct = (i % 2 == 0)
        try:
            r = _session(direct).get(url, params=params, timeout=timeout, headers=headers)
            if r.status_code == 200:
                return r.text
            last = FetchError(f"HTTP {r.status_code}")
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(min(0.4 * (2 ** i), 6.0) * (0.6 + random.random() * 0.8))
    raise FetchError(f"{url} failed after {tries} tries: {last}")
