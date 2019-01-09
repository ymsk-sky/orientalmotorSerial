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
    q = b"\x01\x03\x00\x7d\x00\x01\x14\x12" # 確認
    for x in range(16):
        c_on_query = make_c_on_query(x)
        client.write(mbc_query)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(0.02)
        # mbc = get_mbc_status(response)
        # print("MBC:", mbc)
        time.sleep(1) # ディレイ

        client.write(c_on_query)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(1) # ディレイ

        client.write(q)
        time.sleep(0.02)
        response = client.read(size=16)
        print_result(response)
        time.sleep(1) # ディレイ
    client.close()

def make_c_on_query(x):
    # *** bit2 R-IN2(M2)をC-ONに書き換える(ID1のみ変更済み)
    query = b"\x01"                 # スレーブアドレス(1号機)
    query += b"\x06"                # ファンクションコード(06:1レジスタ書き込み)
    # ドライバ入力指令
    # レジスタアドレス: 125(007Dh)
    # 書き込む値: 4(0004h, 0000_0000_0000_0100b)
    # bit2へ1を書き込む(ONにする)
    query += b"\x00\x7d"    # データ(007Dhに0004を書き込む)
    query += (1 << x).to_bytes(2, "big")
    query += create_error_check(query)            # エラーチェック
    return query

def create_error_check(query):
    reg = 0xFFFF
    for d in query:
        t = reg ^ d
        n = 0
        while(n < 8):
            if(t&1 ==1):
                t >>= 1
                n += 1
                t = 0xA001 ^ t
            else:
                t >>= 1
                n += 1
        reg = t
    return reg.to_bytes(2, "little")

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
            "START", "C-ON", "M1", "M0"]
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

def free():
    c = serial.Serial()
    set_serial(c)
    c.open()
    time.sleep(0.1)
    c.write(b"\x01\x06\x00\x7d\x00\x44\x19\xe1")
    time.sleep(0.02)
    response = c.read(size=16)
    T = 100
    for x in range(T):
        print("time:", T-x)
        time.sleep(0.1)
    c.write(b"\x01\x06\x00\x7d\x00\x00\x19\xd2")
    time.sleep(0.02)
    response = c.read(size=16)
    time.sleep(0.02)
    print("written")
    c.close()

def reset(fg_reset):
    c = serial.Serial()
    set_serial(c)
    c.open()
    time.sleep(0.1)
    if(fg_reset==1):
        c.write(b"\x01\x06\x00\x7d\x00\x00\x19\xd2")
    elif(fg_reset==0):
        c.write(b"\x01\x06\x00\x7d\x00\x04\x18\x11")
    time.sleep(0.02)
    c.read(size=16)
    time.sleep(0.02)
    c.close()

if __name__ == "__main__":
    # test1() # 原点復帰
    # test2()
    # test3()
    # free()
    reset(1)
