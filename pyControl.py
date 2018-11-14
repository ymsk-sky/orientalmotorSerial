# -*- coding: utf-8 -*-

import os
import serial
import time

class serialCommunication():
    __client = serial.Serial()

    def setSerial(self, br=115200, bs=8, to=0.01):
        self.__client.port = self.getComPort()
        self.__client.baudrate = br
        self.__client.bytesize = bs
        self.__client.timeout = to
        self.__client.parity = serial.PARITY_EVEN
        self.__client.stopbits = serial.STOPBITS_ONE

    def getComPort(self):
        for file in os.listdir('/dev'):
            if 'tty.usbserial' in file:
                return '/dev/' + file
        return

    def open(self):
        self.__client.open()

    def close(self):
        self.__client.close()

def main():
    ##### シリアル接続 #####
    sc = serialCommunication()
    sc.setSerial()
    sc.open()
    ##### クエリ作成 #####
    # 状態確認：READY=1, MOVE=0, ALM_A=0
    ##### クエリ作成 #####
    # ダイレクトデータ運転
    ##### クエリ作成 #####
    # 状態確認：MOVE=0になるまでループ
    # ダイレクトデータ運転に戻る
    ##### 接続終了 #####
    sc.close()


if __name__ == "__main__":
    main()
