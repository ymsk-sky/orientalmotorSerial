# -*- coding: utf-8 -*-

##### ダイレクトデータ運転 運転データNo.
DATA_NO_DEFAULT = 0
DATA_NO_MIN = 0
DATA_NO_MAX = 255

##### ダイレクトデータ運転 方式一覧
### 値: from 0 to 22 except 4,5,6,19
# 設定なし
NO_SETTING = 0
# 絶対位置決め
ABSOLUTE_POSITION = 1
# 相対位置決め（指令位置基準）
RELATIVE_POSITION_BASED_ON_ORDER_POSITION = 2
# 相対位置決め（検出位置基準）
RELATIVE_POSITION_BASED_ON_DETECT_POSITION = 3
# 連続運転（位置制御）
CONTINUES_OPERATION = 7
# ラウンド絶対位置決め
ROUND_ABUSOLUTE_POSITION_ODER = 8
# ラウンド近回り位置決め
ROUND_NEAR_POSITION_ODER = 9
# ラウンドFWD方向絶対位置決め
ROUND_FORWARD_ABUSOLUTE_POSITION_ODER = 10
# ラウンドRVS方向絶対位置決め
ROUND_REVERSE_ABUSOLUTE_POSITION_ODER = 11
# ラウンド絶対押し当て
ROUND_ABUSOLUTE_PRESS = 12
# ラウンド近回り押し当て
ROUND_NEAR_PRESS = 13
# ラウンドFWD方向押し当て
ROUND_FORWARD_PRESS = 14
# ラウンドRVS方向押し当て
ROUND_REBERSE_PRESS = 15
# 連続運転（速度制御）
CONTINUES_OPERATION_WITH_SPEED = 16
# 連続運転（押し当て）
CONTINUES_OPERATION_WITH_PRESS = 17
# 連続運転（トルク）
CONTINUES_OPERATION_WITH_TORQUE = 18
# 絶対位置決め押し当て
ABUSOLUTE_POSITION_PRESS = 20
# 相対位置決め押し当て（指令位置基準）
RELATIVE_POSITION_WITH_ORDER_POSITION = 21
# 相対位置決め押し当て（検出位置基準）
RELATIVE_POSITION_WITH_DETECT_POSITION = 22

##### ダイレクトデータ運転 位置
# [step]
POSITION_DEFAULT = 0
POSITION_MIN = -2147483648
POSITION_MAX = 2147483648

##### ダイレクトデータ運転 速度
# [Hz]
SPEED_DEFAULT = 1000
SPEED_MIN = -4000000
SPEED_MAX = 4000000

##### ダイレクトデータ運転 起動・変速レート
# 1 = 0.001[kHz/s], 0.001[s], 0.001[ms/kHz]
START_SHIFT_RATE_DEFAULT = 1000000
START_SHIFT_RATE_MIN = 1
START_SHITF_RATE_MAX = 1000000000

##### ダイレクトデータ運転 停止レート
# 1 = 0.001[kHz/s], 0.001[s], 0.001[ms/kHz]
STOP_RATE_DEFAULT = 1000000
STOP_RATE_MIN = 1
STOP_RATE_MAX = 1000000000

##### ダイレクトデータ運転 運転電流
# 1 = 0.1[%]
CURRENT_DEFAULT = 1000
CURRENT_MIN = 0
CURRENT_MAX = 1000

##### ダイレクトデータ運転 反映トリガ
# -7: 運転データNo.
# -6: 方式
# -5: 位置
# -4: 速度
# -3: 起動・変速レート
# -2: 停止レート
# -1: 運転電流
# 0: 無効
# 1: 全データ反映
### マイナス値はF埋めする
### 例）-1→FFFF FFFF, -2→FFFF FFFE
TRIGGER_DEFAULT = 0
TRIGGER_MIN = -7
TRIGGER_MAX = 1

##### ダイレクトデータ運転 転送先
# 0: 実行メモリ
# 1: バッファメモリ
TRANSFER_DEFAULT = 0
TRANSFER_MIN = 0
TRANSFER_MAX = 1

##### リモートI/O
### 入力信号(ハイフンはアンダースコアに置換)
M0 = 0          # R-IN0
M1 = 1          # R-IN1
M2 = 2          # R-IN2
START = 3       # R-IN3
ZHOME = 4       # R-IN4
STOP = 5        # R-IN5
FREE = 6        # R-IN6
ALM_RST = 7     # R-IN7
D_SEL0 = 8      # R-IN8
D_SEL1 = 9      # R-IN9
D_SEL2 = 10     # R-IN10
SSTART = 11     # R-IN11
FW_JOG_P = 12   # R-IN12
RV_JOG_P = 13   # R-IN13
FW_POS = 14     # R-IN14
RV_POS = 15     # R-IN15
