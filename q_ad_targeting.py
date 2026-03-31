# ============================================
# ファイル名  : q_ad_targeting.py
# 目的       : Web広告の配信条件（属性・時間・環境など）に対し、
#              最も反応率が高い組合せを量子的に探索。
# 処理内容   : 条件をビット論理式で定義し、Grover的Oracleで抽出。
# 入力       : 条件論理式（例: 若年×スマホ×夜間 = x0 & x1 & x2）
# 出力       : 該当するビット列（ターゲット属性の組合せ）
# ============================================
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseOracleGate, GroverOperator
from qiskit_aer import AerSimulator

# Oracle条件を定義
# x0=1（若年）かつ x1=1（スマホ）かつ x2=1（夜間）
# → 理想的な広告ターゲット条件に合致するビット列に印を付ける
oracle = PhaseOracleGate('(x0 & x1 & x2)')

# 3量子ビット＋3古典ビットの量子回路を作成
qc = QuantumCircuit(3, 3)

# Oracleゲートを回路に追加
# 条件に一致する量子状態に位相反転を与える
qc.append(oracle, range(3))
oracle_circuit = QuantumCircuit(3)
oracle_circuit.append(oracle, range(3))
grover_op = GroverOperator(oracle_circuit)
qc.append(grover_op, range(3))

# 量子状態を測定し、結果を古典ビットに格納
qc.measure(range(3), range(3))

# ローカル量子回路シミュレータを初期化
sim = AerSimulator()

# 回路をシミュレータ用に最適化し、1024回実行
result = sim.run(transpile(qc, sim), shots=1024).result()

# 測定結果（各ビット列の出現回数）を取得
counts = result.get_counts()

# 各ビットの意味を人間が理解しやすいラベルに対応付け
labels = {
    'x0': ['高齢', '若年'],    # 年齢属性
    'x1': ['PC', 'スマホ'],    # 利用デバイス
    'x2': ['昼間', '夜間']     # 利用時間帯
}
# 結果表示：ビット列 → 属性 → 出現回数　※条件に完全一致した場合は「ターゲット一致」と明示
print("【Web広告ターゲティング最適化】出現条件（ビット列・属性・出現回数）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    attrs = [labels[f'x{i}'][int(b)] for i, b in enumerate(reversed(bit))]
    match_note = " ← ターゲット一致" if bit == "111" else ""
    print(f"  {bit} → {'・'.join(attrs)}：{count} 回{match_note}")
