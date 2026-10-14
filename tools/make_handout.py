"""把「判据二」讲解渲染成图片。

字体限制（2026-09-28 实测）：微软雅黑缺 ẋ/θ̇ 这类「组合变音符」与 ᵢ 这类下标字母 → 显示为方框。
因此本脚本统一使用 ASCII 安全写法：速度写成 dq_i/dt，下标写成 _i / _a，避免任何组合字符。
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1700, 2350
M = 90
BG = (255, 255, 255)
FG = (28, 30, 36)
ACCENT = (12, 82, 160)
BOXBG = (238, 245, 253)
BOXBD = (12, 82, 160)
GRAY = (95, 100, 110)

REG = r"C:\Windows\Fonts\msyh.ttc"
BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

# 不安全字符 → 安全写法（渲染前统一替换）
SAFE = {
    "q̇ᵢ": "dq_i/dt",
    "q̇": "dq/dt",
    "θ̇": "dθ/dt",
    "ẋ": "dx/dt",
    "ᵢ": "_i",
    "ₐ": "_a",
    "₀": "0",
    "₁": "1",
    "₂": "2",
}


def safe(text: str) -> str:
    for bad, good in SAFE.items():
        text = text.replace(bad, good)
    return text


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if draw.textlength(cur + ch, font=f) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, title):
        self.im = Image.new("RGB", (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.y = M
        self.d.text((M, self.y), safe(title), font=font(52, True), fill=ACCENT)
        self.y += 82

    def para(self, text, size=32, bold=False, color=FG, gap=14, indent=0):
        f = font(size, bold)
        for line in wrap(self.d, safe(text), f, W - 2 * M - indent):
            self.d.text((M + indent, self.y), line, font=f, fill=color)
            self.y += int(size * 1.52)
        self.y += gap

    def step(self, tag, text, size=32):
        self.d.text((M, self.y), safe(tag), font=font(size, True), fill=ACCENT)
        self.y += int(size * 1.5)
        self.para(text, size=size, indent=36, gap=8)

    def box(self, title, lines):
        f1, f2 = font(31, True), font(31)
        wrapped = []
        for ln in lines:
            wrapped += wrap(self.d, safe(ln), f2, W - 2 * M - 60)
        h = 70 + int(31 * 1.5) * len(wrapped) + 30
        self.d.rounded_rectangle([M, self.y, W - M, self.y + h], 18, fill=BOXBG, outline=BOXBD, width=3)
        self.d.text((M + 30, self.y + 22), safe(title), font=f1, fill=BOXBD)
        yy = self.y + 22 + int(31 * 1.55)
        for ln in wrapped:
            self.d.text((M + 30, yy), ln, font=f2, fill=FG)
            yy += int(31 * 1.5)
        self.y += h + 24

    def rule(self):
        self.d.line([M, self.y, W - M, self.y], fill=(215, 218, 224), width=2)
        self.y += 26

    def save(self, path):
        self.im.save(path)
        print("saved", path, self.im.size)


# ---------------- 第 1 页 ----------------
c = Canvas("判据二：为什么 E 有时不等于 T + U")
c.para("出处：课件 p6 / p9（守恒条件）、p8（欧拉齐次定理）、p10（T = T2 + T1 + T0）；朗道《力学》§6，PDF 第 40-41 页", size=26, color=GRAY, gap=20)
c.rule()

c.step("第 0 步　定义式", "E = Σ (dq_i/dt)·(∂L/∂(dq_i/dt)) − L　　当 L 不显含 t 时守恒（课件 p9：dh/dt = −∂L/∂t）")
c.step("第 1 步　代入 L = T − U", "U 不含速度，所以 ∂L/∂(dq_i/dt) = ∂T/∂(dq_i/dt)，于是：\nE = Σ (dq_i/dt)·(∂T/∂(dq_i/dt)) − T + U\n→ 全部问题只剩一个量：Σ (dq_i/dt)·(∂T/∂(dq_i/dt)) 等于几？")
c.step("第 2 步　它是 2T 吗（齐次函数的欧拉定理）", "若 f 是 n 次齐次（f(λx) = λ^n f(x)），则 Σ x_i·(∂f/∂x_i) = n·f。\nT 若是速度的二次齐次 → 取 n = 2 → Σ (dq/dt)·(∂T/∂(dq/dt)) = 2T → E = 2T − T + U = T + U")
c.step("第 3 步　什么时候不是二次齐次", "位置 r = r(q, t)，速度 dr/dt = Σ (∂r/∂q_i)·(dq_i/dt) + ∂r/∂t\n其中 ∂r/∂t 这一块不含广义速度。把它平方展开：\nT = T2 + T1 + T0（二次项 + 一次项 + 零次项，课件 p10）\nT0 = Σ_a (1/2) m_a (∂r_a/∂t)^2 —— 来自「约束自己在动」，与质点相对约束的运动无关。")
c.step("第 4 步　逐项用欧拉定理", "T2 是 2 次齐次 → 2T2 ；T1 是 1 次齐次 → 1·T1 ；T0 与速度无关 → 0\n所以 Σ (dq/dt)·(∂T/∂(dq/dt)) = 2T2 + T1\n代回第 1 步：E = (2T2 + T1) − (T2 + T1 + T0) + U = T2 − T0 + U")
c.box("结论", [
    "约束静止（∂r/∂t = 0）→ T1 = T0 = 0 → E = T + U（判据二成立）",
    "约束在动（∂r/∂t ≠ 0）→ E = T2 − T0 + U，不等于 T + U（差 2T0）",
    "守恒与否由第 0 步决定；判据二只决定 E 是否等于机械能 T + U。",
])
c.save(r"subjects\01-理论力学\讲义\T04-判据二讲解-1.png")

# ---------------- 第 2 页 ----------------
c = Canvas("判据二：验算、你的理解、30 秒自检")
c.rule()
c.step("验算（H4.2 的环上珠子）", "T = (m/2)R^2(dθ/dt)^2 + (m/2)R^2Ω^2(sinθ)^2\n→ T2 = (m/2)R^2(dθ/dt)^2 ，T0 = (m/2)R^2Ω^2(sinθ)^2 ，U = −mgR·cosθ\nE = T2 − T0 + U = (m/2)R^2(dθ/dt)^2 − (m/2)R^2Ω^2(sinθ)^2 − mgR·cosθ\n而 T + U = (m/2)R^2(dθ/dt)^2 + (m/2)R^2Ω^2(sinθ)^2 − mgR·cosθ\n两者相差 2T0 —— 这就是「E 不等于 T + U」的全部内容。")
c.step("你的理解核对", "你说的「T0 里不含速度项」——对，但要精确：\nT0 不含的是【广义速度 dq/dt】（它来自约束的给定运动，比如 Ω），它可以显含时间 t。")
c.step("30 秒自检（回答这一句就算过关）", "对 H4.1 的 L = (m/2)(dx/dt)^2 − (k/2)(√(h^2+x^2) − l0)^2：\n它的 T1 和 T0 是不是 0？依据是什么？\n（提示：看这个系统的 r 里有没有 t。）")
c.box("H4.2 就写这三行", [
    "判据一：L 不显含 t（Ω 恒定）→ E 守恒（依据课件 p9）",
    "判据二：T = T2 + T0 含 T0 → E = T2 − T0 + U，不等于 T + U（依据课件 p10 + p8）",
    "直接计算：用拉格朗日方程算 dE/dt = 0",
])
c.step("教材 / 知识库对照（逐页核过）", "教材 §6 Energy，印刷页 13-14 = PDF 第 40-41 页：E 的定义、守恒条件、E = T + U（前提 T 是速度的二次函数）。\n教材 §5，印刷页 8-12 = PDF 第 35-39 页：T 在广义坐标下是二次型（式 5.5）。\n注意：T = T2 + T1 + T0 这个分解不在这本教材的 §5/§6，它出自课件 p10。\n知识库：卡片「定理_时空对称性与守恒定律」；章节「第02章_06_能量守恒」「第01章_05_质点系拉格朗日量」。")
c.save(r"subjects\01-理论力学\讲义\T04-判据二讲解-2.png")
