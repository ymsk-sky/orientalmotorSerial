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
    query = make_query()
    while(True):
        client.write(query)
        time.sleep(0.02)
        response = client.read(size=16)
        time.sleep(0.02)
        mbc = get_mbc_status(response)
        print("MBC:", mbc)
        time.sleep(0.1) # ディレイ
    client.close()

def get_mbc_status(r):
    return (((r[3] << 8) + r[4]) >> 9) & 1

def make_query():
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

if __name__ == "__main__":
    # test1()
    test2()
