# ModbusによるPLC経由でのモータ制御
オリエンタルモーターAZシリーズをシリアルで動作させる。


# ModbusTest.py
コピペしました。
Qiita [Modbusを使ってPLC経由でモータを制御する](https://qiita.com/ToyoshiMorioka/items/8f92121f6bf6b9b6d9a0)

## 使い方
1. git clone
2. pip install pyserial
3. python ModbusTest.py

COMポートは都度書き換えること。

# ダイレクトデータ運転
通常運転より操作できるパラメータが少ないが、書き込みと同時に動作開始する。
パラメータは以下の7項目。
- データNo.
- 方式
- 位置
- 速度
- 起動・変速レート
- 停止レート
- 運転電流

# ドライバ出力状態
ドライバI/Oの出力状態をModbus通信でアクセスできる。
