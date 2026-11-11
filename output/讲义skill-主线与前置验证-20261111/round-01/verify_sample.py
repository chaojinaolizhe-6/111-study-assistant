#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reproducible checks for round-01/sample.tex.

This script checks the numerical/symbolic claims used in the sample:
- the non-symmetric quadratic form only sees the symmetric part;
- the 2D ellipse example and its principal axes;
- the 3D diagonalization example;
- the 2x2 symmetric lemma (random coefficient checks);
- random 3x3 real symmetric spectral decompositions;
- invariance of the orthogonal complement used in the proof;
- the P7 trace identity;
- the inertia mini-example and Rayleigh bounds.

Any failed assertion exits non-zero.  Passing these checks does not replace
reading the printed proof or the PDF pages; it only verifies the algebra.
"""
from __future__ import annotations

import sys

import numpy as np
import sympy as sp

np.set_printoptions(precision=8, suppress=True)
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not bool(condition):
        raise AssertionError(message)


def main() -> int:
    # 1. The symmetric-part example in section 1.1.
    x, y = sp.symbols("x y", real=True)
    T = sp.Matrix([[1, 2], [0, 1]])
    a = sp.Matrix([x, y])
    E_T = sp.expand((a.T * T * a)[0])
    S = (T + T.T) / 2
    E_S = sp.expand((a.T * S * a)[0])
    check(sp.simplify(E_T - (x + y) ** 2) == 0,
          "non-symmetric quadratic form is not (x+y)^2")
    check(sp.simplify(E_T - E_S) == 0, "symmetric part changes the quadratic form")

    # 2. The rotated 2D ellipse example in section 1.2.
    T2 = sp.Matrix([[2, 1], [1, 2]])
    n1 = sp.Matrix([1, 1]) / sp.sqrt(2)
    n2 = sp.Matrix([-1, 1]) / sp.sqrt(2)
    check(sp.simplify(T2 * n1 - 3 * n1) == sp.zeros(2, 1), "n1 is not a 3-eigenvector")
    check(sp.simplify(T2 * n2 - n2) == sp.zeros(2, 1), "n2 is not a 1-eigenvector")
    check(sp.simplify(n1.dot(n2)) == 0, "n1 and n2 are not orthogonal")
    check(sp.simplify(n1.dot(n1) - 1) == 0 and sp.simplify(n2.dot(n2) - 1) == 0,
          "principal directions are not unit vectors")
    u, v = sp.symbols("u v", real=True)
    E2 = sp.expand(2 * x**2 + 2 * x * y + 2 * y**2)
    substituted = sp.expand(E2.subs({x: (u - v) / sp.sqrt(2), y: (u + v) / sp.sqrt(2)}))
    check(sp.simplify(substituted - (3 * u**2 + v**2)) == 0,
          "rotated quadratic form is not 3u^2+v^2")
    check(abs(float(1 / sp.sqrt(3)) - 0.5773502691896257) < 1e-12,
          "semi-axis 1/sqrt(3) is wrong")

    # 3. The 3D diagonalization example in section 1.3.
    D = sp.Matrix([[6, 2, 0], [2, 6, 0], [0, 0, 1]])
    lam = sp.symbols("lam")
    p = sp.expand((D - lam * sp.eye(3)).det())
    check(sp.simplify(p - (1 - lam) * (lam - 4) * (lam - 8)) == 0,
          "characteristic polynomial of D does not factor as stated")
    e1 = sp.Matrix([1, 1, 0]) / sp.sqrt(2)
    e2 = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
    e3 = sp.Matrix([0, 0, 1])
    for vec, mu, name in ((e1, 8, "e1"), (e2, 4, "e2"), (e3, 1, "e3")):
        check(sp.simplify(D * vec - mu * vec) == sp.zeros(3, 1), f"{name} is not an eigenvector")
    for i in range(3):
        for j in range(i + 1, 3):
            vecs = (e1, e2, e3)
            check(sp.simplify(vecs[i].dot(vecs[j])) == 0, "3D principal axes are not orthogonal")
    reconstructed = 8 * (e1 * e1.T) + 4 * (e2 * e2.T) + 1 * (e3 * e3.T)
    check(sp.simplify(reconstructed - D) == sp.zeros(3, 3), "spectral reconstruction does not give D")
    check(D.trace() == 13 == 8 + 4 + 1, "trace check for D failed")
    check(D.det() == 32 == 8 * 4 * 1, "determinant check for D failed")

    # 4. Random 2x2 symmetric lemma checks.
    rng = np.random.default_rng(20261111)
    for _ in range(500):
        a0, b0, d0 = rng.normal(size=3)
        B = np.array([[a0, b0], [b0, d0]])
        disc = (a0 - d0) ** 2 + 4 * b0**2
        check(disc >= -1e-12, "2x2 discriminant is negative")
        roots = np.linalg.eigvalsh(B)
        check(np.all(np.isreal(roots)), "2x2 symmetric matrix has a non-real eigenvalue")
        if abs(b0) > 1e-12:
            check((a0 - d0) ** 2 + 4 * b0**2 > 0, "distinct-root claim failed for b != 0")
            mu_plus = ((a0 + d0) + np.sqrt(disc)) / 2
            mu_minus = ((a0 + d0) - np.sqrt(disc)) / 2
            v_plus = np.array([b0, mu_plus - a0])
            v_minus = np.array([b0, mu_minus - a0])
            check(np.allclose(B @ v_plus, mu_plus * v_plus), "v_plus is not an eigenvector")
            check(np.allclose(B @ v_minus, mu_minus * v_minus), "v_minus is not an eigenvector")
            check(abs(v_plus @ v_minus) < 1e-9, "2x2 eigenvectors are not orthogonal")
            check(np.allclose(np.sort(roots), np.sort([mu_plus, mu_minus])),
                  "2x2 roots do not match the discriminant formula")

    # 5. Random 3x3 real symmetric spectral decomposition.
    for _ in range(500):
        M = rng.normal(size=(3, 3))
        A = M + M.T
        check(np.allclose(A, A.T), "random matrix is not symmetric")
        w, V = np.linalg.eigh(A)
        check(np.all(np.isreal(w)), "symmetric matrix has non-real eigenvalues")
        check(np.allclose(V.T @ V, np.eye(3)), "eigenvectors are not orthonormal")
        check(np.allclose(V @ np.diag(w) @ V.T, A), "spectral reconstruction failed")
        # T preserves the orthogonal complement of its first eigenvector.
        u0 = V[:, 0]
        z = rng.normal(size=3)
        z = z - (z @ u0) * u0
        check(abs(z @ u0) < 1e-10, "test vector is not in the orthogonal complement")
        check(abs((A @ z) @ u0) < 1e-10, "T does not preserve the orthogonal complement")

    # 6. P7: cyclic trace and orthogonal change of basis.
    for _ in range(200):
        A0 = rng.normal(size=(3, 3))
        B0 = rng.normal(size=(3, 3))
        check(abs(np.trace(A0 @ B0) - np.trace(B0 @ A0)) < 1e-10,
              "trace is not cyclic")
        Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        check(np.allclose(Q.T @ Q, np.eye(3)), "QR matrix is not orthogonal")
        T0 = rng.normal(size=(3, 3))
        check(abs(np.trace(Q.T @ T0 @ Q) - np.trace(T0)) < 1e-10,
              "orthogonal change of basis does not preserve trace")

    # 7. Inertia mini-example and Rayleigh bounds.
    J = np.diag([1.0, 2.0, 3.0])
    n = np.ones(3) / np.sqrt(3)
    I = n @ J @ n
    check(abs(I - 2.0) < 1e-12, "inertia mini-example is not 2")
    check(1.0 - 1e-12 <= I <= 3.0 + 1e-12, "Rayleigh bound failed for the mini-example")
    for _ in range(500):
        M = rng.normal(size=(3, 3))
        A = M + M.T
        w, _ = np.linalg.eigh(A)
        z = rng.normal(size=3)
        quotient = (z @ A @ z) / (z @ z)
        check(w.min() - 1e-10 <= quotient <= w.max() + 1e-10,
              "Rayleigh quotient is outside [lambda_min, lambda_max]")

    print(f"checks executed: {checks}")
    print("ALL ASSERTIONS PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ASSERTION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
