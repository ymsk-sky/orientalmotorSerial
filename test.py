# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import time

# ポートからusbmodem(Arduino)を取得してシリアル通信
# 値を読み込みint値(0~255)に変換し出力する
def main():
    ser = serial.Serial()
    ser.baudrate = 19200
    ser.bytesize = 8
    ser.timeout = None
    ser.parity = serial.PARITY_EVEN
    ser.stopbits = serial.STOPBITS_ONE

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
        if(value == 255 or value == 0):
            break
    ser.close()

class Ser():
    client = serial.Serial()

def test():
    ser1 = Ser()
    ser2 = Ser()
    ser1.client.port = "/dev/tty.usbmodem1421"
    ser1.client.baudrate = 19200
    ser1.client.bytesize = 8
    ser1.client.timeout = None
    ser1.client.open()
    ser2.client.port = "/dev/tty.usbserial-FT1GOG9N"
    ser2.client.baudrate = 115200
    ser2.client.bytesize = 8
    ser2.client.timeout = 0.01
    ser2.client.parity = serial.PARITY_EVEN
    ser2.client.stopbits = serial.STOPBITS_ONE
    ser2.client.open()
    v = ser1.client.read(1)
    v2 = int.from_bytes(v, 'big')
    print(v2)
    ser2.client.write(b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08")
    time.sleep(0.02)
    a = ser2.client.read(16)
    time.sleep(0.02)
    print("response is", a)
    ser1.client.close()
    ser2.client.close()

class ClassT():
    def set_serial(self, ser, br):
        print("set:", id(ser), br)
        ser.baudrate = br


def test2():
    t1 = ClassT()
    t2 = ClassT()

    s1 = serial.Serial()
    s2 = serial.Serial()

    t1.set_serial(s1, 9600)
    t2.set_serial(s2, 115200)

    print(s1, id(s1))
    print(s2, id(s2))

if __name__ == "__main__":
    # main()
    # test()
    test2()
