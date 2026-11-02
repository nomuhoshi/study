"""一维简谐振子能级的有限差分数值解（取 hbar = m = omega = 1）。

理论值：E_n = n + 1/2。
运行：python3 01_harmonic_oscillator.py   （需要 numpy：pip install numpy）
练习：把势能换成 x**4 或无限深方势阱，先预测能级怎么变，再运行验证。
"""
import numpy as np

# 1. 空间网格：在 [-5, 5] 上取 1000 个点
N = 1000
L = 10.0
x = np.linspace(-L / 2, L / 2, N)
dx = x[1] - x[0]

# 2. 势能 V(x) = x^2 / 2
V = 0.5 * x**2

# 3. 哈密顿量 H = -1/2 d²/dx² + V
#    二阶导数用有限差分：(ψ[i+1] - 2ψ[i] + ψ[i-1]) / dx²
main_diag = 1.0 / dx**2 + V                 # 对角元
off_diag = -0.5 / dx**2 * np.ones(N - 1)    # 次对角元
H = np.diag(main_diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)

# 4. 求本征值（H 是实对称矩阵，用 eigvalsh）
energies = np.linalg.eigvalsh(H)[:5]

# 5. 和理论值比较
for n, E in enumerate(energies):
    print(f"n={n}: 数值 E={E:.5f}，理论 E={n + 0.5:.1f}，误差={abs(E - (n + 0.5)):.2e}")
