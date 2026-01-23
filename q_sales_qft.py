# ============================================
# ファイル名  : q_sales_qft.py
# 目的       : 売上データ（CSV）を読み込み、一定の閾値で 1/0 に変換。
#              それを量子ビットの初期状態に反映し、量子フーリエ変換（QFT）を適用。
#              測定結果のビット列分布から、周期性の傾向を視覚的に分析する。
#
# 入力       : sales.csv（例: 日別売上データ, カラム: day, sales）
#              ※ 閾値（例：1000）を超える売上 → 1、それ未満 → 0 に変換。
#
# 処理内容   : 
#   - 売上データの2値変換（1 or 0）を反転順で量子ビットにXゲートでセット。
#   - QFTGateにより状態全体にフーリエ変換を適用。
#   - 全量子ビットを測定し、1024ショットで統計を取得。
#
# 測定結果   : 2ⁿ通り（n = ビット数）のビット列が出現し、その出現頻度（count）を出力。
#              特定ビット列の頻度が突出することで、周期的パターンの存在を示す。
#
# 出力       : 測定結果（コンソール）＋ ヒストグラム画像（qft_output_histogram.png）
# ============================================

import csv
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# --- 売上CSVを読み込み、売上が threshold 以上なら1、未満なら0に変換 ---
threshold = 1000
sales_bits = []

with open("sales.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sales = int(row["sales"])
        bit = 1 if sales >= threshold else 0
        sales_bits.append(bit)

# --- 量子回路構築：ビット列に応じて量子状態を |0⟩ or |1⟩ に設定 ---
n_qubits = len(sales_bits)
qc = QuantumCircuit(n_qubits, n_qubits)

for i, bit in enumerate(reversed(sales_bits)):  # Qiskitは逆順配置
    if bit == 1:
        qc.x(i)

# --- QFTゲートを適用 ---
qc.append(QFTGate(n_qubits), range(n_qubits))

# --- 測定追加 ---
qc.measure(range(n_qubits), range(n_qubits))

# --- シミュレーション実行 ---
backend = AerSimulator()
compiled = transpile(qc, backend)
job = backend.run(compiled, shots=1024)
result = job.result()
counts = result.get_counts()

# --- 測定結果を表示 ---
print("QFT測定結果 (bitstring : count)")
for bit, count in sorted(counts.items()):
    print(f"  {bit}: {count}")

# --- ヒストグラム保存（タイトルはASCIIのみに限定） ---
fig = plot_histogram(counts)
plt.title("QFT Distribution from Sales Data")
fig.savefig("qft_output_histogram.png")
print("Saved: qft_output_histogram.png")

