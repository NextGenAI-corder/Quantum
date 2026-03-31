# ============================================
# ファイル名  : q_sensor_correlation.py
# 目的       : 複数センサの相関パターンをGrover探索で抽出。
# 処理内容   : センサA・B・CのON/OFF状態をビット列で表現し、
#              Oracle条件に一致するパターンを振幅増幅で強調抽出。
# 入力       : センサの相関条件（例：A=ON, B=ON, C=OFF）
# 出力       : 条件一致センサパターンの出現頻度（頻度順）
# ============================================

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseOracleGate, GroverOperator
from qiskit_aer import AerSimulator

# Oracle条件設定：センサA=1, B=1, C=0（ビット列: x2 x1 x0）
oracle = PhaseOracleGate('(x0 & x1 & ~x2)')

# 3量子ビット＋3古典ビットの回路を作成
qc = QuantumCircuit(3, 3)

# Oracleゲートを回路に適用（条件一致ビット列に位相反転）
qc.append(oracle, range(3))
oracle_circuit = QuantumCircuit(3)
oracle_circuit.append(oracle, range(3))
grover_op = GroverOperator(oracle_circuit)
qc.append(grover_op, range(3))

# すべての量子ビットを測定（結果を古典ビットに反映）
qc.measure(range(3), range(3))

# ローカルシミュレータで回路を1024回実行
sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()

# 出力結果を日本語で表示（センサA〜Cの状態をON/OFFでマッピング）
print("【センサ相関パターン抽出】マッチしたセンサ状態（頻度順）:")
for bit, count in sorted(counts.items(), key=lambda x: -x[1]):
    a, b, c = bit[2], bit[1], bit[0]
    a_state = "ON" if a == '1' else "OFF"
    b_state = "ON" if b == '1' else "OFF"
    c_state = "ON" if c == '1' else "OFF"
    print(f"  ビット列 {bit} → A:{a_state}・B:{b_state}・C:{c_state}：{count} 回")
    