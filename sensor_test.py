# -*- coding: utf-8 -*-

class DummySerial():
    __SERIAL_FG = False
    __serial = {"port": "/dev/comport", "baudrate": 0, "bytesize": 8}

    def __init__(self):
        pass

    def set_serial(self, p="", b=0, s=0):
        self.__serial["port"] = p
        self.__serial["baudrate"] = b
        self.__serial["bytesize"] = s

    def read_serial(self):
        if(self.__SERIAL_FG):
            pass
        else:
            print("NOT OPEN SERIAL")

    def write_serial(self, cmd):
        if(self.__SERIAL_FG):
            pass
        else:
            print("NOT OPEN SERIAL")

    def open_serial(self):
        if(self.__SERIAL_FG):
            print("ALREADY OPENED SERIAL")
            exit()
        else:
            self.__SERIAL_FG = True

    def close_serial(self):
        if(self.__SERIAL_FG):
            self.__SERIAL_FG = False
        else:
            print("NOT OPEN SERIAL")

    def print_serial(self):
        print(self.__serial)

class DriverSerial(DummySerial):
    pass

class SensorSerial(DummySerial):
    pass

class Main():
    def main(self):
        driver = DriverSerial()
        sensor = SensorSerial()
        driver.open_serial()
        sensor.open_serial()
        ##### 処理 - 開始 #####
        # 初期設定
        # ループ
        while(True):
            break
        ##### 処理 - 終了 #####
        driver.close_serial()
        sensor.close_serial()


if __name__ == "__main__":
    main = Main()
    main.main()
