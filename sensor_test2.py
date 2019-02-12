# -*- coding: utf-8 -*-

import serial
import time

SENSOR_NUM = 1

def print_sensor_value(response):
    # r = b"\xFF\x11\x22\xEE"
    # ヘッダー, センサ値(上位), センサ値(下位), チェックサム
    # センサ値は1ビット左シフトしているため元に戻す必要がある
    # マイナス値の場合桁あふれでエラーになりそう

    # ヘッダ確認
    head = response[0]
    if(head != 0xFF):
        # ヘッダが異なる
        return
    # チェックサム確認
    checksum = 0
    for x in range(SENSOR_NUM):
        checksum += response[1+2*x] + response[2+2*x]
    if(checksum != response[-1]):
        # チェックサムが異なる
        return
    # 処理
    for i in range(SENSOR_NUM):
        higher = response[1+2*i]   # 1, 3, 5, 7, ...
        lower = response[2+2*i]    # 2, 4, 6, 8, ...
        value = (higher << 8) + lower
        print(value)

def main():
    ser = serial.Serial()
    ser.port = "/dev/tty.usbmodem1421"
    ser.baudrate = 19200
    ser.timeout = 0.01
    ser.open()

    while(ser.read() != b"\x99"):
        pass
    print("### ARDUINO IS READY ###")
    while(True):
        ser.write("\x00")
        time.sleep(0.1)
        response = ser.read(2+SENSOR_NUM)
        print_sensor_value(response)
        time.sleep(0.5)
    ser.close()

if __name__ == "__main__":
    main()
