# -*- coding: utf-8 -*-
"""L16-17 矩阵指数讲义的可复现核验脚本。

覆盖：
  * 例1、例4、例5、例7、例8 的 F(0)=I 与 F'=AF 全式符号核验；
  * 作业1-3 的 F(0)=I 与 F'=AF 全式符号核验；
  * 例2 的多项式长除与矩阵恒等式；
  * 例6 四阶谱 5(三重)/2(单重) 的 Hermite 系数、谱条件、r_0=1，
    以及在具体实现 diag(J3(5),2) 上的 F'=AF 核验；
  * 例3 通用结构（n=2,3）的系数矩阵非奇异；
  * 原课件 p14、p15、p27、p36 四处印刷疑点的独立复算；
  * 例4 消元文字 3*alpha0 的核对。

输出：本文件同目录 verify_output.txt（UTF-8）。
"""
import io
import json
import sys
from pathlib import Path
import sympy as sp

x = sp.symbols('x', real=True)
out = []
checks = []
def P(*a):
    s = ' '.join(str(t) for t in a)
    out.append(s)
    print(s)

def mat(rows):
    return sp.Matrix(rows)

def check_F(name, A, F, note=''):
    """核验 F(0)=I 与 F'=AF（逐元素化简为 0）。"""
    n = A.shape[0]
    I = sp.eye(n)
    e0 = sp.simplify(F.subs(x, 0) - I)
    e1 = sp.simplify(sp.diff(F, x) - A * F)
    ok0 = e0.is_zero_matrix
    ok1 = e1.is_zero_matrix
    P(f'[{name}] F(0)=I : {ok0}')
    P(f'[{name}] F\'(x)=A F(x) : {ok1}')
    if not ok0:
        P('   残差(0)=', e0)
    if not ok1:
        P('   残差=', e1)
    if note:
        P('   注：', note)
    checks.append((name, bool(ok0 and ok1)))
    return ok0 and ok1

# ---------------------------------------------------------------- 例1
A1 = mat([[1, -1, 1], [1, 1, -1], [2, -1, 0]])
V1 = mat([[1, 1, -1], [0, 1, 3], [1, 1, 5]])
L1 = sp.diag(2, 1, -1)
P('=== 例1 (课件 p13-p15) ===')
P('A1 =', A1.tolist())
P('char poly =', sp.factor(A1.charpoly().as_expr()))
P('eigenvects =', [(e, m) for e, m, _ in A1.eigenvects()])
V1inv = sp.simplify(V1.inv())
P('V1^-1 (实际) =', V1inv.tolist())
P('V1^-1 * V1 =', sp.simplify(V1inv * V1).tolist())
P('课件 p14 印的 V^-1 =', [[sp.Rational(1,3), 0, sp.Rational(2,3)],
                            [sp.Rational(1,2), 1, -sp.Rational(1,2)],
                            [-sp.Rational(1,6), 0, sp.Rational(1,6)]])
F1 = sp.simplify(V1 * sp.diag(sp.exp(2*x), sp.exp(x), sp.exp(-x)) * V1inv)
check_F('例1', A1, F1)
P('e^{A1 x} =', sp.simplify(F1).tolist())
P('化为三个秩一指数项：')
for i in range(3):
    Vi = V1[:, i]
    Wi = V1inv[i, :]
    P(f'  lambda={L1[i,i]}: V{i+1} W{i+1} =', sp.simplify(Vi * Wi).tolist())
P('初值通解 Y(x0)=Y0 用 e^{A(x-x0)} 核验：F1(x0)=I 仅当 x0=0')

# ---------------------------------------------------------------- 例2
P('\n=== 例2 (课件 p20) ===')
s = sp.symbols('s')
A2 = mat([[3, 1], [1, 2]])
p2 = s**4 + 3*s**3 + 2*s**2 + s + 1
Delta2 = sp.expand((s - A2.eigenvals().popitem()[0]) * 0 + (s**2 - 5*s + 5))
q2, r2 = sp.div(p2, Delta2, s)
P('Delta(s) =', Delta2, ' q(s) =', q2, ' r(s) =', sp.expand(r2))
P('q*Delta+r - p =', sp.simplify(sp.expand(q2 * Delta2 + r2 - p2)))
P('p(A) - (146A-184I) =', sp.simplify((A2**4 + 3*A2**3 + 2*A2**2 + A2 + sp.eye(2)) - (146*A2 - 184*sp.eye(2))).tolist())
P('146A-184I =', (146*A2 - 184*sp.eye(2)).tolist())

