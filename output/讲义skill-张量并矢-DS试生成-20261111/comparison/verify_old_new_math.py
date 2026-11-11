# -*- coding: utf-8 -*-
"""Numeric/algebraic checks for the four claims quoted in the comparison booklet.

Every assertion is executed; any failure exits non-zero and prints FAIL.
This does NOT test readability or learning; it only checks the arithmetic
that the booklet attributes to the two handouts.
"""
import sys
import numpy as np

PASS = []
FAIL = []


def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
        print(f"[PASS] {name}" + (f" | {detail}" if detail else ""))
    else:
        FAIL.append(name)
        print(f"[FAIL] {name}" + (f" | {detail}" if detail else ""))


def rot2(deg):
    a = np.deg2rad(deg)
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


def main():
    # ---- B1: old §4.5 printed T' = R T R^T, but old §4.4 and direct
    # projection give T' = R^T T R.
    T = np.array([[2.0, 0.0], [0.0, 1.0]])
    R = rot2(45)          # columns are the new basis vectors n1, n2 in the old basis
    # direct terminal-by-terminal projection: T'_ij = n_i · (T n_j)
    direct = np.array([[R[:, i] @ T @ R[:, j] for j in range(2)] for i in range(2)])
    correct = R.T @ T @ R     # old §4.4 / new §2.7
    wrong = R @ T @ R.T       # old §4.5 final sentence
    check("B1 direct projection == R^T T R", np.allclose(direct, correct),
          f"max|diff|={np.max(np.abs(direct - correct)):.3e}")
    check("B1 direct projection != R T R^T", not np.allclose(direct, wrong),
          f"max|diff|={np.max(np.abs(direct - wrong)):.3e}")
    # component form of old §4.4: T'_ij = R_ki R_lj T_kl
    comp = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            comp[i, j] = sum(R[k, i] * R[l, j] * T[k, l] for k in range(2) for l in range(2))
    check("B1 old §4.4 component law == R^T T R", np.allclose(comp, correct),
          f"max|diff|={np.max(np.abs(comp - correct)):.3e}")

    # ---- new §2.7 three-step algebra, random real case
    rng = np.random.default_rng(20261111)
    ok = True
    for _ in range(5):
        R3 = np.linalg.qr(rng.normal(size=(3, 3)))[0]
        if np.linalg.det(R3) < 0:
            R3[:, 0] *= -1
        T3 = rng.normal(size=(3, 3))
        Tp = R3.T @ T3 @ R3
        for _ in range(4):
            v = rng.normal(size=3)
            u = T3 @ v
            up = R3.T @ u
            vp = R3.T @ v
            ok = ok and np.allclose(up, Tp @ vp)
    check("B1 new §2.7: u'=T'v' holds with T'=R^T T R", ok)

    # ---- B2: P1 (old 例1) eigenvalues and the lambda=5 null vector
    D = np.array([[4.0, 1.0, 0.0], [1.0, 4.0, 0.0], [0.0, 0.0, 2.0]])
    M = D - 5 * np.eye(3)
    n1 = np.array([1.0, 1.0, 0.0]) / np.sqrt(2)
    wrong_dir = np.array([-1.0, 1.0, 0.0])
    check("B2 (D-5I)(1,1,0)=0", np.allclose(M @ np.array([1.0, 1.0, 0.0]), 0))
    check("B2 (-1,1,0) is not in the null space", not np.allclose(M @ wrong_dir, 0),
          f"|M(-e1+e2)|={np.linalg.norm(M @ wrong_dir):.3f}")
    check("B2 P1 eigenvalues are 2,3,5", np.allclose(np.sort(np.linalg.eigvalsh(D)), [2, 3, 5]))
    check("B2 n1 is a unit eigenvector of lambda=5", np.allclose(D @ n1, 5 * n1) and abs(np.linalg.norm(n1) - 1) < 1e-12)
    check("B2 P1 tr/det/D:D = 10/30/38",
          abs(np.trace(D) - 10) < 1e-12 and abs(np.linalg.det(D) - 30) < 1e-12
          and abs(np.sum(D * D) - 38) < 1e-12)

    # ---- A2: epsilon sign convention, old A_ij = -eps_ijk a_k, new (a^x)_ij = eps_ikj a_k
    a = np.array([1.0, 2.0, 3.0])

    def eps(i, j, k):
        if len({i, j, k}) < 3:
            return 0
        sign = 1 if (j - i) * (k - j) * (k - i) > 0 else -1
        return sign

    A_old = np.array([[sum(-eps(i + 1, j + 1, k + 1) * a[k] for k in range(3))]
                      for i in range(3) for j in range(3)]).reshape(3, 3)
    A_new = np.array([[sum(eps(i + 1, k + 1, j + 1) * a[k] for k in range(3))]
                      for i in range(3) for j in range(3)]).reshape(3, 3)
    x = np.array([0.5, -1.0, 2.0])
    check("A2 old/new epsilon matrices agree", np.allclose(A_old, A_new))
    check("A2 A_23 = -a_1", abs(A_old[1, 2] + a[0]) < 1e-12,
          f"A_23={A_old[1,2]:.3f}")
    check("A2 a^x x = a cross x", np.allclose(A_new @ x, np.cross(a, x)),
          f"max|diff|={np.max(np.abs(A_new @ x - np.cross(a, x))):.3e}")

    # ---- B3: figure 8 end-face signs and 30-degree decomposition
    s0 = 2.0
    sig = np.zeros((3, 3))
    sig[0, 0] = s0
    t_plus = sig @ np.array([1.0, 0.0, 0.0])
    t_minus = sig @ np.array([-1.0, 0.0, 0.0])
    check("B3 t(+e1)=+sigma0 e1", np.allclose(t_plus, [s0, 0, 0]))
    check("B3 t(-e1)=-sigma0 e1", np.allclose(t_minus, [-s0, 0, 0]))
    th = np.deg2rad(30)
    n = np.array([np.cos(th), np.sin(th), 0.0])
    t = sig @ n
    tn = t @ n
    tau_vec = t - tn * n
    tau = np.linalg.norm(tau_vec)
    check("B3 30deg tn=3/4 sigma0", abs(tn - 0.75 * s0) < 1e-12, f"tn={tn:.6f}")
    check("B3 30deg tau=sqrt3/4 sigma0", abs(tau - np.sqrt(3) / 4 * s0) < 1e-12, f"tau={tau:.6f}")
    check("B3 t is along +e1", np.allclose(t, [s0 * np.cos(th), 0, 0]),
          f"t=({t[0]:.6f},{t[1]:.6f},{t[2]:.6f})")

    print()
    print(f"TOTAL: {len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED:", ", ".join(FAIL))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
