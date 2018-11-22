# -*- coding: utf-8 -*-

class DummySerial():
    def __init__(self):
        print("init dummy serial")

    def __del__(self):
        print("del dummy serial")

    __serial = 0
    __value = 0

    def set_serial(self, ser):
        self.__serial = ser

    def get_serial(self):
        return self.__serial

    def print_serial(self):
        print(self.__serial)

def setting_serial(ser):
    ser.set_serial(100)
    print("set serial")
    print("ID-02:", id(ser))

def main():
    print("-----before-----")
    ser = DummySerial()
    print("ID-01:", id(ser))
    print("-----after-----")
    setting_serial(ser)
    result = ser.get_serial()
    print(result)
    print("ID-03:", id(ser))

    for x in range(10):
        pass

    print("fin")

if __name__ == "__main__":
    main()
