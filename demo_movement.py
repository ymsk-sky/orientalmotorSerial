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

    # リモートI/Oアクセス
    ria = b"\x03\x00\x7f\x00\x01"
    remote_io_access_1 = b"\x01" + ria + crc_error_check(b"\x01" + ria)
    remote_io_access_2 = b"\x02" + ria + crc_error_check(b"\x02" + ria)
    remote_io_access_3 = b"\x03" + ria + crc_error_check(b"\x03" + ria)
    remote_io_access_4 = b"\x04" + ria + crc_error_check(b"\x04" + ria)
    remote_io_access_5 = b"\x05" + ria + crc_error_check(b"\x05" + ria)
    remote_io_access_6 = b"\x06" + ria + crc_error_check(b"\x06" + ria)

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

    ddp1 = b"\x01" + dd_p
    direct_data_operation_p_1 = ddp1 + crc_error_check(ddp1)
    ddm1 = b"\x01" + dd_m
    direct_data_operation_m_1 = ddm1 + crc_error_check(ddm1)
    ddp2 = b"\x02" + dd_p
    direct_data_operation_p_2 = ddp2 + crc_error_check(ddp2)
    ddm2 = b"\x02" + dd_m
    direct_data_operation_m_2 = ddm2 + crc_error_check(ddm2)

    ddp3 = b"\x03" + dd_p
    direct_data_operation_p_3 = ddp3 + crc_error_check(ddp3)
    ddm3 = b"\x03" + dd_m
    direct_data_operation_m_3 = ddm3 + crc_error_check(ddm3)
    ddp4 = b"\x04" + dd_p
    direct_data_operation_p_4 = ddp4 + crc_error_check(ddp4)
    ddm4 = b"\x04" + dd_m
    direct_data_operation_m_4 = ddm4 + crc_error_check(ddm4)

    ddp5 = b"\x05" + dd_p
    direct_data_operation_p_5 = ddp5 + crc_error_check(ddp5)
    ddm5 = b"\x05" + dd_m
    direct_data_operation_m_5 = ddm5 + crc_error_check(ddm5)
    ddp6 = b"\x06" + dd_p
    direct_data_operation_p_6 = ddp6 + crc_error_check(ddp6)
    ddm6 = b"\x06" + dd_m
    direct_data_operation_m_6 = ddm6 + crc_error_check(ddm6)

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
    direct_query_list = [[q.direct_data_operation_p_1,
                          q.direct_data_operation_p_2],
                         [q.direct_data_operation_m_1,
                          q.direct_data_operation_m_2]]
    remote_query_list = [q.remote_io_access_1, q.remote_io_access_2]

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
