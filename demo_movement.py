# -*- coding: utf-8 -*-

import serial
from time import sleep

# R: \x01, L: \x02
# 変数の末尾にRorLをつけて左右判断
# 反対でも左右対称の動きをするので前後の動作は問題なし・左右の動作は反転不可
class Queries():
    remote_io_access_R = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
    remote_io_access_L = b"\x02\x03\x00\x7f\x00\x01\xb5\xe1"

    direct_data_to_front_R = (b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                              + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                              + b"\x00\x00\x04\xe2" # 位置 +1250
                              + b"\x00\x00\xc3\x50" # 速度 50000
                              + b"\x00\x00\x13\x88" # 起動・変速レート 5000
                              + b"\x00\x00\x13\x88" # 停止レート 5000
                              + b"\x00\x00\x03\xe8\x00\x00\x00\x01\x1b\x33")

    direct_data_to_front_L = (b"\x02\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                              + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                              + b"\x00\x00\x04\xe2" # 位置 +1250
                              + b"\x00\x00\xc3\x50" # 速度 50000
                              + b"\x00\x00\x13\x88" # 起動・変速レート 5000
                              + b"\x00\x00\x13\x88" # 停止レート 5000
                              + b"\x00\x00\x03\xe8\x00\x00\x00\x01\x00\x87")

    direct_data_to_back_R = (b"\x01\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                             + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                             + b"\xff\xff\xfb\x1e" # 位置 -1250
                             + b"\x00\x00\xc3\x50" # 速度 50000
                             + b"\x00\x00\x13\x88" # 起動・変速レート 5000
                             + b"\x00\x00\x13\x88" # 停止レート 5000
                             + b"\x00\x00\x03\xe8\x00\x00\x00\x01\x09\xfc")

    direct_data_to_back_L = (b"\x02\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                             + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                             + b"\xff\xff\xfb\x1e" # 位置 -1250
                             + b"\x00\x00\xc3\x50" # 速度 50000
                             + b"\x00\x00\x13\x88" # 起動・変速レート 5000
                             + b"\x00\x00\x13\x88" # 停止レート 5000
                             + b"\x00\x00\x03\xe8\x00\x00\x00\x01\x12\x48")

def stop_rotation(ser, response):
    if(not (len(response) == 7)):
        ser.reset_input_buffer()
        return False
    status = (response[3] << 8) + response[4]
    move = (status >> 13) & 1
    if(move):
        return False
    else:
        return True

def main():
    motor_list = [b"\x01", b"\x02", b"\x03", b"\x04"]
    driver = serial.Serial(port = '/dev/tty.usbserial-FT1GOG9N',
                           baudrate = 115200,
                           parity = 'E',
                           timeout = 0.01)
    print("## START")
    # -------- -------- -------- --------
    q = Queries()

    while(True):
        # 右を前、左を後ろ
        driver.write(q.direct_data_to_front_R)
        sleep(0.02)
        response = driver.read(16)
        driver.write(q.direct_data_to_front_L)
        sleep(0.02)
        response = driver.read(16)

        # 動き終わるまで待機
        move_R = True
        move_L = True
        while(move_R or move_L):
            if(move_R):
                driver.write(q.remote_io_access_R)
                sleep(0.02)
                response = driver.read(16)
                if(stop_rotation(driver, response)):
                    move_R = False
            if(move_L):
                driver.write(q.remote_io_access_L)
                sleep(0.02)
                response = driver.read(16)
                if(stop_rotation(driver, response)):
                    move_L = False

        # 右を後ろ、左を前
        driver.write(q.direct_data_to_back_R)
        sleep(0.02)
        response = driver.read(16)
        driver.write(q.direct_data_to_back_L)
        sleep(0.02)
        response = driver.read(16)

        # 動き終わるまで待機
        move_R = True
        move_L = True
        while(move_R or move_L):
            if(move_R):
                driver.write(q.remote_io_access_R)
                sleep(0.02)
                response = driver.read(16)
                if(stop_rotation(driver, response)):
                    move_R = False
            if(move_L):
                driver.write(q.remote_io_access_L)
                sleep(0.02)
                response = driver.read(16)
                if(stop_rotation(driver, response)):
                    move_L = False
    # -------- -------- -------- --------
    print("## FINISH")
    driver.close()


if __name__ == "__main__":
    main()
