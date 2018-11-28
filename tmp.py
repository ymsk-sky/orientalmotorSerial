# -*- coding: utf-8 -*-

import serial

class Test():
    def set_serial(self, client, a):
        if(a == 1):
            client.port = "/dev/tty.usbmodem1421"
            client.baudrate = 19200
        elif(a == 2):
            client.port = "/dev/tty.usbserial-FT1GOG9N"
            client.baudrate = 115200
            client.timeout = 0.01
            client.parity= 'N'

    def open_serial(self, client):
        client.open()

def main():
    t = Test()

    client1 = serial.Serial()
    client2 = serial.Serial()

    t.set_serial(client1, 1)
    t.open_serial(client1)

    t.set_serial(client2, 2)
    t.open_serial(client2)

if __name__ == "__main__":
    main()
