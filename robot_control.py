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

# スレーブ一覧
BROADCAST = b"\x00"
ANKLE_R = b"\x01"
ANKLE_L = b"\x02"
VERTICAL_SWING_R = b"\x03"
VERTICAL_SWING_L = b"\x04"
LATERAL_SWING_R = b"\x05"
LATERAL_SWING_L = b"\x06"

# モータードライバ一覧
slave_motors = [BROADCAST,
                ANKLE_R, ANKLE_L,
                VERTICAL_SWING_R, VERTICAL_SWING_L,
                LATERAL_SWING_R, LATERAL_SWING_L]

# 接続済みのモータードライバ一覧
"""
connected_slave_motors = [ANKLE_R,
                          ANKLE_L,
                          VERTICAL_SWING_R,
                          VERTICAL_SWING_L,
                          LATERAL_SWING_R,
                          LATERAL_SWING_L]

# 電磁ブレーキ有のモータードライバ一覧
electromagneticbrake = [VERTICAL_SWING_R,
                        VERTICAL_SWING_L,
                        LATERAL_SWING_R,
                        LATERAL_SWING_L]
"""

connected_slave_motors = [b"\x01", b"\x02"]
electromagneticbrake = [b"\x01"]

# 引数時間待機する
def standby(term=0.02):
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

# ダイレクトデータ運転のパラメータをセンサ値から決定する
def get_params(slave, sensor_values):
    # 固定
    function_code = b"\x10"
    head_address = b"\x00\x58"
    register_num = b"\x00\x10"
    byte_num = b"\x20"
    data_no = b"\x00\x00\x00\x00"

    current = b"\x00\x00\x03\xe8"
    trigger = b"\x00\x00\x00\x01"
    # センサ値から決定
    method = b"\x00\x00\x00\x02"
    position = b"\x00\x00\x21\x34"
    speed = b"\x00\x00\x07\xd0"
    start_rate = b"\x00\x00\x05\xdc"
    stop_rate = b"\x00\x00\x05\xdc"
    query = (slave + function_code + head_address + register_num + byte_num +
             data_no + method + position + speed + start_rate + stop_rate +
             current + trigger)
    query += crc_error_check(query)
    return query

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

# モータードライバへ送信するクエリのリストを作成する
def make_queries(sensor_values):
    # 必要な動作のみのクエリのリストを作成する
    queries = []
    for slave in connected_slave_motors:
        q = get_params(slave, sensor_values)
        # TODO: get_paramsで動作なしの場合は空文字を返すようにする
        if(q == b""):
            continue
        q += crc_error_check(q)
        queries.append(q)
    return queries

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
    """
    queries = [b"\x01\x06\x00\x7d\x00\x04\x18\x11",
               b"\x02\x06\x00\x7d\x00\x04\x18\x22",
               b"\x03\x06\x00\x7d\x00\x04\x19\xf3",
               b"\x04\x06\x00\x7d\x00\x04\x18\x44",
               b"\x05\x06\x00\x7d\x00\x04\x19\x95",
               b"\x06\x06\x00\x7d\x00\x04\x19\xa6"]
    """
    queries = [b"\x01\x06\x00\x7d\x00\x04\x18\x11"]
    write_queries_only(driver, queries)

# 全ての電磁ブレーキを保持する（C-ONをOFFにする）
def retain_all_brakes(driver):
    """
    queries = [b"\x01\x06\x00\x7d\x00\x00\x19\xd2",
               b"\x02\x06\x00\x7d\x00\x00\x19\xe1",
               b"\x03\x06\x00\x7d\x00\x00\x18\x30",
               b"\x04\x06\x00\x7d\x00\x00\x19\x87",
               b"\x05\x06\x00\x7d\x00\x00\x18\x56",
               b"\x06\x06\x00\x7d\x00\x00\x18\x65"]
    """
    queries = [b"\x01\x06\x00\x7d\x00\x00\x19\xd2"]
    write_queries_only(driver, queries)

# クエリリストを順次ドライバへ書き込む。レスポンスは廃棄
def write_queries_only(driver, queries):
    for q in queries:
        driver.write(q)
        response = b""
        while(not response):
            # レスポンスを受け取るまでループ
            response = driver.read(size=16)

# ダイレクトデータ運転
def direct_data_operation(driver, queries):
    write_queries_only(driver, queries)

# TODO: すべての運転完了まで待機
def wait_finishing_operation(driver):
    """
    queries = [b"\x01\x03\x00\x7f\x00\x01\xb5\xd2",
               b"\x02\x03\x00\x7f\x00\x01\xb5\xe1",
               b"\x03\x03\x00\x7f\x00\x01\xb4\x30",
               b"\x04\x03\x00\x7f\x00\x01\xb5\x87",
               b"\x05\x03\x00\x7f\x00\x01\xb4\x56",
               b"\x06\x03\x00\x7f\x00\x01\xb4\x65"]
    """
    queries = [b"\x01\x03\x00\x7f\x00\x01\xb5\xd2",
               b"\x02\x03\x00\x7f\x00\x01\xb5\xe1"]
    for q in queries:
        move = True
        while(move):
            # 要確認: 動作速くてクエリ送信に対してエラー吐きそう
            driver.write(q)
            response = b""
            while(not response):
                response = driver.read(size=16)
            debug_print(response)
            if(get_one_status(response, OutputStatus.MOVE) == 0):
                move = False

def main():
    debug_print("### START")
    driver = serial.Serial('/dev/tty.usbserial-FT1GOG9N', 115200,
                           parity='E', timeout=0.01)
    micro = serial.Serial(get_port_micro(), 19200)
    while(True):
        # Arduino初期化を待機
        if(micro.read() == b"\x99"):
            break
    debug_print("### ARDUINO READY")
    # ドライバ状態確認（準備完了までループ）
    for address in [b"\x02"]:
        query = remote_io_access(address)
        while(True):
            driver.write(query)
            standby()
            response = driver.read(size=16)
            ready = get_one_status(response, OutputStatus.READY)
            standby()
            if(ready):
                break
    debug_print("### MOTOR DRIVERS READY")
    # メインループ -------- -------- -------- --------
    loop_number = 0 # tmp: ループ回数を制限
    while(loop_number < 3):
        ## センサ値取得
        sensor_values = get_sensor_values(micro)
        ## TODO: 動作量を計算
        ### td: センサ値を元に動作量を出力しクエリを作成
        queries = make_queries(sensor_values)
        ## モーター動作
        ### 電磁ブレーキ操作
        #### 電磁ブレーキ状態確認 TODO: orしなくてもいい？
        #### 電磁ブレーキオフ(解放)
        release_all_brakes(driver)
        ### ダイレクトデータ運転
        direct_data_operation(driver, queries)
        ### 運転完了まで待機
        wait_finishing_operation(driver)
        ### 電磁ブレーキオン（保持）
        retain_all_brakes(driver)
        ## モーターが全て動作可能になるまで待機
        while(True):
            standby(1)  # tmp: 一周がわかるように1秒待機
            break
        loop_number += 1    # tmp
    # -------- -------- -------- -------- --------
    # 終了
    driver.close()
    micro.close()

if __name__ == "__main__":
    main()
