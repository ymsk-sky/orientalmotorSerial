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

    remote_io_access_R = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"
    remote_io_access_L = b"\x02\x03\x00\x7f\x00\x01\xb5\xe1"

    base_direct_data_to_plus = (b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                                + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                                + (1250).to_bytes(4, "big", signed=True) # 位置
                                + (50000).to_bytes(4, "big") # 速度
                                + (100000).to_bytes(4, "big") # 起動・変速レート
                                + (100000).to_bytes(4, "big") # 停止レート
                                + b"\x00\x00\x03\xe8\x00\x00\x00\x01")

    base_direct_data_to_minus = (b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
                                 + b"\x00\x00\x00\x01" # 方式 絶対位置決め
                                 + (-1250).to_bytes(4, "big", signed=True) # 位置
                                 + (50000).to_bytes(4, "big") # 速度
                                 + (100000).to_bytes(4, "big") # 起動・変速レート
                                 + (100000).to_bytes(4, "big") # 停止レート
                                 + b"\x00\x00\x03\xe8\x00\x00\x00\x01")

    ddtf_r = b"\x01" + base_direct_data_to_plus
    direct_data_to_plus_R = ddtf_r + crc_error_check(ddtf_r)

    ddtf_l = b"\x02" + base_direct_data_to_plus
    direct_data_to_plus_L = ddtf_l + crc_error_check(ddtf_l)

    ddtb_r = b"\x01" + base_direct_data_to_minus
    direct_data_to_minus_R = ddtb_r + crc_error_check(ddtb_r)

    ddtb_l = b"\x02" + base_direct_data_to_minus
    direct_data_to_minus_L = ddtb_l + crc_error_check(ddtb_l)


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
                           parity = 'E',
                           timeout = 0.01)
    print("## START")
    # -------- -------- -------- --------
    q = Queries()

    # クエリリスト作成
    direct_query_list = [[q.direct_data_to_plus_R, q.direct_data_to_plus_L],
                         [q.direct_data_to_minus_R, q.direct_data_to_minus_L]]
    remote_query_list = [q.remote_io_access_R, q.remote_io_access_L]

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
