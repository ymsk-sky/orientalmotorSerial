# -*- coding: utf-8 -*-

import serial
from time import sleep

# R: \x01, L: \x02
# 変数の末尾にRorLをつけて左右判断
# 反対でも左右対称の動きをするので前後の動作は問題なし・左右の動作は反転不可
class Queries():
    # CRC-16/Modbusによるエラーチェック
    def crc_error_check(query):
        crc_register = 0xFFFF
        for data_byte in query:
            crc_register ^= data_byte
            for _ in range(8):
                overflow = crc_register & 1 == 1
                crc_register >>= 1
                if overflow:
                    crc_register ^= 0xA001
        # 結果は(上位→下位)の順
        return crc_register.to_bytes(2, 'little')

    # スレーブアドレス一覧
    slave_addresses = [b"\x01", b"\x02", b"\x03", b"\x04", b"\x05", b"\x06"]

    # リモートI/Oアクセス
    ria = b"\x03\x00\x7f\x00\x01"
    remote_io_access = []
    for add in slave_addresses:
        remote_io_access.append(add + ria + crc_error_check(add + ria))

    # ダイレクトデータ運転
    dd_p = (b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
            + b"\x00\x00\x00\x01" # 方式 絶対位置決め
            + (1250).to_bytes(4, "big", signed=True) # 位置
            + (50000).to_bytes(4, "big") # 速度
            + (100000).to_bytes(4, "big") # 起動・変速レート
            + (100000).to_bytes(4, "big") # 停止レート
            + b"\x00\x00\x03\xe8\x00\x00\x00\x01")

    dd_m = (b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
            + b"\x00\x00\x00\x01" # 方式 絶対位置決め
            + (-1250).to_bytes(4, "big", signed=True) # 位置
            + (50000).to_bytes(4, "big") # 速度
            + (100000).to_bytes(4, "big") # 起動・変速レート
            + (100000).to_bytes(4, "big") # 停止レート
            + b"\x00\x00\x03\xe8\x00\x00\x00\x01")

    direct_data_operation_plus = []
    for add in slave_addresses:
        tmp = add + dd_p
        direct_data_operation_plus.append(tmp + crc_error_check(tmp))

    direct_data_operation_minus = []
    for add in slave_addresses:
        tmp = add + dd_m
        direct_data_operation_minus.append(tmp + crc_error_check(tmp))

# 回転が停止状態かを確認
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
    # motor_list = [b"\x01", b"\x02", b"\x03", b"\x04"]
    driver = serial.Serial(port = '/dev/tty.usbserial-FT1GOG9N',
                           baudrate = 115200,
                           parity = serial.PARITY_EVEN,
                           timeout = 0.01)
    print("## START")
    # -------- -------- -------- --------
    q = Queries()

    # クエリリスト作成
    direct_query_list = [[q.direct_data_operation_plus[0],
                          q.direct_data_operation_plus[1]],
                         [q.direct_data_operation_minus[0],
                          q.direct_data_operation_minus[1]]]
    remote_query_list = [q.remote_io_access[0], q.remote_io_access[1]]

    # 動作ループ
    for _ in range(3):
        for step in direct_query_list:
            # 一回の動作分のクエリを送信
            for query in step:
                driver.write(query)
                sleep(0.02)
                response = driver.read(16)
                print(response)
            # 動き終わるまで待機
            for query in remote_query_list:
                while(True):
                    driver.write(query)
                    sleep(0.02)
                    response = driver.read(16)
                    if(stop_rotation(driver, response)):
                        break
    # -------- -------- -------- --------
    print("## FINISH")
    driver.close()


if __name__ == "__main__":
    main()