# ---------------------------------------------------------------- 例3 通用结构
P('\n=== 例3 (课件 p23) 通用结构 ===')
for n in (2, 3):
    mus = sp.symbols('mu1:%d' % (n+1))
    # 系数矩阵 Vandermonde：r(mu_j)=e^{mu_j x} 的未知量是 beta_0..beta_{n-1}
    M = sp.Matrix(n, n, lambda i, j: mus[i]**j)
    P(f'n={n} 谱方程系数矩阵 det =', sp.factor(M.det()))
P('例7 重根 x=0 处方程组矩阵 [[4,-2,1],[-4,1,0],[2,0,0]] det =',
  sp.Matrix([[4,-2,1],[-4,1,0],[2,0,0]]).det())

# ---------------------------------------------------------------- 例4
P('\n=== 例4 (课件 p24-p25) ===')
A4 = mat([[1, 1], [9, 1]])
P('eigenvalues =', A4.eigenvals())
a1x = (sp.exp(4*x) - sp.exp(-2*x))/6
a0 = (sp.exp(4*x) + 2*sp.exp(-2*x))/3
P('alpha1*x =', sp.simplify(a1x), ' ; alpha0 =', sp.simplify(a0))
F4 = sp.simplify(a1x*A4 + a0*sp.eye(2))
check_F('例4', A4, F4)
P('e^{A4 x} =', F4.tolist())
# 直接用未知量验证 3 alpha0
a0s, a1xs = sp.symbols('a0 a1x')
eq1 = sp.Eq(sp.exp(4*x), 4*a1xs + a0s)
eq2 = sp.Eq(sp.exp(-2*x), -2*a1xs + a0s)
sol = sp.solve([eq1, eq2], [a1xs, a0s], dict=True)[0]
P('解出 x*alpha1 =', sp.simplify(sol[a1xs]), ' alpha0 =', sp.simplify(sol[a0s]))
P('直接相加得 2*x*alpha1 + 2*alpha0；第一式加第二式两倍得 3*alpha0 :',
  sp.simplify((eq1.lhs + 2*eq2.lhs) - 3*sol[a0s]))

# ---------------------------------------------------------------- 例5
P('\n=== 例5 (课件 p26-p27) ===')
A5 = mat([[0, 1], [-1, 0]])
F5 = mat([[sp.cos(x), sp.sin(x)], [-sp.sin(x), sp.cos(x)]])
check_F('例5', A5, F5)
P('A5^2 =', (A5**2).tolist())
P('课件 p27 展开通解印为 c1(cos,-sin)+c2(-sin,cos)；第二列应为 (sin,cos)')

# ---------------------------------------------------------------- 例7
P('\n=== 例7 (课件 p33-p35) ===')
A7 = mat([[0, -4, 0], [1, -4, 0], [1, -2, -2]])
P('char poly =', sp.factor(A7.charpoly().as_expr()))
P('eigenvects =', A7.eigenvects())
N7 = A7 + 2*sp.eye(3)
P('N=A+2I =', N7.tolist(), ' N^2 =', (N7**2).tolist())
P('geometric multiplicity g = 3 - rank(N) =', 3 - N7.rank())
F7 = sp.exp(-2*x) * (sp.eye(3) + x*N7)
check_F('例7', A7, F7)
P('e^{A7 x} =', sp.simplify(F7).tolist())

# ---------------------------------------------------------------- 例8
P('\n=== 例8 (课件 p36-p38) ===')
A8 = mat([[0, 1, 0], [0, -2, -5], [0, 1, 2]])
P('char poly =', sp.factor(A8.charpoly().as_expr()))
P('A8^2 =', (A8**2).tolist())
F8 = sp.Matrix([[1, -2 + 2*sp.cos(x) + sp.sin(x), -5 + 5*sp.cos(x)],
                [0, sp.cos(x) - 2*sp.sin(x), -5*sp.sin(x)],
                [0, sp.sin(x), sp.cos(x) + 2*sp.sin(x)]])
