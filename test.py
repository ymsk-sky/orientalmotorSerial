# -*- coding: utf-8 -*-

import os
import serial
import time

client = serial.Serial()
size = 16

def get_com_port():
    for file in os.listdir('/dev'):
        if "tty.usbserial" in file:
            return '/dev/' + file
    return

def set_serial():
    client.port = get_com_port()
    client.baudrate = 115200
    client.bytesize = 8
    client.timeout = 0.01
    client.parity = serial.PARITY_EVEN
    client.stopbits = serial.STOPBITS_ONE

def open_serial():
    client.open()

def close_serial():
    client.close()

def send_trigger():
    query = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08"
    client.write(query)
    time.sleep(0.02)
    response = client.read(size)
    time.sleep(0.02)
    print(response)
    for x in range(3):
        print(x)
        time.sleep(1)
    query = b"\x02\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x07\xbc"
    client.write(query)
    time.sleep(0.02)
    response = client.read(size)
    time.sleep(0.02)
    print(response)

def main():
    set_serial()
    open_serial()
    send_trigger()
    close_serial()

if __name__ == "__main__":
    main()
