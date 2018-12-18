# -*- coding: utf-8 -*-

import os
import serial
import time

import py_control as ctl

import sensor_test

# 高速原点回帰運動
def test1():
    sc = ctl.SerialCommunication()
    drv = serial.Serial()
    sc.set_serial(client=drv, port_type='MotorDriver', baudrate=115200,
                  parity='E', stopbits=1, timeout=0.01)
    sc.open_serial(drv)

    po = ctl.ProvisionOperation()
    po.high_speed_return_to_origin_operation(drv, slave=1)
    time.sleep(3)
    po.high_speed_return_to_origin_operation(drv, slave=2)

    sc.close_serial(drv)


# 電磁ブレーキステータスへのアクセス
def test2():
    ### MBC: レジスタアドレス: 379(017Bh) bit9
    client = serial.Serial()
    set_serial(client)
    client.open()
    mbc_query = make_mbc_query()
    for _ in range(10):
        client.write(mbc_query)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(0.02)
        mbc = get_mbc_status(response)
        print("MBC:", mbc)
        time.sleep(0.1) # ディレイ
    c_on_query = make_c_on_query()
    for _ in range(10):
        pass
    client.close()

def make_c_on_query():
    # *** bit2 R-IN2(M2)をC-ONに書き換える
    query = b"\x01"                 # スレーブアドレス(1号機)
    query += b"\x06"                # ファンクションコード(06:1レジスタ書き込み)
    # ドライバ入力指令
    # レジスタアドレス: 125(007Dh)
    # 書き込む値: 4(0004h, 0000_0000_0000_0100b)
    # bit2へ1を書き込む(ONにする)
    query += b"\x00\x7d\x00\x04"    # データ(007Dhに0004を書き込む)
    query += b"\x18\x11"            # エラーチェック
    return query

def get_mbc_status(r):
    return (((r[3] << 8) + r[4]) >> 9) & 1

def make_mbc_query():
    query = b"\x01"                 # スレーブアドレス
    query += b"\x03"                # ファンクションコード
    query += b"\x01\x7b\x00\x01"    # データ
    query += b"\xf5\xef"            # エラーチェック
    return query

def set_serial(c):
    c.port = get_port()
    c.baudrate = 115200
    c.bytesize = 8
    c.parity = 'E'
    c.stopbits = 1
    c.timeout = 0.01

def get_port():
    for file in os.listdir('/dev'):
        if 'tty.usbserial' in file:
            return '/dev/' + file
    return

# ドライバ入力指令を読む
def test3():
    client = serial.Serial()
    set_serial(client)
    client.open()
    time.sleep(2)   # ディレイ
    q = b"\x01\x03\x00\x7d\x00\x01\x14\x12"
    for _ in range(100):
        client.write(q)
        time.sleep(0.02)
        r = client.read(size=16)
        print_result(r)
        time.sleep(0.02)
    client.close()

def print_result(r):
    list = ["RV-POS", "FW-POS", "RV-JOG-P", "FW-JOG-P",
            "SSTART", "D-SEL2", "D-SEL1", "D-SEL0",
            "ALM-RST", "FREE", "STOP", "ZHOME",
            "START", "M2", "M1", "M0"]
    h = r[3]
    l = r[4]
    _h = bin(h)[2:].zfill(8)
    _l = bin(l)[2:].zfill(8)
    print("="*30)
    for i in range(16):
        if(i < 8):
            print("bit" + str(15-i) + "\t" + "%8s"%list[i] + "\t" + _h[i])
        else:
            print("bit" + str(15-i) + "\t" + "%8s"%list[i] + "\t" + _l[i-8])

if __name__ == "__main__":
    # test1()
    # test2()
    test3()
