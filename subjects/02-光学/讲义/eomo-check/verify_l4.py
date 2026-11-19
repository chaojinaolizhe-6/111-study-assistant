# -*- coding: utf-8 -*-
"""Lecture 4 (Electro-optic & Magneto-optic) numbers check.
All checks are assertions; any failure exits non-zero.
"""
import sys
import math

ok = []


def chk(name, got, want, rel=2e-3):
    good = (want == 0 and abs(got) < 1e-12) or abs(got - want) <= rel * abs(want)
    ok.append((name, got, want, good))
    return good


# ---------------- Problem 1: Pockels, transverse ----------------
r = 10.6e-12      # m/V
n = 1.5
lam = 633e-9      # m
L = 0.03          # m
d = 0.005         # m
V = 5.0e3         # V

E = V / d                                  # V/m
dphi = 2 * math.pi * n**3 * r * E * L / lam
Vpi = lam * d / (2 * n**3 * r * L)
chk("P1 E (V/m)", E, 1.0e6)
chk("P1 dphi (rad)", dphi, 10.654, 1e-3)
chk("P1 dphi = pi V/Vpi", dphi, math.pi * V / Vpi, 1e-9)
chk("P1 Vpi (V)", Vpi, 1474.5, 1e-3)
chk("P1 Vpi transverse formula = lam*d/(2n^3 r L)", Vpi, lam * d / (2 * n**3 * r * L), 1e-12)

# longitudinal reading (length drops out): dphi_l = 2pi n^3 r V / lam
dphi_l = 2 * math.pi * n**3 * r * V / lam
Vpi_l = lam / (2 * n**3 * r)
chk("P1-long dphi (rad)", dphi_l, 1.7755, 1e-3)
chk("P1-long Vpi (V)", Vpi_l, 8846.96, 1e-3)
chk("P1 dphi in degrees", math.degrees(dphi), 610.4, 1e-3)
chk("P1 dphi in units of pi", dphi / math.pi, 3.391, 1e-3)
chk("P1 V/Vpi", V / Vpi, 3.391, 1e-3)

# ---------------- Problem 2: Faraday ----------------
verdet = 20.0     # rad/(T m)
B = 0.5           # T
Lf = 0.10         # m
theta = verdet * B * Lf
chk("P2 theta (rad)", theta, 1.0)
chk("P2 theta (deg)", math.degrees(theta), 57.2958, 1e-6)
chk("P2 double pass (rad)", 2 * theta, 2.0)
chk("P2 double pass (deg)", math.degrees(2 * theta), 114.59, 1e-3)

# ---------------- Problem 3: Kerr ----------------
K = 2.0e-14       # m/V^2
Ek = 1.0e6        # V/m
dn = K * lam * Ek**2
dphi_k = 2 * math.pi * dn * 0.01 / lam
chk("P3 dn", dn, 1.266e-8, 1e-3)
chk("P3 dphi (rad)", dphi_k, 1.2566e-3, 1e-3)
chk("P3 dphi = 2 pi K E^2 L (lam cancels)", dphi_k, 2 * math.pi * K * Ek**2 * 0.01, 1e-12)
# comparison with Pockels birefringence at the same field
dn_pockels = 0.5 * n**3 * r * Ek
chk("P3 Pockels dn at 1e6 V/m", dn_pockels, 1.789e-5, 1e-3)
chk("P3 ratio Pockels/Kerr", dn_pockels / dn, 1413.0, 1e-2)

