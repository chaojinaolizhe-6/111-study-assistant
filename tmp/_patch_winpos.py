# -*- coding: utf-8 -*-
import io, json
p = r"D:\aaa_D_usual\CODEX\gemini-knowledge-bridge\src\settings.mjs"
s = io.open(p, encoding="utf-8").read()
old = "...(headless ? [] : ['--window-position=-32000,-32000', '--window-size=1280,900'])"
new = "...(headless ? [] : [`--window-position=${config.managedWindowPosition || '80,40'}`, `--window-size=${config.managedWindowSize || '1440,960'}`])"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

sp = r"D:\aaa_D_usual\CODEX\gemini-knowledge-bridge\data\settings.local.json"
cfg = json.loads(io.open(sp, encoding="utf-8-sig").read())
cfg["managedWindowPosition"] = "80,40"
cfg["managedWindowSize"] = "1440,960"
io.open(sp, "w", encoding="utf-8").write(json.dumps(cfg, ensure_ascii=False, indent=4))
print("settings patched")
print(json.dumps(cfg, ensure_ascii=False, indent=2))
