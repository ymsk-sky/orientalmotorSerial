# -*- coding: utf-8 -*-

import serial
import time

def set_serial(client):
    client.port = "/dev/tty.usbmodem1421"
    client.baudrate = 19200
    client.parity = 'N'
    client.stopbits = serial.STOPBITS_ONE
    client.timeout = 0.1

def print_val(response):
    val_x = (response[0] << 8) + response[1]
    val_y = (response[2] << 8) + response[3]
    print(val_x, val_y)

def main():
    client = serial.Serial()
    set_serial(client)
    client.open()
    # print(client)
    print("# OPEN AND SLEEP 2 SECONDS")
    time.sleep(2)   # waiting for reseting Arduino
    print("# START LOOP")
    # -- start serial communication --
    for _ in range(100):
        client.write(b"\xFF")
        time.sleep(0.02)
        response = client.read(size=4)
        print_val(response)
        time.sleep(0.02)
    # -- -- -- -- -- -- -- -- -- -- --
    client.close()

if __name__ == "__main__":
    main()
