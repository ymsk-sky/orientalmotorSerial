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
    c.bytesize = 8
    c.parity = 'E'
    c.stopbits = 1
    c.timeout = 0.01

def mbc_status(r):
    return (((r[3] << 8) + r[4]) >> 9) & 1

def move_status(r):
    return (((r[3] << 8) + r[4]) >> 13) & 1

def main():
    client = serial.Serial()
    set_serial(client)
    client.open()
    # -------- 開始 --------
    # クエリ作成
    ## MBC(電磁ブレーキの状態)読み出し
    q_mbc = b"\x01\x03\x01\x7b\x00\x01\xf5\xef"
    ## C-ONをON = 電磁ブレーキを解放
    q_release = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    ## C-ONをOFF = 電磁ブレーキを保持
    q_keep = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    ## ダイレクトデータ運転（例）
    q_direct = b"\x01\x10\x00\x58\x00\x10\x20\
                 \x00\x00\x00\x00\x00\x00\x00\x02\
                 \x00\x00\x21\x34\x00\x00\x07\xd0\
                 \x00\x00\x05\xdc\x00\x00\x05\xdc\
                 \x00\x00\x03\xe8\x00\x00\x00\x01\
                 \x1c\x08"
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

    ## MBC確認
    while(True):
        client.write(q_mbc)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(0.02)
        if(mbc_status(response) == 0):
            break
    ## 電磁ブレーキOFF
    client.write(q_release)
    time.sleep(0.02)
    client.read(size=16)
    time.sleep(0.02)
    ## (temp) MBC 確認
    client.write(q_mbc)
    time.sleep(0.02)
    response = client.read(size=16)
    time.sleep(0.02)
    if(mbc_status(response) == 1):
        print("ok")
        time.sleep(1)
    ## ダイレクトデータ運転
    client.write(q_direct)
    time.sleep(0.02)
    client.read(size=16)
    time.sleep(0.02)
    ## MOVE確認
    while(True):
        client.write(q_)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(0.02)
        if(move_status(response) == 0):
            break
    ## 電磁ブレーキON
    client.write(q_keep)
    time.sleep(0.02)
    client.read(size=16)
    time.sleep(0.02)
    ## (temp) MBC 確認
    client.write(q_mbc)
    time.sleep(0.02)
    response = client.read(size=16)
    time.sleep(0.02)
    if(mbc_status(response) == 0):
        print("ok2")
        time.sleep(1)
    # -------- 終了 --------
    client.close()

if __name__ == "__name__":
    main()
