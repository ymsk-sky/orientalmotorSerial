# -*- coding: utf-8 -*-

import serial
import time

def print_sensor_value(response):
    # r = b"\xFF\x11\x22\xEE"
    # ヘッダー, センサ値(上位), センサ値(下位), チェックサム
    # センサ値は1ビット左シフトしているため元に戻す必要がある
    # マイナス値の場合桁あふれでエラーになりそう
    SENSOR_NUM = 1
    head = response[0]
    if(head != 0xFF):
        # ヘッダが異なる
        return
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
        ser.write("\xFF")
        time.sleep(0.1)
        response = ser.read(16)
        print_sensor_value(response)
        time.sleep(0.5)
    ser.close()

if __name__ == "__main__":
    main()
