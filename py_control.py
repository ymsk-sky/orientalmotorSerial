# -*- coding: utf-8 -*-

import os
import serial
from time import sleep


class SerialCommunication():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def set_serial(self, client,
                   port_type, baudrate,
                   bytesize=8, parity='N', stopbits=1, timeout=0.01):
        client.port = self.get_port(port_type)
        client.baudrate = baudrate
        client.bytesize = bytesize
        client.parity = parity
        client.stopbits = stopbits
        client.timeout = timeout

    def get_port(self, port_type):
        if(port_type == 'MotorDriver'):
            port = 'tty.usbserial'
        if(port_type == 'Arduino'):
            port = 'tty.usbmodem'
        else:
            print("cannot use port type")
            return
        for file in os.listdir('/dev'):
            if port in file:
                return '/dev/' + file
        return

    def write_serial(self, client, query):
        return client.write(query)

    def read_serial(self, client, size=1):
        return client.read(size)

    def open_serial(self, client):
        client.open()

    def close_serial(self, client):
        client.close()


class QueryGeneration():
    pass


def main():
    # シリアル通信インスタンスを生成
    sc = SerialCommunication()
    ### シリアル接続（モータードライバ）
    driver = serial.Serial()
    sc.set_serial(client=driver, port_type='MotorDriver',
                  baudrate=115200, parity='E', stopbits=1, timeout=0.01)
    ### シリアル接続（マイコン）
    arduino = serial.Serial()
    sc.set_serial(client=arduino, port_type='Arduino',
                  baudrate=19200, parity='N', stopbits=1, timeout=None)

    ### クエリ作成
    qg = QueryGeneration()
    ### ドライバ状態確認

    # *** ループ開始 ***

    ### センサ値取得
    ### クエリ作成
    ### モーター動作
    ### レスポンス確認

    # *** ループ終了 ***
    pass

if __name__ == "__main__":
    main()
