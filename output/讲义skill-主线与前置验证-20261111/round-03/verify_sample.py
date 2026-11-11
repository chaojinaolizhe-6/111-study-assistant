#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reproducible checks for round-03/sample.tex.

This script checks the numerical/symbolic claims used in the sample:
- the non-symmetric quadratic form only sees the symmetric part;
- the 2D ellipse example and its principal axes;
- the 3D diagonalization example;
- the 2x2 symmetric lemma (random coefficient checks);
- random 3x3 real symmetric spectral decompositions;
- invariance of the orthogonal complement used in the proof;
- the characteristic-polynomial factorization p_T(lambda)=prod(lambda_k-lambda) through an orthonormal eigenbasis, including repeated eigenvalues;
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

    # 1b. The point-product geometry example in section 0.1.
    p_a = np.array([3.0, 0.0])
    p_b = np.array([3.0, 4.0])
    p_c = np.array([0.0, 4.0])
    check(np.isclose(p_a @ p_b, 9.0), "3-4-5 dot product is not 9")
    check(np.isclose(np.linalg.norm(p_a), 3.0), "3-4-5 first length is not 3")
    check(np.isclose(np.linalg.norm(p_b), 5.0), "3-4-5 second length is not 5")
    check(np.isclose((p_a @ p_b) / (np.linalg.norm(p_a) * np.linalg.norm(p_b)), 3 / 5),
          "3-4-5 cosine is not 3/5")
    check(np.isclose(p_b @ (p_a / np.linalg.norm(p_a)), 3.0),
          "projection of b on a is not the horizontal component 3")
    check(np.isclose(p_a @ p_c, 0.0), "a and c are not orthogonal")

    proj_a = np.array([1.0, 2.0, 2.0])
    proj_n = np.ones(3) / np.sqrt(3)
    proj_scalar = proj_a @ proj_n
    check(np.isclose(proj_scalar, 5 / np.sqrt(3)), "projection scalar is not 5/sqrt(3)")
    proj_vec = proj_scalar * proj_n
    proj_rem = proj_a - proj_vec
    check(abs(proj_rem @ proj_n) < 1e-12, "projection remainder is not orthogonal")
    check(np.allclose(proj_rem, [-2 / 3, 1 / 3, 1 / 3]),
          "projection remainder is not (-2/3,1/3,1/3)")

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

    # 2b. The half-axis formula has two signed endpoints, not only the positive root.
    t_plus = 1 / sp.sqrt(3)
    for t_value, label in ((t_plus, "+"), (-t_plus, "-")):
        point = t_value * n1
        uu = n1.dot(point)
        vv = n2.dot(point)
        check(sp.simplify(3 * uu**2 + vv**2 - 1) == 0,
              f"endpoint with t{label} does not satisfy E=1")
    check(sp.simplify(abs(t_plus) - 1 / sp.sqrt(3)) == 0,
          "half-axis length is not |t|=1/sqrt(3)")

    # 2c. The concrete 3D coordinate/lifting example in section 1.4.
    T4 = sp.Matrix([[5, 0, 0], [0, 2, 1], [0, 1, 2]])
    i_vec = sp.Matrix([1, 0, 0])
    j_vec = sp.Matrix([0, 1, 0])
    k_vec = sp.Matrix([0, 0, 1])
    check(sp.simplify(T4 * i_vec - 5 * i_vec) == sp.zeros(3, 1),
          "T4 does not send i to 5i")
    B4 = sp.Matrix([[2, 1], [1, 2]])
    for col, vec in enumerate((j_vec, k_vec)):
        for row, out_vec in enumerate((j_vec, k_vec)):
            check(sp.simplify(out_vec.dot(T4 * vec) - B4[row, col]) == 0,
                  "B4 entry does not match e_i . T e_j")
    y_sym, z_sym = sp.symbols("y_sym z_sym", real=True)
    coord_vec = y_sym * j_vec + z_sym * k_vec
    lhs = T4 * coord_vec
    rhs = (2 * y_sym + z_sym) * j_vec + (y_sym + 2 * z_sym) * k_vec
    check(sp.simplify(lhs - rhs) == sp.zeros(3, 1),
          "2D coordinate action does not lift back to T on the plane")
    c2 = sp.Matrix([1, 1]) / sp.sqrt(2)
    c3 = sp.Matrix([1, -1]) / sp.sqrt(2)
    check(sp.simplify(B4 * c2 - 3 * c2) == sp.zeros(2, 1), "c2 is not a 3-eigenvector of B4")
    check(sp.simplify(B4 * c3 - c3) == sp.zeros(2, 1), "c3 is not a 1-eigenvector of B4")
    u2 = (j_vec + k_vec) / sp.sqrt(2)
    u3 = (j_vec - k_vec) / sp.sqrt(2)
    check(sp.simplify(T4 * u2 - 3 * u2) == sp.zeros(3, 1), "lifted u2 is not a 3-eigenvector")
    check(sp.simplify(T4 * u3 - u3) == sp.zeros(3, 1), "lifted u3 is not a 1-eigenvector")
    for left, right in ((i_vec, u2), (i_vec, u3), (u2, u3)):
        check(sp.simplify(left.dot(right)) == 0, "lifted basis is not orthogonal")
    for vec in (i_vec, u2, u3):
        check(sp.simplify(vec.dot(vec) - 1) == 0, "lifted basis is not normalized")
    check(sp.simplify(T4.trace() - 9) == 0 and sp.simplify(T4.det() - 15) == 0,
          "T4 trace/determinant do not match 5+3+1 and 5*3*1")

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
        # The eigenvalue-set statement used in the new step-four proof:
        # every eigenvalue of T is lambda_1 or an eigenvalue of B on P.
        B4 = V[:, 1:].T @ A @ V[:, 1:]
        wB = np.linalg.eigvalsh(B4)
        check(np.allclose(np.sort(w), np.sort(np.concatenate(([w[0]], wB)))),
              "eigenvalue set is not {lambda_1} union eigenvalues of B")

    # 5b. Characteristic-polynomial factorization through the orthonormal
    # eigenbasis: det(T - lambda I) = prod_k (lambda_k - lambda).  Both sides
    # are cubic in lambda, so agreement at four points checks the identity.
    for _ in range(20):
        M = rng.normal(size=(3, 3))
        A = M + M.T
        w, V = np.linalg.eigh(A)
        check(np.allclose(V.T @ V, np.eye(3)), "eigenbasis is not orthonormal")
        check(np.allclose(V.T @ A @ V, np.diag(w)), "Q^T T Q is not diagonal")
        for t in (-1.7, 0.3, 1.1, 2.4):
            lhs = np.linalg.det(A - t * np.eye(3))
            rhs = float(np.prod(w - t))
            check(abs(lhs - rhs) < 1e-9,
                  "det(T-lambda I) does not factor through the eigenbasis")
    # Repeated eigenvalues: the product keeps the same multiplicity.
    for _ in range(20):
        Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        A = Q @ np.diag([2.0, 2.0, 5.0]) @ Q.T
        w = np.linalg.eigvalsh(A)
        check(np.allclose(np.sort(w), [2.0, 2.0, 5.0]),
              "repeated-eigenvalue test lost its eigenvalues")
        for t in (-1.0, 0.5, 2.0, 4.0):
            lhs = np.linalg.det(A - t * np.eye(3))
            rhs = float(np.prod(w - t))
            check(abs(lhs - rhs) < 1e-9,
                  "repeated-root factorization does not match det(T-lambda I)")

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
        S0 = rng.normal(size=(3, 3))
        S0 = S0 + S0.T
        check(np.allclose((Q.T @ S0 @ Q).T, Q.T @ S0 @ Q),
              "orthogonal change of basis does not preserve symmetry")

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
