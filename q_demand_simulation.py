# ============================================
# ファイル名  : q_demand_simulation.py
# 目的       : 量子振幅により商品需要の確率傾向をシミュレーション。
# 処理内容   : 各商品の「売れる確率」をRyゲートで振幅に反映し、
#              測定によって売れやすい組合せ（ビット列）を抽出。
# 入力       : 各商品の需要傾向（角度で指定: 0〜π）
# 出力       : 出現頻度が高いビット列＝売れやすい商品パターン
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 3商品（A,B,C）の売れやすさを角度で設定（例: A高, B低, C中）
qc = QuantumCircuit(3, 3)
qc.ry(2.5, 0)  # 商品A：需要高め
qc.ry(0.8, 1)  # 商品B：需要低め
qc.ry(1.5, 2)  # 商品C：中間程度

# 全ての量子ビットを測定し、それぞれ古典ビットに対応づける
qc.measure(range(3), range(3))

# Aerシミュレータを初期化（ローカルで量子回路を模擬実行するバックエンド）
sim = AerSimulator()

# 回路をシミュレータ用に最適化（トランスパイル）し、1024回実行
result = sim.run(transpile(qc, sim), shots=1024).result()

# 測定結果（各ビット列の出現回数）を取得
counts = result.get_counts()

print("【商品需要シミュレーション結果】需要パターンと出現回数:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {bit}: {count}")
