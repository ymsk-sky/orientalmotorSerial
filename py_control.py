# -*- coding: utf-8 -*-

import os
import serial
from time import sleep

import parameter as p

### シリアル通信クラス
# 基本機能のみ実装
# TODO: エラー時の処理
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
        elif(port_type == 'Arduino'):
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

    def flush_input(self, client):
        client.reset_input_buffer()

    def open_serial(self, client):
        print("### OPEN", client.port, "###")
        client.open()

    def close_serial(self, client):
        client.close()
        print("### CLOSED", client.port, "###")


class SlaveMotor():
    # スレーブアドレス一覧(仮)
    BROADCAST = 0
    ANKLE_R = 1
    ANKLE_L = 2
    VERTICAL_SWING_R = 3
    VERTICAL_SWING_L = 4
    LATERAL_SWING_R = 5
    LATERAL_SWING_L = 6

    slave_address_list = [b"\x00", b"\x01", b"\x02",
                          b"\x03", b"\x04", b"\x05", b"\x06"]

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

### クエリ作成クラス
# TODO: モーターが複数台になるとスレーブアドレスで管理するので実装
class QueryGeneration():
    def __init__(self):
        pass

    def __del__(self):
        pass

    # スレーブアドレスを返す
    def create_slave_address(self, slave=1):
        # 0はブロードキャストのためデフォルトは1とする
        SlaveMotor.slave_address_list[slave]
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
            result += position.to_bytes(4, "big", signed=True)
            # 7. 速度
            result += speed.to_bytes(4, "big", signed=True)
            # 8. 起動・変速レート
            result += start_shift_rate.to_bytes(4, "big", signed=True)
            # 9. 停止レート
            result += stop_rate.to_bytes(4, "big", signed=True)
            # 10. 運転電流(100.0[%]で固定)
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
            while(shift_number < 8):
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

### 既存の制御
# 呼び出すだけでクエリ作成から動作まですべて行なうように設計
# TODO: 割り込みで使用する（予定）
class ProvisionOperation(QueryGeneration):
    def __init__(self):
        pass

    def __del__(self):
        pass

    # 高速原点復帰運転
    def high_speed_return_to_origin_operation(self, client):
        ### 運転開始
        qg = QueryGeneration()
        # クエリ作成
        query = qg.create_slave_address()
        query += b"\x06\x00\x7d\x00\x10"
        query += qg.create_error_check(query)
        # クエリ送信
        client.write(query)
        standby()
        # レスポンスを読む
        response = client.read(size=16)
        standby()
        ### 運転終了まで待機(クエリを送信しレスポンスのMOVEを確認)
        query = makequery_remote_io_access(qg)
        while(True):
            client.write(query)
            standby()
            response = client.read(size=16)
            move = get_one_status(response, OutputStatus.MOVE)
            standby()
            if(move == 0):
                break
        ### 運転終了
        query = qg.create_slave_address()
        query += "\x06\x00\x7d\x00\x00"
        query += qg.create_error_check(query)
        client.write(query)
        standby()
        response = client.read(size=16)
        standby()

    # トルクモニタ
    # 現在のトルクを、励磁最大静止トルクに対する割合で示す。
    def get_torque_monitor(self, client):
        # register address: 上位: 214(00D6h), 下位: 215(00D7h)
        qg = QueryGeneration()
        query = qg.create_slave_address()
        query += b"\x03\x00\xd6\x00\x02"
        query += qg.create_error_check(query)
        client.write(query)
        standby()
        response = client.read(size=16)
        # response = b"\x01\x03\x04\x00\x00\x03\xe7\xba\x89" # 999
        # レスポンスの詳細不明（おそらく1=0.1[%]）
        percentage = ((response[3] << 24) + (response[4] << 16)
                      + (response[5] << 8) + response[6]) / 10
        print(response)
        print(percentage)
        standby()
        return percentage

    # ドライバ温度
    # 現在のドライバの温度を示す。(1 = Celsius 0.1 deg.)
    def get_driver_temperature(self, client):
        # register address: 上位: 248(00F8h), 下位: 249(00F9h)
        qg = QueryGeneration()
        query = qg.create_slave_address()
        query += b"\x03\x00\xf8\x00\x02"
        query += qg.create_error_check(query)
        client.write(query)
        standby()
        response = client.read(size=16)
        standby()
        temperature = ((response[3] << 24) + (response[4] << 16)
                       + (response[5] << 8) + response[6]) / 10
        return temperature

    # モーター温度
    # 現在のモーターの温度を示す。(1 = Celsius 0.1 deg.)
    def get_motor_temperature(self, client):
        # register address: 上位: 250(00FAh), 下位: 251(00FBh)
        qg = QueryGeneration()
        query = qg.create_slave_address()
        query += b"\x03\x00\xfa\x00\x02"
        query += qg.create_error_check(query)
        client.write(query)
        standby()
        response = client.read(size=16)
        standby()
        temperature = ((response[3] << 24) + (response[4] << 16)
                       + (response[5] << 8) + response[6]) / 10
        return temperature

