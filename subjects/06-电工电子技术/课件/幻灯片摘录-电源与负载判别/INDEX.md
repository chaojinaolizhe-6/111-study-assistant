---
# 该文件夹是课件摘录图片存放处，本文件供校验脚本识别目录（scripts 要求每个 subject 子目录有 INDEX.md）
---

# 幻灯片摘录：电源与负载的判别（Power absorbed / supplied）

- 来源：`../Chapter one -1-2026中白上传.pdf`、`../Chapter One -2-2026中白上传.pdf`
- 生成方式：2026-09-29 用 PyMuPDF 渲染 140 dpi（`fitz` → PNG，1400×788），**内容为课件原页，未裁剪**
- 用途：复习时直接看原页（避免"文字层碎片 ≠ 页面内容"）；配套讲解见 [`../../topics/C1-电源与负载判别.md`](../../topics/C1-电源与负载判别.md)
- 读取状态（2026-09-29）：①已登记 ✅ ②已渲染 ✅（15 页，此处存 10 张）③**内容已读 9/15** ④p37 判据已逐字核验

| 文件 | 对应页 | 内容 |
|------|--------|------|
| `Ch1-1-p37-核心判据-Power absorbed or supplied.png` | 章1-1 p37 | **核心判据页**：P = U·I；U、I 同方向→吸收；反方向→发出；粉框 "Notice: Not all the sources supply power." |
| `Ch1-1-p38-例-3A与3V无电阻.png` | 章1-1 p38 | 回路：3 A 电流源（箭头向上）+ 3 V 电压源（+ 在上），无电阻 |
| `Ch1-1-p39-例-1欧并联.png` | 章1-1 p39 | 三支路并联：3 A 源 / 1 Ω / 3 V 源 |
| `Ch1-1-p40-例-0.5欧.png` | 章1-1 p40 | 同 p39，电阻 0.5 Ω |
| `Ch1-1-p41-例-2欧.png` | 章1-1 p41 | 同 p39，电阻 2 Ω（**助手尚未读图**） |
| `Ch1-1-p42-例-1欧串联.png` | 章1-1 p42 | 串联回路：3 A 源 → 1 Ω 在顶部 → 3 V 源 |
| `Ch1-1-p43-追问-电流源一定发出功率吗.png` | 章1-1 p43 | 同 p42 + 绿框追问 "Does the current source in the circuit always provide power?" |
| `Ch1-2-p09-Review-5V与1A与R.png` | 章1-2 p09 | Review：5 V 源 / 1 A 源 / R 三支路并联 |
| `Ch1-2-p11-Review-3A与1欧与3V.png` | 章1-2 p11 | Review：3 A 源 / 1 Ω / 3 V 源（同 p39） |
| `Ch1-2-p13-Review-通用二端块-方向一致即吸收.png` | 章1-2 p13 | Review：通用二端方框，I 流入 + 端 → 吸收 |

> 另渲染未存盘：`Chapter One -2` p06、p07、p08、p10、p12（同批 Review 页）；需要时用 PyMuPDF 重新渲染即可。
