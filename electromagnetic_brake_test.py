# -*- coding: utf-8 -*-

import os
import serial
import time

def get_port():
    for file in os.listdir('/dev'):
        if 'tty.usbserial' in file:
            return '/dev/' + file

def set_serial(c):
    c.port = get_port()
    c.baudrate = 115200
    c.parity = 'E'
    c.stopbits = 1
    c.timeout = 0.01

def main():
    client = serial.Serial()
    set_serial(client)
    client.open()
    # -------- 開始 --------
    # クエリ作成
    q = b"\x00"
    # クエリ送信
    client.write(q)
    # 一定時間待機
    time.sleep(0.02)
    # レスポンス受信
    response = client.read(size=16)
    # 一定時間待機
    time.sleep(0.02)
    # レスポンス処理
    print(response)
    # -------- 終了 --------
    client.close()

if __name__ == "__name__":
    main()
