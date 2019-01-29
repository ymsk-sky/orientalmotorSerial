# -*- coding: utf-8 -*-

import os
import serial
from time import sleep

# マイコンのポートを取得する
def get_port_micro():
    for file in os.listdir('/dev'):
        if 'tty.usbmodem' in file:
            return '/dev/' + file

def main():
    driver = serial.Serial('/dev/tty.usbserial-FT1GOG9N', 115200,
                           parity='E', timeout=0.01)
    micro = serial.Serial(get_port_micro(), 19200)
    sleep(2)    # Arduino初期化を待機
    # ドライバ状態確認

    while(True):
        break
    # 終了
    driver.close()
    micro.close()

if __name__ == "__main__":
    main()
