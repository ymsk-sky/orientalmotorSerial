# -*- coding: utf-8 -*-

import serial
from time import sleep

def main():
    ser = serial.Serial("/dev/tty.usbserial-FT1GOG9N", 115200,
                        parity='E', timeout=0.01)
    release_query = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    retain_query = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    remote_io_access_query = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"

    ser.write(release_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    print(response)

    ser.write(retain_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    

if __name__ == "__main__":
    main()


"""
1. 電磁ブレーキをOFFにする（C-ONをONにする）
2. リモートI/Oを確認する
    a. READY, MOVEを確認する
    b. MBCを確認する
3. ダイレクトデータ運転する
"""
