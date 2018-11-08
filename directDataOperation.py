# -*- coding: utf-8 -*-

import os
import serial

client = serial.Serial()

def main():
    setSerial()
    client.open()
    sendTrigger()
    closeSerial()

def sendTrigger():
    cmd = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xD0\x00\x00\x05\xDC\x00\x00\x05\xDC\x00\x00\x03\xE8\x00\x00\x00\x01\x1C\x08"
    client.write(cmd)

def closeSerial():
    client.close()

def setSerial():
    client.port = getComPort()
    client.baudrate = 115200
    client.bytesize = 8
    client.parity = 'E'
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
