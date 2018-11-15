# -*- coding: utf-8 -*-

import os
import serial
import time

client = serial.Serial()
size = 16

def main():
    set_serial()
    client.open()
    ##### direct data operation #####
    for _ in range(3):
        direct = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08"
        client.write(direct)
        standby()
        response = client.read(size)
        print(response)
        standby()
        ##### remote I/O accessing #####
        command = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
        while(True):
            client.write(command)
            standby()
            response = client.read(size)
            move = print_move_status(response)
            standby()
            if(move == 0):
                break
        #####
    client.close()

def print_move_status(response):
    driver_output = (response[3] << 8) + response[4]
    move = (driver_output >> 13) & 1
    if(move == 1):
        print("Moving")
    elif(move == 0):
        print("NOT Moving: stopping")
    return move

def standby():
    time.sleep(0.02)

def set_serial():
    client.port = get_com_port()
    client.baudrate = 115200
    client.bytesize = 8
    client.timeout = 0.01
    client.parity = serial.PARITY_EVEN
    client.stopbits = serial.STOPBITS_ONE

def get_com_port():
    for file in os.listdir('/dev'):
        if "tty.usbserial" in file:
            return '/dev/' + file
    return

if __name__ == "__main__":
    main()
