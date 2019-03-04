# -*- coding: utf-8 -*-

import serial
from time import sleep

def main():
    ser = serial.Serial("/dev/tty.usbserial-FT1GOG9N", 115200,
                        parity='E', timeout=0.01)
    release_query = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    retain_query = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    remote_io_access_query = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
    direct_data_query = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08"

    print("start")
    ser.write(release_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    print("released")

    """
    sleep(2)
    ser.write(remote_io_access_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    print(response)
    sleep(2)
    """
    sleep(0.05)

    print("direct data operation")
    ser.write(direct_data_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    print("waiting movement")
    while(True):
        ser.write(remote_io_access_query)
        response = b""
        while(not response):
            # ser.reset_input_buffer()
            response = ser.read(16)
        if(not (len(response) == 7)):
            ser.reset_input_buffer()
            print("To continue because response length is too short.")
            print(response)
            continue
        status = (response[3] << 8) + response[4]
        move = (status >> 13) & 1
        if(not move):
            break
    print("finish movement")

    print("will retain")
    ser.write(retain_query)
    sleep(0.02)
    response = ser.read(16)
    sleep(0.02)
    print("finish")


if __name__ == "__main__":
    main()


"""
1. 電磁ブレーキをOFFにする（C-ONをONにする）
2. リモートI/Oを確認する
    a. READY, MOVEを確認する
    b. MBCを確認する
3. ダイレクトデータ運転する
"""