check_F('例8', A8, F8)
P('按 alpha 形式：alpha2*x^2=1-cos x, alpha1*x=sin x, alpha0=1')
alpha2x2 = 1 - sp.cos(x); alpha1x = sp.sin(x); alpha0e = 1
F8b = sp.simplify(alpha2x2*(A8**2) + alpha1x*A8 + alpha0e*sp.eye(3))
check_F('例8(alpha形式)', A8, F8b)
P('p36 中间矩阵 (3,2) 项：printed -alpha1*x；应为 +alpha1*x（见上 A^2 与 A 的 (3,2)）')

# ---------------------------------------------------------------- 例6
P('\n=== 例6 (课件 p30-p31) 谱 5(三重), 2(单重) ===')
mu = sp.symbols('mu')
b0, b1, b2, b3 = sp.symbols('b0 b1 b2 b3')
r = b0 + b1*mu + b2*mu**2 + b3*mu**3
conds = [sp.Eq(r.subs(mu, 5), sp.exp(5*x)),
         sp.Eq(sp.diff(r, mu).subs(mu, 5), x*sp.exp(5*x)),
         sp.Eq(sp.diff(r, mu, 2).subs(mu, 5), x**2*sp.exp(5*x)),
         sp.Eq(r.subs(mu, 2), sp.exp(2*x))]
sol6 = sp.solve(conds, [b0, b1, b2, b3], dict=True)[0]
for k in (b0, b1, b2, b3):
    P(f'beta_{str(k)[1]} =', sp.simplify(sol6[k]))
# 等价的光滑 Hermite 形式
c = (sp.exp(5*x)*(1 - 3*x + sp.Rational(9,2)*x**2) - sp.exp(2*x))/27
rH = sp.exp(5*x)*(1 + x*(mu - 5) + sp.Rational(1,2)*x**2*(mu - 5)**2) + c*(mu - 5)**3
P('Hermite 形式 c(x) =', sp.simplify(c))
P('Hermite 形式与 beta 形式差 =', sp.simplify(sp.expand(rH - r.subs(sol6))))
P('rH(0,mu) =', sp.simplify(rH.subs(x, 0)))
for k in range(3):
    P(f'  d^{k}/dmu^{k} rH at 5 减 期望 =',
      sp.simplify(sp.diff(rH, mu, k).subs(mu, 5) - (x**k)*sp.exp(5*x)))
P('  rH(2) - e^{2x} =', sp.simplify(rH.subs(mu, 2) - sp.exp(2*x)))
# 具体实现 A=diag(J3(5),2)：用 Hermite 多项式评估，核验 F'=AF
J = sp.zeros(4, 4)
J[0, 0] = 5; J[0, 1] = 1; J[1, 1] = 5; J[1, 2] = 1; J[2, 2] = 5; J[3, 3] = 2
F6 = sp.zeros(4, 4)
for k, bk in enumerate([b0, b1, b2, b3]):
    F6 += sol6[bk] * (J**k)
check_F('例6 具体实现 diag(J3(5),2)', J, sp.simplify(F6))
P('该实现 e^{Ax} =', sp.simplify(F6).tolist())

# ---------------------------------------------------------------- 作业1-3
P('\n=== 作业1 ===')
H1 = mat([[-6, -4], [8, 6]])
P('eigenvalues =', H1.eigenvals(), ' A^2 =', (H1**2).tolist())
Fh1 = sp.simplify(sp.cosh(2*x)*sp.eye(2) + (sp.sinh(2*x)/2)*H1)
check_F('作业1', H1, Fh1)
P('e^{A x} =', Fh1.tolist())

P('\n=== 作业2 ===')
H2 = mat([[-4, 4], [-5, 4]])
P('eigenvalues =', H2.eigenvals(), ' A^2 =', (H2**2).tolist())
Fh2 = sp.simplify(sp.cos(2*x)*sp.eye(2) + (sp.sin(2*x)/2)*H2)
check_F('作业2', H2, Fh2)
P('e^{A x} =', Fh2.tolist())

P('\n=== 作业3 ===')
H3 = mat([[-24, 0, 0], [4, -2, 0], [1, 0, 2]])
P('eigenvalues =', H3.eigenvals())
g0, g1, g2 = sp.symbols('g0 g1 g2')
rg = g0 + g1*mu + g2*mu**2
solh3 = sp.solve([sp.Eq(rg.subs(mu, -24), sp.exp(-24*x)),
                  sp.Eq(rg.subs(mu, -2), sp.exp(-2*x)),
                  sp.Eq(rg.subs(mu, 2), sp.exp(2*x))], [g0, g1, g2], dict=True)[0]
