# -*- coding: utf-8 -*-

import serial
from time import sleep

def main():
    driver = serial.Serial(port = '/dev/tty.usbserial-FT1GOG9N',
                           baudrate = 115200,
                           parity = 'E',
                           timeout = 0.01)
    pass
    driver.close()

if __nama__ == "__main__":
    main()
