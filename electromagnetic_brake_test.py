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
    print("##### START")
    client = serial.Serial()
    set_serial(client)
    client.open()
    print("##### SERIAL OPEN")
    # -------- 開始 --------
    # クエリ作成
    ## MBC(電磁ブレーキの状態)読み出し
    q_mbc = b"\x01\x03\x01\x7b\x00\x01\xf5\xef"
    ## C-ONをON = 電磁ブレーキを解放
    q_release = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    ## C-ONをOFF = 電磁ブレーキを保持
    q_keep = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    ## ダイレクトデータ運転（例）
    q_direct = (b"\x01\x10\x00\x58\x00\x10\x20"
                + b"\x00\x00\x00\x00\x00\x00\x00\x02"
                + b"\x00\x00\x21\x34\x00\x00\x07\xd0"
                + b"\x00\x00\x05\xdc\x00\x00\x05\xdc"
                + b"\x00\x00\x03\xe8\x00\x00\x00\x01"
                + b"\x1c\x08")
    q_status = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
    print("##### QUERY READY")
    ## MBC確認
    # while(True):
    #     client.write(q_mbc)
    #     time.sleep(0.02)
    #     response = client.read(size=16)
    #     print(response)
    #     time.sleep(0.02)
    #     if(mbc_status(response) == 0):
    #         break
    print("##### INITED")
    ## 電磁ブレーキOFF
    client.write(q_release)
    time.sleep(0.02)
    response = client.read(size=16)
    time.sleep(0.02)
    print("brake off")
    print(response)
    time.sleep(1)
    ## ダイレクトデータ運転
    client.write(q_direct)
    time.sleep(0.02)
    response = client.read(size=16)
    print("direct data operation")
    print(response)
    time.sleep(0.02)
    time.sleep(1)   # direct data operation now
    ## MOVE確認
    while(True):
        client.write(q_status)
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
    # -------- 終了 --------
    client.close()
    print("##### SERIAL CLOSE")


def change_c_on_status(b):
    client = serial.Serial("/dev/tty.usbserial-FT1GOG9N", 115200, 8, 'E', 1, 0.01)
    if(b==0):
        # 解放
        q = b"\x01\x06\x00\x7d\x00\x04\x18\x11"
    elif(b==1):
        # 保持
        q = b"\x01\x06\x00\x7d\x00\x00\x19\xd2"
    client.write(q)
    time.sleep(0.02)
    response = client.read(size=16)
    time.sleep(0.02)
    client.close()

def make_query():
    query = b"\x01"
    # スレーブアドレス
    ## ドライバにスイッチで割り当てる
    ## 0はブロードキャスト(*このときクエリ送信してもレスポンスがないので注意)
    # ファンクションコード
    ## 使用するのは(読み出し, 書き込み, 複数書き込み)の3つ
    # データ
    ## レジスタアドレスや書き込み数（読み出し数）などで長さはNとなる
    # エラーチェック
    ## エラーチェック以外のクエリからエラーチェック(CRC-16/Modbus)を算出
    ## CRC-16/Modbus計算は実装済み
    return query

def test_main():
    # シリアル確立
    client = serial.Serial()
    set_serial(client)
    client.open()
    # ---------------- 開始 ----------------
    query = make_query()
    # ---------------- 終了 ----------------
    client.close()

if __name__ == "__main__":
    main()
    # change_c_on_status(1)
