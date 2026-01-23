# ============================================
# ファイル名  : q_target_ads.py
# 改良内容   : ビット列を「年齢」「性別」「時間帯」に分解して人間が読める形で表示
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseOracleGate

oracle = PhaseOracleGate('(x0 & x1 & x2)')
qc = QuantumCircuit(3, 3)
qc.append(oracle, range(3))
qc.measure(range(3), range(3))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()

# 属性ラベル定義
age_map = {'0': '高齢', '1': '若年'}
gender_map = {'0': '男性', '1': '女性'}
time_map = {'0': '昼間', '1': '夜間'}

print("【ターゲット広告最適化】マッチしたユーザーパターン（出現回数）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    age = age_map[bit[2]]
    gender = gender_map[bit[1]]
    time = time_map[bit[0]]
    print(f"  {bit} → {age}・{gender}・{time}：{count} 回")
