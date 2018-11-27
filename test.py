# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports

# ポートからusbmodem(Arduino)を取得してシリアル通信
# 値を読み込みint値(0~255)に変換し出力する
def main():
    ser = serial.Serial()
    ser.baudrate = 19200
    devices = serial.tools.list_ports.comports()
    for device in devices:
        if("usbmodem" in device[0]):
            print(device[0])
            ser.port = device[0]
    ser.open()
    while(True):
        val_data = ser.read()
        value = int.from_bytes(val_data, 'big')
        print(val_data, value)
        if(value == 255):
            break
    ser.close()

if __name__ == "__main__":
    main()
