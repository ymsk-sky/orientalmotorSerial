# -*- coding: utf-8 -*-

import os
import serial
import time
# import threading
import concurrent.futures

client = serial.Serial()
size = 16

def test():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    executor.submit(func1)
    executor.submit(func2)
    executor.submit(func3)

def func1():
    for _ in range(100):
        print("func1")
    print("func1 is finished")

def func2():
    for _ in range(100):
        print("func2")
    print("func2 is finished")

def func3():
    for _ in range(100):
        print("func3")
    print("func3 is finished")

def io_test():
    set_serial()
    client.open()
    ##### direct data operation #####
    for _ in range(1):
        # direct = b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x21\x34\x00\x00\x07\xd0\x00\x00\x05\xdc\x00\x00\x05\xdc\x00\x00\x03\xe8\x00\x00\x00\x01\x1c\x08"
        # client.write(direct)
        # standby()
        # response = client.read(size)
        # print(response)
        # standby()
        ##### remote I/O accessing #####
        command = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
        while(True):
            client.write(command)
            standby()
            response = client.read(size)
            move = print_move_status(response)
            print("{0:016d}".format(int(bin(((response[3] << 8) + response[4]))[2:])))
            standby()
            if(move == 1):
                break
        #####
    client.close()

def print_move_status(response):
    driver_output = (response[3] << 8) + response[4]
    move = (driver_output >> 13) & 1
    if(move == 1):
        pass
        #print("Moving")
    elif(move == 0):
        pass
        #print("NOT Moving: stopping")
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

def main():
    pass

if __name__ == "__main__":
    # main()
    # io_test()
    test()
