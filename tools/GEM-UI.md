# Gemini 专用浏览器的系统级操作工具（gem_ui.ps1）

目的：不依赖 Gemini 连接器（`D:\aaa_D_usual\CODEX\gemini-knowledge-bridge`）的内部接口，
直接从操作系统层面截屏 + 点击 + 打字，操作那个专用 Chrome 窗口。
连接器只给了我「问一句」的能力，这个工具补上「点任何东西」。

## 前提

- 专用 Chrome 进程存在，窗口标题含 `Google Gemini`。
- 窗口必须**可见**。其启动参数原本是 `--window-position=-32000,-32000`（屏幕外，所以一直看不见），
  2026-11-12 已改成 `80,40`（见 `data/browser.managed.json`），下次重启浏览器就会出现在屏幕上。
- 屏幕为 2560×1600、缩放 150%；脚本以 `SetProcessDPIAware` 运行，坐标一律是**物理像素**。

## 用法

```powershell
$S = 'D:\aaa_D_usual\DSH\111学习助手\tools\gem_ui.ps1'
$ps = (Get-Command powershell.exe).Source

& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action rect    -TitleMatch 'Google Gemini'
& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action shot    -Out  'D:\...\tmp\shots\a.png' -TitleMatch 'Google Gemini'
& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action click   -X 1584 -Y 1354 -TitleMatch 'Google Gemini'
& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action dclick  -X 1200 -Y 12   -TitleMatch 'Google Gemini'   # 双击标题栏=最大化
& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action wheel   -X 900  -Y 700 -Wheel -480 -TitleMatch 'Google Gemini'
& $ps -NoProfile -ExecutionPolicy Bypass -File $S -Action place   -X 0 -Y 0 -TitleMatch 'Google Gemini'
```

`shot` 保存的是**整窗截图**，图片像素坐标 = 窗口相对坐标，直接喂给 `click -X -Y` 即可
（脚本内部会加上窗口左上角偏移）。

## 已验证的操作（2026-11-12）

1. 打开模型菜单（点输入框右上「Argon … ∨」）；
2. 点「思考等级 ▸」展开子菜单；
3. 点「中」→ 输入框按钮变成 `Argon 中`（截图 `tmp/shots/s6.png`）；
4. 再点「高」→ 变回 `Argon 高`（截图 `tmp/shots/final2.png`）。

## 坑

- `ShowWindow(SW_RESTORE=9)` 会把已最大化的窗口还原——本脚本只在窗口最小化时才用 9，
  否则用 5（SW_SHOW）。早期版本因此出现过「刚最大化、一截图又变回去」。
- 右下角常驻一个 `Heysocks` 悬浮窗，会挡住窗口右下角的菜单项；窗口最大化后菜单在它上方，
  或把窗口挪开后菜单跟着挪，都能绕开。
- 点击前会强制把窗口提到前台；如果你正在别的窗口打字，会被抢焦点。
- 连接器的 `ask_gemini` 在发送期间要求输入框为空且页面不跳转；手动点击/切对话会让它报
  `APP_HAS_DRAFT` / `APP_CONTEXT_CHANGED`。自动化跑的时候不要同时点。

## 与连接器的关系

连接器（`ask_gemini`）只能「打字 + 点发送」；模型下拉和思考等级它点不到，所以
`model_label` 一直显示 `unverified`。这个工具是旁路：不碰连接器代码、不重启进程，
只在屏幕上操作。需要改模型/档位时用它，改完照常调 `ask_gemini`。
