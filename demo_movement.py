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
    def make_dd_query(address, position, speed, op_rate, ed_rate):
        def error_check(query):
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

        t = (address
             + b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00"
             + b"\x00\x00\x00\x01"  # 方式 絶対位置決め
             + position.to_bytes(4, "big", signed=True) # 位置
             + speed.to_bytes(4, "big") # 速度
             + op_rate.to_bytes(4, "big")   # 起動・変速レート
             + ed_rate.to_bytes(4, "big")   # 停止レート
             + b"\x00\x00\x03\xe8\x00\x00\x00\x01")
        return t + error_check(t)

    direct_data_operation_plus = []     # 正方向への回転(CW)
    direct_data_operation_minus = []    # 負方向への回転(CCW)
    direct_data_operation_base = []     # 原点への回転(位置0へ移動)
    foot_plus = []                      # 足首を正回転(CW)
    foot_minus = []                     # 足首を負回転(CCW)
    for add in slave_addresses:
        direct_data_operation_plus.append(make_dd_query(add, 1250, 50000, 100000, 100000))
        direct_data_operation_minus.append(make_dd_query(add, -1250, 50000, 100000, 100000))
        direct_data_operation_base.append(make_dd_query(add, 0, 50000, 100000, 100000))
        foot_plus.append(make_dd_query(add, 5000, 50000, 100000, 100000))
        foot_minus.append(make_dd_query(add, -5000, 50000, 100000, 100000))

    # 高速原点復帰運転
    hsrtoo_on = b"\x06\x00\x7d\x00\x10"
    hsrtoo_off = b"\x06\x00\x7d\x00\x00"
    high_speed_return_on = []
    high_speed_return_off = []
    for add in slave_addresses:
        tmp_on = add + hsrtoo_on
        tmp_off = add + hsrtoo_off
        high_speed_return_on.append(tmp_on + crc_error_check(tmp_on))
        high_speed_return_off.append(tmp_off + crc_error_check(tmp_off))


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
    # モーターリスト
    # P: PSギア - 左右, F: FCギア - 前後, D: DRSM(アクチュエータ) - 上下
    # *********************************************
    # **** ドライバとモーターのケーブル接続と合わせる ****
    # *********************************************
    PR = 0  # 左右動作 - 右
    PL = 1  # 左右動作 - 左
    FR = 2  # 前後動作 - 右
    FL = 3  # 前後動作 - 左
    DR = 4  # 上下動作 - 右
    DL = 5  # 上下動作 - 左

    driver = serial.Serial(port = '/dev/tty.usbserial-FT1GOG9N',
                           baudrate = 115200,
                           parity = serial.PARITY_EVEN,
                           timeout = 0.01)
    print("## START")
    # -------- -------- -------- --------
    q = Queries()

    # クエリリスト作成
    ### 前後動作
    direct_query_list1 = [[q.direct_data_operation_plus[FR],
                           q.direct_data_operation_plus[FL],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_minus[FR],
                           q.direct_data_operation_minus[FL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]]]
    ### 擬似ふらつき動作
    direct_query_list2 = [[q.direct_data_operation_base[FL],
                           q.direct_data_operation_base[PL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]],
                          [q.direct_data_operation_base[FR],
                           q.direct_data_operation_base[PR],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_minus[FL],
                           q.direct_data_operation_minus[PL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]],
                          [q.direct_data_operation_plus[FR],
                           q.direct_data_operation_base[PR],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_plus[FL],
                           q.direct_data_operation_base[PL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]],
                          [q.direct_data_operation_minus[FR],
                           q.direct_data_operation_plus[PR],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_base[FL],
                           q.direct_data_operation_minus[PL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]],
                          [q.direct_data_operation_base[FR],
                           q.direct_data_operation_base[PR],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_minus[FL],
                           q.direct_data_operation_base[PL],
                           q.direct_data_operation_plus[DR],
                           q.direct_data_operation_minus[DL]],
                          [q.direct_data_operation_plus[FR],
                           q.direct_data_operation_plus[PR],
                           q.direct_data_operation_minus[DR],
                           q.direct_data_operation_plus[DL]]]
    ### アクチュエータのみ回転
    direct_query_list3 = [[q.direct_data_operation_plus[DR],
                           q.direct_data_operation_plus[DL]],
                          [q.direct_data_operation_minus[DR],
                           q.direct_data_operation_minus[DL]]]

    ### アクチュエータのみ回転（list3より多く回転させる）
    direct_query_list4 = [[q.foot_plus[DR],
                           q.foot_plus[DL]],
                          [q.foot_minus[DR],
                           q.foot_minus[DL]]]
    """
    direct_query_list4 = [[q.direct_data_operation_[],
                           q.direct_data_operation_[]],
                          [q.direct_data_operation_[],
                           q.direct_data_operation_[]]]

    direct_query_list5 = [[q.direct_data_operation_[],
                           q.direct_data_operation_[]],
                          [q.direct_data_operation_[],
                           q.direct_data_operation_[]]]
    """

    # 動作ループ
    for _ in range(2):  # ループ回数を決定
        for step in direct_query_list2: # 動作を決定
            # 一回の動作分のクエリを送信
            for query in step:
                driver.write(query)
                sleep(0.02)
                response = driver.read(16)
                print(response)
            # 動き終わるまで待機
            for query in q.remote_io_access:
                while(True):
                    driver.write(query)
                    sleep(0.02)
                    response = driver.read(16)
                    if(stop_rotation(driver, response)):
                        break
    # -------- -------- -------- --------
    print("## FINISH")
    driver.close()

# 高速原点復帰運転を行なう
def position_reset():
    driver = serial.Serial(port = '/dev/tty.usbserial-FT1GOG9N',
                           baudrate = 115200,
                           parity = serial.PARITY_EVEN,
                           timeout = 0.01)
    q = Queries()
    for query in q.high_speed_return_on:
        driver.write(query)
        sleep(0.02)
        response = driver.read(16)
    print("RETURNING...")
    sleep(3)
    for query in q.high_speed_return_off:
        driver.write(query)
        sleep(0.02)
        response = driver.read(16)
    print("RETURNED")

if __name__ == "__main__":
    main()
    position_reset()
