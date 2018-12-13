# -*- coding: utf-8 -*-

# Arudino側: memsic2125.inoに対応
# ヘッダーとヘッダーと区別するための1ビット左シフトを実装

import serial
import time

size = 5
# correct_head = b"\xFF"
head_value = 255
correct_head = head_value.to_bytes(1, "big")

def set_serial(client):
    client.port = "/dev/tty.usbmodem1411"
    client.baudrate = 19200
    client.parity = 'N'
    client.stopbits = serial.STOPBITS_ONE
    client.timeout = 0.1

def is_correct_head(head):
    if(head == correct_head):
        return True
    else:
        return False

def is_correct_check_sum(response):
    checksum = response[-1]
    data = response[:-1]
    sum = 0
    for val in data:
        sum += val
    sum &= 0xFF
    if(sum == checksum):
        return True
    else:
        return False

def print_val(response):
    tmp = response[:-1]
    tmp2 = int.from_bytes(tmp, "big")
    tmp2 >>= 1
    data = tmp2.to_bytes(len(response) - 1, "big")
    val_x = (data[0] << 8) + data[1]
    val_y = (data[2] << 8) + data[3]
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
        # クエリ送信（仮）
        client.write(b"\xFF")
        time.sleep(0.02)
        head = client.read()
        # ヘッダか確認して正しければデータを読み込む
        if(is_correct_head(head)):
            response = client.read(size=size)
            # チェックサムを確認して正しければ値を表示
            if(is_correct_check_sum(response)):
                print_val(response)
                time.sleep(0.02)
    # -- -- -- -- -- -- -- -- -- -- --
    client.close()

if __name__ == "__main__":
    main()
