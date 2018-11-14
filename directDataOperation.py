# -*- coding: utf-8 -*-

import os
import serial
import time

client = serial.Serial()
size = 16

def main():
    setSerial()
    client.open()
    sendTrigger()
    closeSerial()

def sendTrigger():
    cmd = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08"
    client.write(cmd)
    time.sleep(0.02)
    result = client.read(size)
    # print(result)
    r = ''.join([r'\x{:02x}'.format(x) for x in result]).split('\\x')
    r.pop(0)
    print(r)

def closeSerial():
    client.close()

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
