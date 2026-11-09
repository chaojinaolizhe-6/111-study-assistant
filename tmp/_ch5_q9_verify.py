# -*- coding: utf-8 -*-
"""第五章乱序第 9 题：f(t)=A|sin wt| 在 (0,T), T=pi/w 上的傅里叶级数 —— 数值与符号复核。"""
import sympy as sp

t, w, A = sp.symbols('t omega A', positive=True)
T = sp.pi / w
n = sp.symbols('n', positive=True, integer=True)
k = sp.Symbol('k', positive=True, integer=True)

f = A * sp.Abs(sp.sin(w * t))
fs = A * sp.sin(w * t)          # 在 (0,T)= (0,pi/w) 上与 f 相同

# 0) 区间长度 T = pi/w 恰是 f 的一个整周期？
print("T =", T)
print("f(t+T)-f(t) 在 [0,pi] 上抽样:",
      [sp.simplify(f.subs(t, v + T) - f.subs(t, v)) for v in (sp.Rational(1, 3), sp.Rational(1, 2))])

# 1) 直接按 (0,T) 积分算系数：基频 2*pi/T = 2w
a0 = sp.simplify((2 / T) * sp.integrate(fs, (t, 0, T)))
print("\na0 =", a0, "  -> a0/2 =", sp.simplify(a0 / 2))

an = sp.simplify(sp.integrate((2 / T) * fs * sp.cos(2 * n * w * t), (t, 0, T)))
target = -4 * A / (sp.pi * (4 * n**2 - 1))
print("a_n =", an)
print("与 -4A/(pi(4n^2-1)) 之差 =", sp.simplify(an - target))

bn = sp.simplify(sp.integrate((2 / T) * fs * sp.sin(2 * n * w * t), (t, 0, T)))
print("b_n =", bn)

# 2) 正交性归一化常数
print("\nint_0^T cos^2(2nwt)dt =", sp.simplify(sp.integrate(sp.cos(2*n*w*t)**2, (t, 0, T))), "  T/2 =", sp.simplify(T/2))
print("int_0^T sin^2(2nwt)dt =", sp.simplify(sp.integrate(sp.sin(2*n*w*t)**2, (t, 0, T))))
print("int_0^T cos*sin     =", sp.simplify(sp.integrate(sp.cos(2*n*w*t)*sp.sin(2*n*w*t), (t, 0, T))))
print("int_0^T 1*cos       =", sp.simplify(sp.integrate(sp.cos(2*n*w*t), (t, 0, T))))

# 3) 换上下限合法：f 本身以 T 为周期 -> 任意长度 T 的窗口同值（负半周用 -sin 表示 |sin|）
left = sp.simplify(sp.integrate((-fs.subs(t, t)) * sp.cos(2 * n * w * t), (t, -T/2, 0)))
right = sp.simplify(sp.integrate(fs * sp.cos(2 * n * w * t), (t, 0, T/2)))
win0T = sp.simplify(sp.integrate(fs * sp.cos(2 * n * w * t), (t, 0, T)))
print("\n[换窗口] int_0^T =", win0T)
print("[换窗口] int_{-T/2}^{T/2} =", sp.simplify(left + right))
print("[换窗口] 两者之差 =", sp.simplify(win0T - (left + right)))

# 4) 中心窗口里偶函数红利给出同一个 a_n
an2 = sp.simplify((2 / T) * 2 * sp.integrate(fs.subs(t, t) * sp.cos(2*n*w*t), (t, 0, T/2)))
print("[中心窗口偶函数] a_n =", an2, " 与直接算之差 =", sp.simplify(an2 - an))

# 5) 反例：窗口不是整周期 -> 正交性失效
bad = sp.simplify(sp.integrate(sp.sin(w*t) * sp.sin(2*w*t), (t, 0, T/2)))
bad2 = sp.simplify(sp.integrate(sp.cos(w*t) * sp.cos(2*w*t), (t, 0, T/2)))
print("\n[反例] int_0^{T/2} sin(wt)sin(2wt)dt =", bad)
print("[反例] int_0^{T/2} cos(wt)cos(2wt)dt =", bad2)
print("[对照] int_0^{T} sin(wt)sin(2wt)dt  =", sp.simplify(sp.integrate(sp.sin(w*t)*sp.sin(2*w*t), (t, 0, T))))

# 6) 数值校验
import math
wv, Av = 1.7, 3.0
def series(tt, N=6000):
    s = 2 * Av / math.pi
    for kk in range(1, N + 1):
        s -= (4 * Av / math.pi) * math.cos(2 * kk * wv * tt) / (4 * kk * kk - 1)
    return s
def exact(tt):
    return Av * abs(math.sin(wv * tt))
Tv = math.pi / wv
print("\nT = pi/w =", Tv)
print("    t      |  级数部分和   |    真值     |  绝对误差")
for tt in [0.0, 0.11, 0.37, 0.62, 0.9186, 1.1, 1.55, 1.84, 0.9239 * 2]:
    print(f"  {tt:7.4f} | {series(tt):13.9f} | {exact(tt):12.9f} | {abs(series(tt)-exact(tt)):.2e}")

# 7) 常数项 = 平均；sum 1/(4k^2-1) = 1/2
S = sp.summation(1 / (4 * k**2 - 1), (k, 1, sp.oo))
print("\nsum_{k>=1} 1/(4k^2-1) =", S)
avg = sp.simplify((1 / T) * sp.integrate(fs, (t, 0, T)))
print("f 在一个周期上的平均 =", avg, " = 2A/pi ?", sp.simplify(avg - 2 * A / sp.pi) == 0)
