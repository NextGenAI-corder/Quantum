# ============================================
# ファイル名  : q_tsp_simple.py
# 目的       : 巡回セールスマン問題（TSP）を量子的に近似解く。
# 処理内容   : 最短経路と仮定するビット条件を論理式で定義し、
#              OracleGateを回路に適用、測定により該当ビット列を検出。
# 入力       : 論理式 (例: x0 & ~x1 & x2) ← 最短経路に相当する条件
# 出力       : 最も測定回数の多いビット列（最短経路の候補）
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseOracleGate

# Oracle条件を定義（巡回経路が特定条件を満たすビット列に印を付ける）
oracle_gate = PhaseOracleGate('(x0 & ~x1 & x2)')

# 3量子ビット＋3古典ビットの量子回路を生成
qc = QuantumCircuit(3, 3)

# Oracleゲートを回路に追加（条件に合う経路に位相反転を与える）
qc.append(oracle_gate, range(3))

# 測定：量子ビットを古典ビットに写す
qc.measure(range(3), range(3))

# ローカルシミュレータを設定し、回路を1024回実行
sim = AerSimulator()
res = sim.run(transpile(qc, sim), shots=1024).result()

# 測定結果（ビット列の出現頻度）を取得
counts = res.get_counts()

# 結果表示：特定の巡回経路（ビット列）の出現回数を表示
print("【TSP量子探索結果】最短ルートに該当するビット列とその出現回数:")
for bit, count in sorted(counts.items()):
    print(f"  {bit}: {count}")
