# -*- coding: utf-8 -*-

import serial
import time

def set_serial(client):
    client.port = "/dev/tty.usbmodem1421"
    client.baudrate = 19200
    client.parity = 'N'
    client.stopbits = serial.STOPBITS_ONE
    client.timeout = 0.1

def main():
    client = serial.Serial()
    set_serial(client)
    client.open()
    # print(client)
    print("# OPEN AND SLEEP 2 SECONDS")
    time.sleep(2)   # waiting for reseting Arduino
    print("# START LOOP")
    # -- start serial communication --
    for _ in range(3):
        h = 255
        r = 1
        g = 55
        b = 254
        # v = (h.to_bytes(1, "big") + r.to_bytes(1, "big")
        #      + g.to_bytes(1, "big") + b.to_bytes(1, "big"))
        # client.write(v)
        time.sleep(1)
        res = client.read(size=16)
        print(res)
        time.sleep(1)
    # -- -- -- -- -- -- -- -- -- -- --
    client.close()

if __name__ == "__main__":
    main()