# ---------------- courseware worked examples (p43-p52, p79-p81) ----------------
# p45: KDP transverse at 1550 nm, L=2cm, d=5mm, n=1.51, r=10.5e-12
Vpi_cw = 1.55e-6 * 0.005 / (2 * 1.51**3 * 10.5e-12 * 0.02)
chk("cw p45 Vpi (V)", Vpi_cw, 5360.0, 1e-3)
# p48: Kerr cell, K=2.2e-14, d=1cm, L=5cm, Gamma=pi/2
Vc = 0.01 / math.sqrt(4 * 2.2e-14 * 0.05)
chk("cw p48 V (V)", Vc, 1.508e5, 1e-3)
# p49-p52: Vpi=4kV -> V=Vpi/2=2kV, Iout=1mW of 2mW
chk("cw p51 V (V)", 4e3 / 2, 2e3)
chk("cw p52 Iout (mW)", 0.5 * 2.0, 1.0)
# p79: TGG 40 rad/(T m), B=0.8, L=5cm
chk("cw p79 theta (rad)", 40 * 0.8 * 0.05, 1.6, 1e-9)
chk("cw p79 theta (deg)", math.degrees(1.6), 91.67, 1e-3)
# p80: 45 deg, V=25, B=0.5
chk("cw p80 L (m)", (math.pi / 4) / (25 * 0.5), 0.06283, 1e-3)
# p81: 45 deg, B=0.3, V=30 / 120
chk("cw p81 LA (m)", (math.pi / 4) / (30 * 0.3), 0.08727, 1e-3)
chk("cw p81 LB (m)", (math.pi / 4) / (120 * 0.3), 0.02182, 1e-3)

# ---------------- half-wave voltage table vs formula (口径) ----------------
for nn, rr, lamx, tag in [(1.51, 10.5e-12, 633e-9, "KDP @633"),
                          (1.51, 10.5e-12, 546e-9, "KDP @546")]:
    chk("Vpi %s" % tag, lamx / (2 * nn**3 * rr), (8756.6 if lamx > 600e-9 else 7553.0), 2e-3)
# LiNbO3 transverse with l/d=10 (n=2.2, r33=30.8pm/V)
chk("LiNbO3 Vpi*(d/l) (V)", 633e-9 / (2 * 2.2**3 * 30.8e-12), 965.0, 5e-3)
chk("LiNbO3 transverse l/d=10 (V)", 633e-9 / (2 * 2.2**3 * 30.8e-12) * 0.1, 96.5, 5e-3)

# ---------------- teaching mini-examples used in the text ----------------
# mini 1: dn = 1e-5, L=1cm, lam=633nm -> phase
chk("mini dn->dphi (rad)", 2 * math.pi * 1e-5 * 0.01 / 633e-9, 0.9927, 1e-3)
# mini 2: quadrature linearisation, Vpi=4kV, v=0.1kV
T0 = math.sin(math.pi * 2e3 / (2 * 4e3))**2
T1 = math.sin(math.pi * 2.1e3 / (2 * 4e3))**2
chk("mini quad T(2kV)", T0, 0.5, 1e-9)
chk("mini quad dT exact", T1 - T0, 0.03926, 1e-2)
chk("mini quad dT linear (pi/2)(v/Vpi)", math.pi / 2 * 0.1 / 4.0, 0.03927, 1e-3)
# mini 3: Faraday example with different numbers (25 rad/Tm, 0.4 T, 5 cm)
chk("mini faraday (rad)", 25 * 0.4 * 0.05, 0.5, 1e-9)
# mini 4: quarter wave at 22.5 deg double pass
chk("mini isolator 22.5*2 (deg)", 2 * 22.5, 45.0)
# mini 5: optical activity two pass cancels
chk("mini OA two pass (deg)", 22.5 - 22.5, 0.0)
# mini 6: real part / imaginary part of n_pm
gam = 1e-5
chk("mini n+ = sqrt(eps+gam) rel", math.sqrt(1 + gam) - 1, 0.5 * gam, 1e-2)
# mini 7: delta n between the two circular modes for Faraday: 2*theta*lam/(2pi L)
th = 1.0
Lx = 0.1
chk("mini Faraday dn = theta*lam/(pi L)", th * 589e-9 / (math.pi * Lx), 1.875e-6, 1e-2)

# ---------------- CD / g factor, Voigt ----------------
chk("CD g = dA/A example", 1e-3 / 1.0, 1e-3)

print("%-46s %14s %14s %s" % ("check", "computed", "expected", "ok"))
bad = 0
for name, got, want, good in ok:
    print("%-46s %14.6g %14.6g %s" % (name, got, want, "PASS" if good else "FAIL"))
    if not good:
        bad += 1
print("\n%d checks, %d failed" % (len(ok), bad))
sys.exit(1 if bad else 0)