class OutputStatus():
    # ドライバ出力状態一覧（ハイフンはアンダースコアに置換）
    M0_R = 0        # R-OUT0
    M1_R = 1        # R-OUT1
    M2_R = 2        # R-OUT2
    START_R = 3     # R-OUT3
    HOME_END = 4    # R-OUT4
    READY = 5       # R-OUT5
    INFO = 6        # R-OUT6
    ALM_A = 7       # R-OUT7
    SYS_BSY = 8     # R-OUT8
    AREA0 = 9       # R-OUT9
    AREA1 = 10      # R-OUT10
    AREA2 = 11      # R-OUT11
    TIM = 12        # R-OUT12
    MOVE = 13       # R-OUT13
    IN_POS = 14     # R-OUT14
    TLC = 15        # R-OUT15

# リモートI/Oの状態を一つ返す
def get_one_status(response, bit_number):
    #ドライバの出力のみを取得
    driver_output = (response[3] << 8) + response[4]
    # 目的の状態分だけ右シフトしてビット演算(&1)でマスク
    result = (driver_output >> bit_number) & 1
    # 結果を返す
    return result

def standby(term=0.02):
    sleep(term)

def makequery_remote_io_access(qg, action=READ_REGISTER):
    query = qg.create_slave_address()
    query += qg.create_function_code(action)
    query += qg.create_data(action)
    query += qg.create_error_check(query)
    return query

def makequery_direct_data_operation(qg, action=WRITE_REGISTERS,
                                    method=0, position=0, speed=0,
                                    start_shift_rate=0, stop_rate=0):
    query = qg.create_slave_address()
    query += qg.create_function_code(action)
    query += qg.create_data(action, method=method, position=position,
                            speed=speed, start_shift_rate=start_shift_rate,
                            stop_rate=stop_rate)
    query += qg.create_error_check(query)
    return query

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
    ### クエリ作成インスタンス生成
    qg = QueryGeneration()
    ### ドライバ状態確認
    function_data = READ_REGISTER
    query = makequery_remote_io_access(qg, function_data)
    # READY状態(READY=1)になるまで繰り返す
    while(True):
        # クエリ送信
        sc.write_serial(driver, query)
        standby()
        # レスポンスを読む
        response = sc.read_serial(driver, size=16)
        # リモートI/OのREADY状態を確認する
        ready = get_one_status(response, OutputStatus.READY)
        standby()
        if(ready == 1):
            # 準備完了なら準備ループを抜ける
            break
    # *** ループ開始 ***
    print("--- for loop ---")
    for _ in range(100):
        ### センサ値取得
        # 入力バッファをリセット
        sc.flush_input(arduino)
        # 生値（0~255の1byteコード）をシリアルリード
        raw_value = sc.read_serial(arduino, 1)
        # int値に変換（0~255の値）
        value = int.from_bytes(raw_value, 'big')
        pos = int(value * (7500 / 256))
        ### クエリ作成
        function_data = WRITE_REGISTERS
        query = makequery_direct_data_operation(qg, function_data,
                                                method=p.ABSOLUTE_POSITION,
                                                position=pos,
                                                speed=10000,
                                                start_shift_rate=1000000,
                                                stop_rate=1000000)
        ### モーター動作(ダイレクトデータ運転)
        # クエリ送信
        sc.write_serial(driver, query)
        standby()
        # レスポンスを読む
        response = sc.read_serial(driver, size=16)
        standby()
        ### モーターが動作中か確認する
        # クエリ作成
        function_data = READ_REGISTER
        query = makequery_remote_io_access(qg, function_data)
        while(True):
            # クエリ送信
            sc.write_serial(driver, query)
            standby()
            # レスポンス確認する
            response = sc.read_serial(driver, size=16)
            # リモートI/OのMOVEが0か確認する
            move = get_one_status(response, OutputStatus.MOVE)
            standby()
            if(move == 0):
                break
    # *** ループ終了 ***
    sc.close_serial(driver)
    sc.close_serial(arduino)
    print("##### FINISH #####")

if __name__ == "__main__":
    main()
