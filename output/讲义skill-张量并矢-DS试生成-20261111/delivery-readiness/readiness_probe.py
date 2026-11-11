"""Read-only readiness probe for the WeChat push chain.

Reuses the sender's own functions (binding / gateway_open / validate /
window_age_hours) so the result comes from its code, not a hand-rolled guess.
Never prints the owner id or account id; only masked facts.
"""
import json
import sys
import time
from pathlib import Path

PROJECT = Path(r"D:\aaa_D_usual\DSH\社交信息整理助手")
SAMPLE = Path(r"D:\aaa_D_usual\DSH\111学习助手\output\讲义skill-张量并矢-DS试生成-20261111\inputs\old-handout.pdf")

sys.path.insert(0, str(PROJECT / "scripts"))
import wechat_send_file as sender  # noqa: E402
import wechat_push as push  # noqa: E402  (argparse only runs under __main__)

out = {"checked_at": time.strftime("%Y-%m-%d %H:%M:%S"), "sender_project": "<social-assistant-project>"}

# gateway
try:
    out["gateway"] = {"port": sender.GATEWAY_PORT, "open": sender.gateway_open()}
except Exception as exc:  # noqa: BLE001
    out["gateway"] = {"port": sender.GATEWAY_PORT, "open": None, "error": type(exc).__name__}

# binding (authoritative check from the tool itself, masked output)
binding_info = {"ok": False}
try:
    account, owner = sender.binding()
    binding_info = {
        "ok": True,
        "bound_owner_count": 1,
        "account_id": "<redacted>",
        "owner_masked": "***" + owner[-10:] if len(owner) > 10 else "***",
        "owner_domain_ok": owner.endswith("@im.wechat"),
    }
except SystemExit as exc:
    binding_info["error"] = str(exc)
except Exception as exc:  # noqa: BLE001
    binding_info["error"] = f"{type(exc).__name__}: {exc}"
out["binding"] = binding_info

# file capability on the requested sample
sample = {}
try:
    raw = SAMPLE.read_bytes()
    sample = {
        "path": "inputs/old-handout.pdf",
        "exists": True,
        "bytes": len(raw),
        "mib": round(len(raw) / 1024 / 1024, 3),
        "magic": raw[:5].decode("latin-1"),
        "is_pdf": raw[:5] == b"%PDF-",
        "nonempty": len(raw) > 0,
        "under_channel_limit_25mib": len(raw) <= sender.MAX_BYTES,
    }
    try:
        validated = push.validate(str(SAMPLE))
        sample["tool_validate_passed"] = str(validated).endswith("old-handout.pdf")
    except SystemExit as exc:
        sample["tool_validate_passed"] = False
        sample["tool_validate_error"] = str(exc)
except OSError as exc:
    sample = {"exists": False, "error": type(exc).__name__}
out["sample_file"] = sample

# reply-window age (uses context-tokens mtime of the bound account)
try:
    out["window_age_hours"] = round(sender.window_age_hours(), 2)
except Exception as exc:  # noqa: BLE001
    out["window_age_hours"] = f"unavailable:{type(exc).__name__}"
out["window_warn_threshold_hours"] = sender.WINDOW_WARN_HOURS

# retry queue state
pending = PROJECT / "data" / "openclaw" / "file-queue" / "pending"
sent = PROJECT / "data" / "openclaw" / "file-queue" / "sent"
def stats(folder):
    if not folder.is_dir():
        return {"exists": False, "count": 0}
    files = sorted(folder.glob("*.json"))
    kinds = {}
    for f in files:
        try:
            kind = json.loads(f.read_text("utf-8")).get("kind", "?")
        except Exception:  # noqa: BLE001
            kind = "unreadable"
        kinds[kind] = kinds.get(kind, 0) + 1
    return {"exists": True, "count": len(files), "kinds": kinds,
            "newest": files[-1].name[:15] if files else None}
out["queue_pending"] = stats(pending)
out["queue_sent"] = stats(sent)
out["channel_limits"] = {"max_bytes": sender.MAX_BYTES, "outbox_keep_days": sender.OUTBOX_KEEP_DAYS}

print(json.dumps(out, ensure_ascii=False, indent=2))
