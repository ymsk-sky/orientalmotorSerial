import os
import serial

# COM = "/dev/tty.usbserial-FT1G0G9N"

ser = serial.Serial()
size = 16

def main():
    setSerial()
    print(ser.name)

    ser.open()
    command(10)
    ser.close()

def command(cmd):
    command = getCommand(cmd)
    ser.write(command)


def getCommand(cmd):
    if cmd == 10:
        return b"\x01\x10\x00\x7c\x00\x02\x04\x00\x00\x00\x00\xf4\xde"
    elif cmd == 20:
        return b"\x01\x10\x00\x7c\x00\x02\x04\x00\x00\x00\x08\xf5\x18"
    else:
        return

# set serial parameters
def setSerial():
    ser.port = getComPort()
    ser.baudrate = 115200
    ser.bytesize = 8
    ser.timeout = 0.01
    ser.parity = serial.PARITY_EVEN
    ser.stopbits = serial.STOPBITS_ONE

# get COM port name
def getComPort():
    for file in os.listdir('/dev'):
        if "tty.usbserial" in file:
            return '/dev/' + file
    return

if __name__ == '__main__':
    main()
