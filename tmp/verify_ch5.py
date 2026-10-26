# -*- coding: utf-8 -*-
"""第五章讲义修订：数值复核（sgn 表、七道作业）"""
import numpy as np

np.set_printoptions(precision=8, suppress=False)

def damped_F(f, w, L=4000.0, h=0.01, eps=2e-4):
    """(1/2pi) int f(t) e^{i w t} e^{-eps|t|} dt"""
    t = np.arange(-L, L + h / 2, h)
    g = f(t) * np.exp(1j * w * t) * np.exp(-eps * np.abs(t))
    val = np.trapezoid(g, t) / (2 * np.pi)
    return val

print("=" * 70)
print("B. sgn 表：f(t)=sin(w0 t)/(pi t)，w0=2")
w0 = 2.0
f = lambda t: np.sin(w0 * t) / (np.pi * t)
sgn = lambda x: 0.0 if x == 0 else (1.0 if x > 0 else -1.0)
for w in [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]:
    num = damped_F(f, w)
    pred = 0.5 * sgn(w + w0) - 0.5 * sgn(w - w0)   # 表里第 4 列
    print(f"  w={w:+.1f}  数值(带阻尼)={num.real:+.5f}{num.imag:+.5f}i   "
          f"表值={pred:+.3f}  F=(1/2pi)*表值={pred/(2*np.pi):+.6f}")

print("=" * 70)
print("C. 第1题 cos^3 x")
x = np.linspace(-3, 3, 7)
lhs = np.cos(x) ** 3
rhs = 0.75 * np.cos(x) + 0.25 * np.cos(3 * x)
print("  max|diff| =", np.max(np.abs(lhs - rhs)))

print("=" * 70)
print("D. 第2题 f=x/3 on (-l,l)，l=2")
l = 2.0
def ser2(x, N=2000):
    n = np.arange(1, N + 1)
    return np.sum((2 * l / (3 * n * np.pi)) * (-1) ** (n + 1) * np.sin(n * np.pi * x / l))
for xv in [-1.5, -0.7, 0.3, 1.2, 1.9]:
    print(f"  x={xv:+.2f}  级数={ser2(xv):+.6f}  x/3={xv/3:+.6f}")
print("  端点 x=l 级数 =", ser2(l), " f(l)=l/3=", l / 3)

print("=" * 70)
print("E. 第3题 A|sin wt|，A=1, w=1, T=2pi")
A, w, T = 1.0, 1.0, 2 * np.pi
def ser3(t, M=400):
    m = np.arange(1, M + 1)
    return 2 * A / np.pi - (4 * A / np.pi) * np.sum(np.cos(2 * m * w * t) / (4 * m ** 2 - 1))
for tv in [0.0, 0.3, np.pi / 2, 2.0, 5.0]:
    print(f"  t={tv:+.3f}  级数={ser3(tv):+.6f}  A|sin|= {A*abs(np.sin(w*tv)):+.6f}")

print("=" * 70)
print("F. 第4题 方波复数级数，H=1, T=2, T0=1")
H, T4, T0 = 1.0, 2.0, 1.0
def ser4(t, N=400):
    c0 = H * T0 / T4
    n = np.arange(1, N + 1)
    cn = (H / (n * np.pi)) * np.sin(n * np.pi * T0 / T4)
    s = c0 * np.ones_like(np.asarray(t, dtype=float))
    for k, c in zip(n, cn):
        s = s + c * np.exp(1j * 2 * np.pi * k * np.asarray(t) / T4)
        s = s + c * np.exp(-1j * 2 * np.pi * k * np.asarray(t) / T4)
    return s

for tv in [0.1, 0.4, 0.6, 0.9]:
    val = ser4(tv)
    exact = H if abs(tv) <= T0 / 2 else 0.0
    print(f"  t={tv:+.2f}  级数={val.real:+.5f}{val.imag:+.5f}i  方波={exact:+.1f}")

print("=" * 70)
print("G. 第5题 锯齿波 F(w)=(1/2pi)int_0^T t e^{-iwt}dt, T=2")
T5 = 2.0
def F5_closed(w):
    if abs(w) < 1e-12:
        return T5 ** 2 / (4 * np.pi) + 0j
    return (np.exp(-1j * w * T5) * (1 + 1j * w * T5) - 1) / (2 * np.pi * w ** 2)

def F5_num(w, N=400000):
    t = np.linspace(0, T5, N)
    return np.trapezoid(t * np.exp(-1j * w * t), t) / (2 * np.pi)

for wv in [0.3, 1.0, 3.7]:
    print(f"  w={wv:+.2f}  闭式={F5_closed(wv):.6f}  数值={F5_num(wv):.6f}")
print("  w->0 闭式 =", F5_closed(0), " 解析 T^2/(4pi) =", T5 ** 2 / (4 * np.pi))

print("=" * 70)
print("H. 第6题 e^{-a t}，a=0.5")
a = 0.5
def F6(w):
    return 1 / (2 * np.pi * (a + 1j * w))
for wv in [0.0, 1.0, 4.0]:
    t = np.linspace(0, 60, 200000)
    num = np.trapezoid(np.exp(-(a + 1j * wv) * t), t) / (2 * np.pi)
    print(f"  w={wv:+.1f}  闭式={F6(wv):.6f}  数值={num:.6f}")

print("=" * 70)
print("I. 第7题 Fresnel，al=1.3")
al = 1.3
def F7_num_cos(k, L=60.0, h=0.002, eps=1e-4):
    x = np.arange(-L, L + h / 2, h)
    g = np.cos(al * x ** 2) * np.exp(-1j * k * x) * np.exp(-eps * x ** 2)
    return np.trapezoid(g, x) / (2 * np.pi)

def F7_num_sin(k, L=60.0, h=0.002, eps=1e-4):
    x = np.arange(-L, L + h / 2, h)
    g = np.sin(al * x ** 2) * np.exp(-1j * k * x) * np.exp(-eps * x ** 2)
    return np.trapezoid(g, x) / (2 * np.pi)

pref = np.sqrt(np.pi / al) / (2 * np.pi)
for kv in [0.0, 0.8, 2.0]:
    ph = np.pi / 4 - kv ** 2 / (4 * al)
    pred_c = pref * np.cos(ph)
    pred_s = pref * np.sin(ph)
    nc = F7_num_cos(kv)
    ns = F7_num_sin(kv)
    print(f"  k={kv:+.1f}  cos: 公式={pred_c:+.6f} 数值={nc.real:+.6f} (虚部{nc.imag:+.2e})")
    print(f"        sin: 公式={pred_s:+.6f} 数值={ns.real:+.6f} (虚部{ns.imag:+.2e})")
