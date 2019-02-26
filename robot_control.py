# -*- coding: utf-8 -*-

import os
import serial
from time import sleep

# 使用するセンサ数
SENSOR_NUM = 2

# プリントデバッグするときはこの関数を使う
def debug_print(*text):
    for t in text:
        print(t)
        # pass

class OutputStatus():
    # ドライバ出力状態一覧（ハイフンはアンダースコアに置換）
    M0_R = 0        # R-OUT0
    M1_R = 1        # R-OUT1
    M2_R = 2        # R-OUT2
    START_R = 3     # R-OUT3
    HOME_END = 4    # R-OUT4
    READY = 5       # R-OUT5
    INFO = 6        # R-OUT6
    ALM_A = 7       # R-OUT7
    SYS_BSY = 8     # R-OUT8
    AREA0 = 9       # R-OUT9
    AREA1 = 10      # R-OUT10
    AREA2 = 11      # R-OUT11
    TIM = 12        # R-OUT12
    MOVE = 13       # R-OUT13
    IN_POS = 14     # R-OUT14
    TLC = 15        # R-OUT15

class SlaveMotor():
    # スレーブ一覧
    BROADCAST = 0
    ANKLE_R = 1
    ANKLE_L = 2
    VERTICAL_SWING_R = 3
    VERTICAL_SWING_L = 4
    LATERAL_SWING_R = 5
    LATERAL_SWING_L = 6

# モータードライバ一覧
slave_motors = [b"\x00", b"\x01", b"\x02", b"\x03", b"\x04", b"\x05", b"\x06"]
# 接続済みのモータードライバ一覧
connected_slave_motors = [slave_motors[SlaveMotor.ANKLE_R],
                          slave_motors[SlaveMotor.ANKLE_L]]
# TODO: 電磁ブレーキ有のモータードライバ一覧
electromagneticbrake = [slave_motors[SlaveMotor.ANKLE_R]]

# 引数時間待機する
def standby(term=0.06):
    # 初期値はクエリ送信後にレスポンスを受信可能になるまで待機する時間
    sleep(term)

# マイコンのポートを取得する
def get_port_micro():
    for file in os.listdir('/dev'):
        if 'tty.usbmodem' in file:
            return '/dev/' + file

# マイコンに接続されたセンサ値を取得する
## TODO: エラー発生の可能性(try囲み)
def get_sensor_values(micro):
    ## センサに要求クエリを送信する
    micro.write(b"\x00")
    response = b""
    while(len(response) < (2 + SENSOR_NUM*2)):
        response += micro.read()
    # ヘッダ確認
    head = response[0]
    if(head != 0xFF):
        print("head error")
        return
    # チェックサム確認
    checksum = 0
    for i in range(SENSOR_NUM):
        checksum += response[1+2*i] + response[2+2*i]
    checksum &= 0xFF
    if(checksum != response[-1]):
        print("checksum error")
        return
    # センサ値の取り出し処理
    values = []
    for i in range(SENSOR_NUM):
        higher = response[1+2*i]
        lower = response[2+2*i]
        value = (higher << 8) + lower
        values.append(s16(value))
    return values

# 2の補数表現を変換
def s16(value):
    return -(value & 0b1000000000000000) | (value & 0b0111111111111111)

# リモートI/Oの状態を一つ返す
def get_one_status(response, bit_number):
    driver_output = (response[3] << 8) + response[4]
    return (driver_output >> bit_number) & 1

# リモートI/Oへのアクセス
def remote_io_access(address):
    query = address + b"\x03" + b"\x00\x7f\x00\x01"
    query += crc_error_check(query)
    return query

# CRC-16/Modbusによるエラーチェック
def crc_error_check(query):
    crc_register = 0xFFFF
    for data_byte in query:
        crc_register ^= data_byte
        for _ in range(8):
            overflow = crc_register & 1 == 1
            crc_register >>= 1
            if overflow:
                crc_register ^= 0xA001
    # 結果は(上位→下位)の順
    return crc_register.to_bytes(2, 'little')

# TODO: 実装
def make_query(sensor_values):
    pass

# 電磁ブレーキの解放（C-ONをONにする）
def release_brake(driver, slave):
    query = slave + b"\x06\x00\x7d\x00\x04"
    query += crc_error_check(query)
    driver.write(query)
    response = b""
    while(not response):
        response = driver.read(size=16)

# 全ての電磁ブレーキを解放する（C-ONをONにする）
def release_all_brakes(driver):
    query = [b"\x01\x06\x00\x7d\x00\x04\x18\x11",
             b"\x02\x06\x00\x7d\x00\x04\x18\x22",
             b"\x03\x06\x00\x7d\x00\x04\x19\xf3",
             b"\x04\x06\x00\x7d\x00\x04\x18\x44"]
    write_queries_only(driver, query)

# 全ての電磁ブレーキを保持する（C-ONをOFFにする）
def retain_all_brakes(driver):
    query = [b"\x01\x06\x00\x7d\x00\x00\x19\xd2",
             b"\x02\x06\x00\x7d\x00\x00\x19\xe1",
             b"\x03\x06\x00\x7d\x00\x00\x18\x30",
             b"\x04\x06\x00\x7d\x00\x00\x19\x87"]
    write_queries_only(driver, query)

# クエリリストを順次ドライバへ書き込む。レスポンスは廃棄
def write_queries_only(driver, query):
    for q in query:
        driver.write(q)
        response = b""
        while(not response):
            # レスポンスを受け取るまでループ
            response = driver.read(size=16)

def main():
    debug_print("### START")
    driver = serial.Serial('/dev/tty.usbserial-FT1GOG9N', 115200,
                           parity='E', timeout=0.01)
    micro = serial.Serial(get_port_micro(), 19200)
    while(True):
        # Arduino初期化を待機
        if(micro.read() == b"\x99"):
            break;
    debug_print("### ARDUINO READY")
    # ドライバ状態確認（準備完了までループ）
    for address in connected_slave_motors:
        query = remote_io_access(address)
        while(True):
            driver.write(query)
            standby()
            response = driver.read(size=16)
            ready = get_one_status(response, OutputSatus.READY)
            standby()
            if(ready):
                break
    debug_print("### MOTOR DRIVERS READY")
    # メインループ -------- -------- -------- --------
    while(True):
        ## センサ値取得
        sensor_values = get_sensor_values(micro)
        ## TODO: 動作量を計算
        ### td: センサ値を元に動作量を出力しクエリを作成
        queries = make_query(sensor_values) # 未実装
        ## モーター動作
        ### 電磁ブレーキ操作
        #### 電磁ブレーキ有のモーターのみ動作
        for t in electromagneticbrake:
            #### 電磁ブレーキ状態確認
            #### 電磁ブレーキオフ(解放)
            release_brake(driver, t) # クエリは固定なのでエラーチェックも書き出しておく
            pass
        ### ダイレクトデータ運転（共通）
        direct_data_operation()
        ### 運転完了まで待機
        while(True):
            break
        ### 電磁ブレーキオン
        if(electromagnetic[i]):
            pass
        ## モーターが全て動作可能になるまで待機
        while(True):
            break
    # -------- -------- -------- -------- --------
    # 終了
    driver.close()
    micro.close()

if __name__ == "__main__":
    main()
