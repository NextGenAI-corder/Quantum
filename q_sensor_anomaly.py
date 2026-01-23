# ============================================
# ファイル名  : q_sensor_anomaly.py
# 目的       : QFTを使ってセンサーデータの周期異常を検出。
# 処理内容   : 定常センサ値（正常パターン）に対して、
#              突然変異（異常値）をビットで注入し、QFTで解析。
# 入力       : 3ビットの異常パターン（例: x0, x2 が異常）
# 出力       : 異常の周期的特徴を持つビット列の測定分布
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator

# 3量子ビット＋3古典ビットの量子回路を生成
# 各量子ビットは1つのセンサーを表す
qc = QuantumCircuit(3, 3)

# センサー異常を初期状態として注入
# センサー0とセンサー2が異常（ON=1）という想定
qc.x(0)  # センサー0が異常状態
qc.x(2)  # センサー2が異常状態

# 量子フーリエ変換（QFTGate）を適用
# センサーデータ全体の周期構造を一斉に解析する
qc.append(QFTGate(3), range(3))

# 量子状態を測定し、結果を古典ビットに格納
qc.measure(range(3), range(3))

# ローカル量子回路シミュレータを初期化
sim = AerSimulator()

# 回路をシミュレータ向けに最適化（トランスパイル）し、
# 1024回のショットで測定を実行
result = sim.run(transpile(qc, sim), shots=1024).result()

# 測定結果（ビット列ごとの出現回数）を取得
counts = result.get_counts()

# 出現頻度の高い順に結果を表示
# 周期的に現れやすいビット列が「異常パターン候補」
print("【センサーデータ異常検出】QFT測定結果（ビット列 : 回数）")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {bit}: {count}")
