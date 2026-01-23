# ============================================
# ファイル名  : q_sensor_grover.py
# 改良内容   : ビット列をセンサA〜Cの状態に変換し、日本語で可視化
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseOracleGate
from qiskit_aer import AerSimulator

# 条件：センサA=ON, B=ON, C=OFF を探す
oracle = PhaseOracleGate('(x0 & x1 & ~x2)')

qc = QuantumCircuit(3, 3)
qc.append(oracle, range(3))
qc.measure(range(3), range(3))

sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()

print("【センサ相関パターン抽出】マッチしたセンサ状態（頻度順）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    a, b, c = bit[2], bit[1], bit[0]
    a_state = "ON" if a == '1' else "OFF"
    b_state = "ON" if b == '1' else "OFF"
    c_state = "ON" if c == '1' else "OFF"
    print(f"  ビット列 {bit} → A:{a_state}・B:{b_state}・C:{c_state}：{count} 回")
