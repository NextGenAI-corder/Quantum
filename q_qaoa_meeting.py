# ============================================
# ファイル名  : q_qaoa_schedule.py
# 目的       : QAOAによる組合せ最適化（スケジューリング問題）。
# 処理内容   : 2値変数の組合せコストを最小化する条件を定義し、
#              QAOAで最適な変数の組合せ（スケジュール）を探索。
# 入力       : 2値変数x0,x1,x2の組合せコスト（二次計画問題）
# 出力       : コストが最小となる変数の組合せ
# 備考       : Qiskit Aqua廃止に伴いQiskit 2.2.3対応に書き直したコード
# ============================================

from qiskit_aer.primitives import Sampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.problems import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

qp = QuadraticProgram()
qp.binary_var('x0')
qp.binary_var('x1')
qp.binary_var('x2')
qp.minimize(linear=[0, 0, 0], quadratic={(0, 1): 1, (1, 2): 1, (0, 2): 1})

sampler = Sampler()
qaoa = QAOA(sampler=sampler, optimizer=COBYLA())
result = MinimumEigenOptimizer(qaoa).solve(qp)

print("最適スケジュール:", result.x)