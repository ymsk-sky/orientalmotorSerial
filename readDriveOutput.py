# -*- coding: utf-8 -*-

import os
import serial
import time

client = serial.Serial()
size = 16

def main():
    setSerial()

    client.open()
    # -- 処理開始 --
    readDriveOutputValue()
    # -- 処理終了 --
    client.close()

def readDriveOutputValue():
    commando = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"  # レジスタアドレス(下位)
    #commando = b"\x01\x03\x00\x7e\x00\x02\xa4\x13"  # レジスタアドレス(上位から2つ)
    client.write(commando)
    time.sleep(0.003)
    result = client.read(size)
    print(result)

# -- setting methods --
def setSerial():
    client.port = getComPort()
    client.baudrate = 115200
    client.bytesize = 8
    client.timeout = 0.01
    client.parity = serial.PARITY_EVEN
    client.stopbits = serial.STOPBITS_ONE

def getComPort():
    for file in os.listdir('/dev'):
        if "tty.usbserial" in file:
            return '/dev/' + file
    return

if __name__ == '__main__':
    main()
