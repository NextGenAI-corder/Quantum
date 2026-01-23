# ============================================
# ファイル名  : q_iot_qft.py
# 目的       : IoTセンサーログ（ON/OFF）から周期性をQFTで解析。
# 処理内容   : IoTデバイスのビットON履歴を量子回路に反映。
#              QFTで周期的なONパターンの成分を抽出。
# 入力       : 任意のONビットパターン（例: 0101 は x1, x3がON）
# 出力       : 周期的なパターン強度（ビット列の測定回数）
# 修正版     : QFT → QFTGate（非推奨回避）
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator

qc = QuantumCircuit(4, 4)

# 例：IoTログ 0101（センサー1と3がON）
qc.x(1)
qc.x(3)

# QFTGate で周期解析
qc.append(QFTGate(4), range(4))
qc.measure(range(4), range(4))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()

print("【IoT周期解析】QFT測定結果（ビット列 : 出現回数）")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {bit}: {count}")