for k in (g0, g1, g2):
    P(f'{k} =', sp.simplify(solh3[k]))
Fh3 = sp.simplify(solh3[g0]*sp.eye(3) + solh3[g1]*H3 + solh3[g2]*(H3**2))
check_F('作业3', H3, Fh3)
P('A^2 =', (H3**2).tolist())
P('e^{A x} =', Fh3.tolist())

# ---------------------------------------------------------------- 原课件疑点复算
P('\n=== 原课件 p14/p15/p27/p36 疑点复算 ===')
P('p14: V^-1 印刷 (1,2)=0；实际 V^-1(1,2) =', V1inv[0, 1])
X0 = sp.Matrix([1, 2, 3])
P('p15: 印刷 Y=V e^{Lambda x} V^-1 Y0，在 x0=1 的初值下不满足 Y(x0)=Y0：')
Yprint = V1 * sp.diag(sp.exp(2*x), sp.exp(x), sp.exp(-x)) * V1inv * X0
P('  Y(1)-Y0 =', sp.simplify(Yprint.subs(x, 1) - X0).tolist())
Yshift = V1 * sp.diag(sp.exp(2*(x-1)), sp.exp(x-1), sp.exp(-(x-1))) * V1inv * X0
P('  改用 e^{Lambda(x-x0)} 后 Y(1)-Y0 =', sp.simplify(Yshift.subs(x, 1) - X0).tolist())
P('p27: 印刷第二列 (-sin,cos)，但 e^{Ax} 第二列 =', F5[:, 1].tolist(),
  '；A*第二列应等于其导数')
P('p36: 中间矩阵 (3,2) 印刷 -alpha1*x；实际 =', sp.simplify((alpha1x*A8)[2, 1]),
  '（A32=1, (A^2)32=', (A8**2)[2, 1], '）')


def check_zero(name, value):
    simplified = sp.simplify(value)
    ok = (simplified.is_zero_matrix is True) if isinstance(simplified, sp.MatrixBase) else (simplified == 0)
    checks.append((name, bool(ok)))
    P(f'[{name}] residual zero: {bool(ok)}')
    if not ok:
        P('  residual =', simplified)

check_zero('例1 eigenvector factorization', V1*L1*V1inv-A1)
check_zero('例2 polynomial division', sp.expand(q2*Delta2+r2-p2))
check_zero('例2 matrix remainder', A2**4+3*A2**3+2*A2**2+A2+sp.eye(2)-(146*A2-184*sp.eye(2)))
for n in (2,3):
    nodes=sp.symbols('nu1:%d' % (n+1))
    vandermonde=sp.Matrix(n,n,lambda i,j:nodes[i]**j)
    determinant=sp.prod(nodes[j]-nodes[i] for i in range(n) for j in range(i+1,n))
    check_zero(f'例3 Vandermonde n={n} under distinct nodes', vandermonde.det()-determinant)
check_zero('例4 elimination', (eq1.lhs+2*eq2.lhs)-3*sol[a0s])
check_zero('例6 Hermite equals beta form', sp.expand(rH-r.subs(sol6)))
check_zero('例6 initial polynomial r_0(mu)=1', rH.subs(x,0)-1)
for order in range(3):
    check_zero(f'例6 Hermite derivative order {order}', sp.diff(rH,mu,order).subs(mu,5)-x**order*sp.exp(5*x))
check_zero('例6 Hermite at 2', rH.subs(mu,2)-sp.exp(2*x))
check_zero('例7 nilpotence', N7**2)
check_zero('作业3 eigenvector -24', H3*sp.Matrix([286,-52,-11])+24*sp.Matrix([286,-52,-11]))
check_zero('平移初值 at x0=1', Yshift.subs(x,1)-X0)
P('\n=== 结论 ===')
ok_all = all(ok for _,ok in checks)
P(f'汇总：{sum(ok for _,ok in checks)}/{len(checks)} 组核验通过；全部通过 = {ok_all}')
P('符号核验检验打印公式的代数一致性；适用前提、覆盖与页面阅读质量另行审查。')
Path(__file__).with_name('verify_output.txt').write_text('\n'.join(out)+'\n',encoding='utf-8')
Path(__file__).with_name('verify_results.json').write_text(json.dumps({'passed':ok_all,'checks':[{'name':name,'passed':ok} for name,ok in checks]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if ok_all else 1)
