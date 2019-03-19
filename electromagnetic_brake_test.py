# -*- coding: utf-8 -*-

import serial
import time

# ループ回数
NUM = 2
# 電磁ブレーキ待機時間
WAIT_ON = 0.14
WAIT_OFF = 0.05

# 回転が停止状態かを確認
def stop_rotation(ser, response):
    if(not (len(response) == 7)):
        ser.reset_input_buffer()
        return False
    status = (response[3] << 8) + response[4]
    move = (status >> 13) & 1
    if(move):
        return False
    else:
        return True

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
    ser = serial.Serial()
    ser.port = '/dev/tty.usbserial-FT1GOG9N'
    ser.baudrate = 115200
    ser.parity = serial.PARITY_EVEN
    ser.timeout = 0.01
    ser.open()
    # ---- ---- ---- ----
    # C-ONをON(電磁ブレーキを解放)
    q_release = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    # C-ONをOFF(電磁ブレーキを保持)
    q_keep = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    # 動作1
    q_dd1 = (b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01"
             + (1250).to_bytes(4, "big", signed=True)   # 位置
             + (50000).to_bytes(4, "big")               # 速度
             + (100000).to_bytes(4, "big")              # 起動・変速レート
             + (100000).to_bytes(4, "big")              # 停止レート
             + b"\x00\x00\x03\xe8\x00\x00\x00\x01")
    q_dd1 += crc_error_check(q_dd1)
    # 動作2
    q_dd2 = (b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01"
             + (-1250).to_bytes(4, "big", signed=True)  # 位置
             + (50000).to_bytes(4, "big")               # 速度
             + (100000).to_bytes(4, "big")              # 起動・変速レート
             + (100000).to_bytes(4, "big")              # 停止レート
             + b"\x00\x00\x03\xe8\x00\x00\x00\x01")
    q_dd2 += crc_error_check(q_dd2)
    # リモートI/Oアクセス
    q_rio = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"

    # メイン動作
    for i in range(NUM):
        ##### 電磁ブレーキを解放する
        ser.write(q_release)
        time.sleep(0.02)
        response = ser.read(16)
        time.sleep(0.02)
        print("電磁ブレーキ解放")

        time.sleep(WAIT_ON)

        ##### モーター動作
        if(i%2 == 0):
            ser.write(q_dd1)
        else:
            ser.write(q_dd2)
        time.sleep(0.02)
        response = ser.read(16)
        time.sleep(0.02)
        print("ダイレクトデータクエリ送信")
        while(True):
            print("動作待機中")
            ser.write(q_rio)
            time.sleep(0.02)
            response = ser.read(16)
            if(stop_rotation(ser, response)):
                break

        ##### 電磁ブレーキを保持する
        ser.write(q_keep)
        time.sleep(0.02)
        response = ser.read(16)
        time.sleep(0.02)
        print("電磁ブレーキ保持")

        time.sleep(WAIT_OFF)
    # ---- ---- ---- ----
    ser.close()

if __name__ == '__main__':
    main()
