# ============================================
# ファイル名  : q_ad_targeting.py
# 目的       : Web広告の配信条件（属性・時間・環境など）に対し、
#              最も反応率が高い組合せを量子的に探索。
# 処理内容   : 条件をビット論理式で定義し、Grover的Oracleで抽出。
# 入力       : 条件論理式（例: 若年×スマホ×夜間 = x0 & x1 & x2）
# 出力       : 該当するビット列（ターゲット属性の組合せ）
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseOracleGate
from qiskit_aer import AerSimulator

# 条件：若年・スマホ・夜間（理想ターゲット）
oracle = PhaseOracleGate('(x0 & x1 & x2)')

qc = QuantumCircuit(3, 3)
qc.append(oracle, range(3))
qc.measure(range(3), range(3))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()

# 属性表示（シンプル）
labels = {
    'x0': ['高齢', '若年'],
    'x1': ['PC', 'スマホ'],
    'x2': ['昼間', '夜間']
}

print("【Web広告ターゲティング最適化】出現条件（ビット列・属性・出現回数）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    attrs = [labels[f'x{i}'][int(b)] for i, b in enumerate(reversed(bit))]
    match_note = " ← ターゲット一致" if bit == "111" else ""
    print(f"  {bit} → {'・'.join(attrs)}：{count} 回{match_note}")
