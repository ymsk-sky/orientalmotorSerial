# -*- coding: utf-8 -*-

import serial
import time

def print_sensor_value(r):
    # r = b"\xFF\x11\x22\xEE"
    # ヘッダー, センサ値(上位), センサ値(下位), チェックサム
    pass

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
