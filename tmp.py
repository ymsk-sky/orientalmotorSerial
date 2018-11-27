# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import os

def com_port():
    devices = serial.tools.list_ports.comports()
    for device in devices:
        if("usbmodem" in device[0]):
            print(device[0])
            return device[0]

def com_port2():
    for file in os.listdir('/dev'):
        if "usbmodem" in file:
            print(file)
            return '/dev/' + file
    return

def main():
    client = serial.Serial()
    client.port = com_port2()
    client.baudrate = 19200
    client.bytesize = 8
    client.timeout = None
    client.open()

    a = client.read()
    b = int.from_bytes(a, 'big')
    print(b)

    client.close()

if __name__ == "__main__":
    main()
