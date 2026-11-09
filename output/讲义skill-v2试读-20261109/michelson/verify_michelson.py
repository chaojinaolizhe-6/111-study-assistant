"""Check excerpt geometry and numbers; a failed assertion exits nonzero.

These checks do not establish the real instrument's coating phase or measured
parameters. Run with: python -B verify_michelson.py
"""
import math
import sympy as s


def require_equal(actual, expected, description):
    difference = s.trigsimp(s.simplify(actual - expected))
    if difference != 0:
        raise AssertionError(f"{description}: difference = {difference}")


def require_close(actual, expected, description, tolerance=1e-9):
    if not math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=tolerance):
        raise AssertionError(f"{description}: {actual} != {expected}")


def main():
    count = 0

    def eq(actual, expected, description):
        nonlocal count
        require_equal(actual, expected, description)
        count += 1

    def close(actual, expected, description, tolerance=1e-9):
        nonlocal count
        require_close(actual, expected, description, tolerance)
        count += 1

    d, theta, n, lam = s.symbols('d theta n lambda', positive=True)
    eq(2*d/s.cos(theta)-2*d*s.tan(theta)*s.sin(theta),
       2*d*s.cos(theta), 'air-film optical path difference')
    # External refractive index is 1: sin(theta0) = n sin(theta).
    eq(2*n*d/s.cos(theta)-2*d*s.tan(theta)*(n*s.sin(theta)),
       2*n*d*s.cos(theta), 'Snell substitution in film path difference')
    eq((2*n*d*s.cos(theta))**2,
       (2*d)**2*(n*n-(n*s.sin(theta))**2),
       'external-angle formula squared; positive cosine selects positive root')

    # Exact coordinates of Figure 1: d=2, theta=30 degrees.
    A = s.Matrix([0, 2]); B = s.Matrix([2/s.sqrt(3), 0])
    C = s.Matrix([4/s.sqrt(3), 2]); D = s.Matrix([1/s.sqrt(3), 3])
    u = s.Matrix([s.Rational(1, 2), s.sqrt(3)/2])
    eq((C-D).dot(u), 0, 'CD perpendicular to outgoing rays')
    eq((D-A)[0]*u[1]-(D-A)[1]*u[0], 0, 'D lies on ray 1')
    eq((A-B).norm(), 2/s.cos(s.pi/6), 'AB = d/cos(theta)')
    eq((C-B).norm(), 2/s.cos(s.pi/6), 'BC = d/cos(theta)')
    eq((C-A).norm(), 4*s.tan(s.pi/6), 'AC = 2d tan(theta)')
    eq((D-A).norm(), (C-A).dot(u), 'AD is the projected path')
    eq((A-B).norm()+(C-B).norm()-(D-A).norm(),
       4*s.cos(s.pi/6), 'AB + BC - AD = 2d cos(theta)')
    print('Figure 1: exact named points, reflection lengths and comparison plane PASS')

    phi, d1, d2 = s.symbols('phi d1 d2', real=True)
    q1 = 2*d1/lam+phi/(2*s.pi)
    q2 = 2*d2/lam+phi/(2*s.pi)
    eq(q2-q1, 2*(d2-d1)/lam, 'fixed coating phase cancels from fringe count')
    eq(s.cos(2*s.pi*s.Integer(3000)), 1, 'integer phase order gives bright fringe')

    # Example A: chosen phi0=0 and exactly integer central bright order.
    wavelength = s.Rational(6328, 10)*s.Rational(1, 10**9)
    K = s.Integer(3000)
    d0 = K*wavelength/2
    z = s.Rational(1, 2)
    eq(d0*1000, s.Rational(9492, 10000), 'selected d0 in mm')
    eq(2*d0/wavelength, K, 'central order exactly integer')
    old_order = 2*s.Rational(1, 1000)/wavelength
    if old_order.is_integer is not False:
        raise AssertionError('regression guard: d=1 mm must not imply integer bright center')
    count += 1
    expected_radius = ['12.91', '18.26', '22.36', '25.82']
    expected_gap = ['5.35', '4.10', '3.46']
    previous = None
    print(f'Example A: lambda={float(wavelength*10**9):.1f} nm; K={K}; d0={float(d0*1000):.4f} mm; phi0=0')
    for m in range(1, 5):
        cosine = 1-s.Rational(m, 1)*wavelength/(2*d0)
        eq(2*d0*cosine/wavelength, K-m, f'bright ring {m} order')
        radius = z*s.sqrt(m*wavelength/d0)*1000
        close(round(float(radius), 2), float(expected_radius[m-1]), f'ring {m} displayed radius')
        gap = None if previous is None else radius-previous
        if gap is not None:
            close(round(float(gap), 2), float(expected_gap[m-2]), f'ring {m} displayed spacing')
        exact_angle = math.acos(float(cosine))
        exact_radius = float(z)*math.tan(exact_angle)*1000
        gap_text = '--' if gap is None else f'{float(gap):.9f}'
        print(f'  m={m}: r_paraxial={float(radius):.9f} mm; gap={gap_text}; theta={math.degrees(exact_angle):.9f} deg; angular-model r={exact_radius:.9f} mm')
        previous = radius
    close(round(math.degrees(math.acos(1-1/3000)), 2), 1.48, 'first-ring angle')

    # Separate example B: d=1 mm only compares optical paths.
    expected_paths = [2.000000000, 1.999695390, 1.998781654, 1.997259070]
    print('Example B: d=1 mm, no assumption that center is bright')
    for angle, expected in enumerate(expected_paths):
        path_mm = 2*math.cos(math.radians(angle))
        close(path_mm, expected, f'angle {angle} displayed path in mm', 5e-10)
        print(f'  theta={angle} deg: DeltaL={path_mm:.9f} mm; decrease={(2-path_mm)*1e6:.3f} nm')

    eq(s.Rational('0.01')/s.Rational('0.0005'), 20, 'source screw reduction ratio')
    expected_counts = [
        (1, '0.3164', '0.006328'), (40, '12.656', '0.25312'),
        (50, '15.82', '0.3164'), (160, '50.624', '1.01248'),
        (280, '88.592', '1.77184'), (550, '174.02', '3.4804'),
    ]
    print('Fringe count / mirror displacement / screw reading:')
    for N, mirror_um, screw_mm in expected_counts:
        displacement = N*wavelength/2
        eq(displacement*10**6, s.Rational(mirror_um), f'{N} rings mirror displacement')
        eq(20*displacement*1000, s.Rational(screw_mm), f'{N} rings screw reading')
        print(f'  N={N}: mirror={mirror_um} um; screw={screw_mm} mm')
    eq(2*(s.Rational('1.01248')/20)*s.Rational(1, 1000)/160,
       wavelength, 'inverse wavelength from preview successive difference')
    for N1, N2 in zip([0, 40, 80, 120], [160, 200, 240, 280]):
        eq(s.Integer(N2-N1), 160, 'preview table paired count difference')

    # Source air-index relation assumes index excess proportional to pressure.
    N, ell, pamb, dp = s.symbols('N ell p_amb Delta_p', positive=True)
    ambient_index = 1+N*lam/(2*ell)*pamb/dp
    delta_n = (ambient_index-1)*dp/pamb
    eq(2*ell*delta_n, N*lam, 'double-pass gas-cell path change and source air-index formula')
    print('Air index: n_amb=1+N lambda p_amb/(2 l Delta_p), pressure-proportional index excess PASS')
    print(f'PASS: {count} explicit assertions. A failed assertion raises and returns nonzero.')


if __name__ == '__main__':
    main()
