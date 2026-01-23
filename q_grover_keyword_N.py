# ============================================
# ファイル名  : q_grover_keyword.py
# 目的       : Groverアルゴリズムで特定キーワード条件に合致する
#              ビット列パターンを高速に探索する
# 対応環境   : Qiskit v2.2.x 系
# ============================================

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, execute
from qiskit.circuit.library import PhaseOracle
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import CustomCircuitOracle
from qiskit.aqua import QuantumInstance

# 問題の条件：x0 AND NOT x1 AND x2
expression = '(x0 & ~x1 & x2)'
oracle = PhaseOracle(expression)

# Groverアルゴリズムの設定（古いAqua系）
backend = Aer.get_backend("qasm_simulator")
grover = Grover(oracle=oracle)
qi = QuantumInstance(backend=backend, shots=1024)
result = grover.run(qi)

# 結果表示
print("Grover探索結果（最も頻出した解）:", result["result"])
