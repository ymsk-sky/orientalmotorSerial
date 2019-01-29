# -*- coding: utf-8 -*-

import os
import serial
from time import sleep

def main():
    driver = serial.Serial('/dev/tty.usbserial-FT1GOG9N', 115200,
                           parity='E', timeout=0.01)
    micro = serial.Serial('/dev/tty.usbmodem1421', 19200)

    driver.close()
    micro.close()

if __name__ == "__main__":
    main()
