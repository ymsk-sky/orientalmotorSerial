# -*- coding: utf-8 -*-

import os
import serial
from time import sleep


class SerialCommunication():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def set_serial(self, client,
                   port_type, baudrate,
                   bytesize=8, parity='N', stopbits=1, timeout=0.01):
        client.port = self.get_port(port_type)
        client.baudrate = baudrate
        client.bytesize = bytesize
        client.parity = parity
        client.stopbits = stopbits
        client.timeout = timeout

    def get_port(self, port_type):
        if(port_type == 'MotorDriver'):
            port = 'tty.usbserial'
        if(port_type == 'Arduino'):
            port = 'tty.usbmodem'
        else:
            print("cannot use port type")
            return
        for file in os.listdir('/dev'):
            if port in file:
                return '/dev/' + file
        return

    def write_serial(self, client, query):
        return client.write(query)

    def read_serial(self, client, size=1):
        return client.read(size)

    def open_serial(self, client):
        client.open()

    def close_serial(self, client):
        client.close()


# ファンクションコード設定
READ_REGISTER = 0
WRITE_REGISTER = 1
DIGNOSE = 2
WRITE_REGISTERS = 3
READ_WRITE_REGISTERS = 4

# ファンクションコードの通信データ一覧
function_code_data_list = [b"\x03", # 保持レジスタからの読み出し
                           b"\x06", # 保持レジスタへの書き込み
                           b"\x08", # 診断
                           b"\x10", # 複数の保持レジスタへの書き込み
                           b"\x17"] # 複数の保持レジスタの読み出し/書き込み

class QueryGeneration():
    def __init__(self):
        pass

    def __del__(self):
        pass

    # スレーブアドレスを返す
    def create_slave_address(self):
        # TODO: モーターが単一のため未実装
        # 複数台の制御になったら変更
        return b"\x01"

    # ファンクションコードを返す
    def create_function_code(self, function_code_data):
        return function_code_data_list[function_code_data]

    # データを作成し返す
    def create_data(self, function_code, method=0, position=0, speed=0,
                    start_shift_rate=0, stop_rate=0):
        if(function_code == READ_REGISTER): # リモートI/Oアクセス
            # レジスタアドレス:007f, レジスタ数:0001
            return b"\x00\x7f\x00\x01"
        elif(function_code == WRITE_REGISTERS): # ダイレクトデータ運転
            # 1. 書き込みレジスタ先頭アドレス
            result = b"\x00\x58"
            # 2. 書き込みレジスタ数
            result += b"\x00\x10"
            # 3. 書き込みバイト数
            result += b"\x20"
            # 4. 運転データNo.
            result += b"\x00\x00\x00\x00"
            # 5. 方式
            result += method.to_bytes(4, "big")
            # 6. 位置
            result += position.to_bytes(4, "big")
            # 7. 速度
            result += speed.to_bytes(4, "big")
            # 8. 起動・変速レート
            result += start_shift_rate.to_bytes(4, "big")
            # 9. 停止レート
            result += stop_rate.to_bytes(4, "big")
            # 10. 運転電流
            result += b"\x00\x00\x03\xe8"
            # 11. 反映トリガ
            result += b"\x00\x00\x00\x01"
            # データ完成
            return result

        # エラーチェックを返す
        def create_error_check(self, command):
            # CRC16/Modbusを計算する
            crc = self.calculate_crc16(command)
            # 上位と下位を入れ替える
            reversed = self.transpose_higher_lower(crc)
            return reversed

        # CRC16/Modbusを計算し返す
        ### リファクタリングプログラム有（Qiita参照）
        def calculate_crc16(self, command):
            # CRCレジスタ値を初期化
            crc_register = 0xFFFF
            for data_byte in command:
                # CRCレジスタとデータバイトの排他的論理和(XOR)
                tmp = crc_register ^ data_byte
                # シフト回数を記憶
                shift_number = 0
                # シフトが8回になるまで繰り返す
                while(shift_number > 8):
                    # ビット演算(&1)によるマスクで1桁目のビットを特定する
                    if(tmp & 1 == 1):
                        tmp = tmp >> 1
                        shift_number += 1
                        # A001htのXOR
                        tmp = 0xA001 ^ tmp
                    else:
                        tmp = tmp >> 1
                        shift_number += 1
                # CRCレジスタを更新する
                crc_register = tmp
            # 計算結果をbytes型へ変換する
            crc = crc_register.to_bytes(2, "big")
            return crc

        # 上位と下位を入れ替えて返す
        def transpose_higher_lower(self, crc):
            # 文字列に置き換える
            tmp = crc.hex()
            # 文字列の入れ替え処理
            tmp = tmp[2:] + tmp[:2]
            # byts型に変換（bytes型へ戻す）
            result = bytes.fromhex(tmp)
            return result


def standby(term=0.02):
    time.sleep(term)

def main():
    # シリアル通信インスタンスを生成
    sc = SerialCommunication()
    ### シリアル接続（モータードライバ）
    driver = serial.Serial()
    sc.set_serial(client=driver, port_type='MotorDriver',
                  baudrate=115200, parity='E', stopbits=1, timeout=0.01)
    sc.open_serial(driver)
    ### シリアル接続（マイコン）
    arduino = serial.Serial()
    sc.set_serial(client=arduino, port_type='Arduino',
                  baudrate=19200, parity='N', stopbits=1, timeout=None)
    sc.open_serial(arduino)
    ### クエリ作成
    qg = QueryGeneration()
    ### ドライバ状態確認
    while(True):
        pass
        if(True):
            break
    # *** ループ開始 ***
    while(True):
        ### センサ値取得
        ### クエリ作成
        ### モーター動作
        ### レスポンス確認
        pass
    # *** ループ終了 ***


if __name__ == "__main__":
    main()
