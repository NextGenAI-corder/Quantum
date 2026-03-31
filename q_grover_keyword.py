# ============================================
# ファイル名  : q_grover_aqua_compatible.py
# 目的       : Groverアルゴリズムによる条件一致ビット列の探索。
# 処理内容   : PhaseOracleGateで条件に合うビット列に位相反転を与え、
#              GroverOperatorで振幅増幅を行い、条件一致パターンを抽出。
# 入力       : Oracle条件式（例：x0 AND NOT x1 AND x2）
# 出力       : 出現頻度が高いビット列＝条件一致候補
# 備考       : Qiskit Aqua廃止に伴いQiskit 2.2.3対応に書き直したコード
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseOracleGate, GroverOperator
from qiskit_aer import AerSimulator

# 問題の条件：x0 AND NOT x1 AND x2
expression = '(x0 & ~x1 & x2)'
oracle = PhaseOracleGate(expression)

oracle_circuit = QuantumCircuit(3)
oracle_circuit.append(oracle, range(3))

qc = QuantumCircuit(3, 3)
qc.append(oracle, range(3))
grover_op = GroverOperator(oracle_circuit)
qc.append(grover_op, range(3))
qc.measure(range(3), range(3))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()

print("Grover探索結果（最も頻出した解）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {bit}: {count}")