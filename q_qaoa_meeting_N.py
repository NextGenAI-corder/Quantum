# ファイル名: q_qaoa_meeting.py
# QAOAで会議スケジュールを最適化（Aer不要版）

from qiskit_aer import AerSimulator
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QAOA
from qiskit.optimization.problems import QuadraticProgram
from qiskit.optimization.algorithms import MinimumEigenOptimizer

qp = QuadraticProgram()
qp.binary_var('x0')
qp.binary_var('x1')
qp.binary_var('x2')
qp.minimize(linear=[0, 0, 0], quadratic={(0, 1): 1, (1, 2): 1, (0, 2): 1})

qi = QuantumInstance(backend=AerSimulator())
qaoa = QAOA(quantum_instance=qi)
result = MinimumEigenOptimizer(qaoa).solve(qp)

print("最適スケジュール:", result.x)
