# -*- coding: utf-8 -*-

class Dummyserial():
    def __init__(self):
        print("Dummyserial --開始")

    port = 0
    baudrate = 0

    def write(self, cmd):
        print("write:", cmd)

class Test():
    #__client = Dummyserial()

    int_1 = 1
    int_2 = 2

    str_abc = "abc"
    str_xyz = "xyz"

    def serial_write(self, cmd):
        self.__client.write(cmd)

def func(t):
    t.serial_write("func write")

def main():
    t = Test()
    t.serial_write("command")

    func(t)

class U():
    def printP(self):
        print("P")

class T():
    def main2(self):
        print("main")

if __name__ == "__main__":
    # main()
    t = T()
    t.main2()
