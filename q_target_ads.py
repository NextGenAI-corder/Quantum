# ============================================
# ファイル名  : q_target_ad_optimize.py
# 目的       : Grover探索によるターゲット広告条件の最適化。
# 処理内容   : ユーザー属性（年齢・性別・時間帯）をビット列で表現し、
#              Oracle条件に一致するパターンを振幅増幅で強調抽出。
# 入力       : ターゲット条件（例：夜間・女性・若年）
# 出力       : 条件一致ユーザーパターンの出現頻度（頻度順）
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseOracleGate, GroverOperator

# Oracle条件設定：x0=1（夜間）かつ x1=1（女性）かつ x2=1（若年）
oracle = PhaseOracleGate('(x0 & x1 & x2)')

# 3量子ビット＋3古典ビットで回路を構築
qc = QuantumCircuit(3, 3)
qc.append(oracle, range(3)) # Oracleゲートを適用（条件に合うビット列に印）
oracle_circuit = QuantumCircuit(3)
oracle_circuit.append(oracle, range(3))
grover_op = GroverOperator(oracle_circuit)
qc.append(grover_op, range(3))
qc.measure(range(3), range(3)) # 全量子ビットを測定

# シミュレータ初期化＋回路の実行（1024回測定）
sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()

# 各ビットの意味を可読なラベルに変換する辞書を定義
age_map = {'0': '高齢', '1': '若年'}
gender_map = {'0': '男性', '1': '女性'}
time_map = {'0': '昼間', '1': '夜間'}

# 結果表示：人間が理解出来るように変換して出力
print("【ターゲット広告最適化】マッチしたユーザーパターン（出現回数）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    age = age_map[bit[2]]
    gender = gender_map[bit[1]]
    time = time_map[bit[0]]
    print(f" {bit} → {age}・{gender}・{time}：{count} 回")