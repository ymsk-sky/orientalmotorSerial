# -*- coding: utf-8 -*-

import os
import serial
from time import sleep

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

# マイコンのポートを取得する
def get_port_micro():
    for file in os.listdir('/dev'):
        if 'tty.usbmodem' in file:
            return '/dev/' + file

# 引数時間待機する
def standby(term=0.06):
    # 初期値はクエリ送信後にレスポンスを受信可能になるまで待機する時間
    sleep(term)

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
    return crc_register.to_bytes(2, 'little')

def main():
    driver = serial.Serial('/dev/tty.usbserial-FT1GOG9N', 115200,
                           parity='E', timeout=0.01)
    micro = serial.Serial(get_port_micro(), 19200)
    standby(2)  # Arduino初期化を待機
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
    # メインループ -------- -------- -------- --------
    while(True):
        ## センサ値取得
        ## TODO: 動作量を計算
        ## モーター動作
        ## モーターが全て動作可能になるまで待機
        pass
    # -------- -------- -------- -------- --------
    # 終了
    driver.close()
    micro.close()

if __name__ == "__main__":
    main()
