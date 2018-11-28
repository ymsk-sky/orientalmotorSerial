# -*- coding: utf-8 -*-

import os
import time
import serial

import parameter

class SerialCommunication():
    __client = serial.Serial()

    # シリアル設定
    def set_serial(self, pt='', br=115200, bs=8, to=0.01):
        self.__client.port = self.get_com_port(pt)
        self.__client.baudrate = br
        self.__client.bytesize = bs
        self.__client.timeout = to
        if(pt == 'MotorDriver'):
            self.__client.parity = serial.PARITY_EVEN
            self.__client.stopbits = serial.STOPBITS_ONE

    # 接続されているCOMポートを探す
    def get_com_port(self, pt):
        if(pt == 'MotorDriver'):
            pt = 'tty.usbserial'
        elif(pt == 'Arduino'):
            pt = 'tty.usbmodem'
        for file in os.listdir('/dev'):
            if pt in file:
                print(file)
                return '/dev/' + file
        return

    # クエリを送る
    def write_serial(self, query):
        self.__client.write(query)
        return query

    # レスポンスを読む
    def read_serial(self, size):
        return self.__client.read(size)

    # ポートのオープン
    def open_serial(self):
        self.__client.open()

    # ポートのクローズ
    def close_serial(self):
        self.__client.close()

class QueryGeneration():
    # スレーブアドレス設定
    BROADCAST = 0
    ANKLE_R = 1
    ANKLE_L = 2
    VERTICAL_SWING_R = 3
    VERTICAL_SWING_L = 4
    LATERAL_SWING_R = 5
    LATERAL_SWING_L = 6

    # ファンクションコード設定
    READ_REGISTER = 0
    WRITE_REGISTER = 1
    DIGNOSE = 2
    WRITE_REGISTERS = 3
    READ_WRITE_REGISTERS = 4

    # スレーブアドレスの通信データ一覧
    slave_address_data_list = [b"\x00", # ブロードキャスト
                               b"\x01", # 足首 - 右
                               b"\x02", # 足首 - 左
                               b"\x03", # 足振り前後 - 右
                               b"\x04", # 足振り前後 - 左
                               b"\x05", # 足振り左右 - 右
                               b"\x06"] # 足振り左右 - 左

    # ファンクションコードの通信データ一覧
    function_code_data_list = [b"\x03", # 保持レジスタからの読み出し
                               b"\x06", # 保持レジスタへの書き込み
                               b"\x08", # 診断
                               b"\x10", # 複数の保持レジスタへの書き込み
                               b"\x17"] # 複数の保持レジスタの読み出し/書き込み

    def create_slave_address(self):
        ##### スレーブアドレスを返す
        # 未実装：モーター複数台になったら変更
        return b"\x01"

    def create_function_code(self, function_code):
        ##### ファンクションコードを返す
        return self.function_code_data_list[function_code]

    def create_data(self, function_code, method=0, position=0, speed=0,
                    start_shift_rate=0, stop_rate=0):
        ##### データを返す
        if(function_code == self.READ_REGISTER):
            ##### リモートI/Oアクセス
            # レジスタアドレス007f, レジスタ数0001
            return b"\x00\x7f\x00\x01"
        elif(function_code == self.WRITE_REGISTERS):
            ##### ダイレクトデータ運転
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

    def create_crc16(self, command):
        ##### CRC-16方式によるエラーチェックを返す
        # CRC-16を計算
        crc = self.calculate_crc16(command)
        # 上位と下位を入れ替える
        reversed = self.transpose_higher_lower(crc)
        return reversed

    ### TODO: 使いづらい返り値なので後で消す ###
    def add_crc16(self, command):
        ##### CRC-16方式によるエラーチェックを加えたクエリを返す
        # CRC-16を計算
        crc = self.calculate_crc16(command)
        # 上位と下位を入れ替える
        reversed = self.transpose_higher_lower(crc)
        # エラーチェック値は下位→上位の順
        return command + reversed

    def calculate_crc16(self, command):
        ##### CRC-16の計算
        # CRCレジスタ値
        crc_register = 0xFFFF
        for data_byte in command:
            # CRCレジスタとデータバイトの排他的論理和(XOR)
            tmp = crc_register ^ data_byte
            # シフト回数を記憶
            shift_number = 0
            # シフトが8回になるまで繰り返す
            while(shift_number < 8):
                # ビット演算(&1)のマスクで1桁めのビットを特定
                if(tmp & 1 == 1):
                    tmp = tmp >> 1
                    shift_number += 1
                    # A001hとのXOR
                    tmp = 0xA001 ^ tmp
                else:
                    tmp = tmp >> 1
                    shift_number += 1
            # CRCレジスタを更新
            crc_register = tmp
        # 計算結果をbytes型へ変換
        crc = crc_register.to_bytes(2, "big")
        return crc

    def transpose_higher_lower(self, crc):
        ##### 2つのbytesを入れ替える
        # 文字列に置き換える
        tmp = crc.hex()
        # 入れ替え処理
        tmp = tmp[2:] + tmp[:2]
        # bytes型に変換（bytes型へ戻す）
        result = bytes.fromhex(tmp)
        return result

class Status():
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

    def get_one_status(self, response, bit_number):
        # ドライバの出力のみを取得
        driver_output = (response[3] << 8) + response[4]
        # 目的の状態分, 右シフトしてビット演算(&1)でマスク
        result = (driver_output >> bit_number) & 1
        return result

def standby(term=0.02):
    # クエリとレスポンスの間隔=0.02秒(20ms)
    time.sleep(term)

def serial_init(se, pt='', br=115200, bs=8, to=0.01):
    se.set_serial(pt, br, bs, to)
    try:
        se.open_serial()
    except:
        print("already opened", pt)

    print("##### START SERIAL", pt, "#####")

def direct_data():
    pass

def remote_io(query_gen):
    pass

def get_value(arduino):
    raw_val = arduino.read_serial(1)
    val = int.from_bytes(raw_val, 'big')
    # val is from 0(20) to 255
    return val

def main():
    ##### Arduino接続 #####
    ard = SerialCommunication()
    serial_init(ard, pt='Arduino', br=19200, to=None)
    ##### シリアル接続 #####
    ser = SerialCommunication()
    serial_init(ser, pt='MotorDriver')
    ##### 初期状態確認 #####
    # クエリ作成
    query_gen = QueryGeneration()
    action = query_gen.READ_REGISTER
    query = query_gen.create_slave_address()
    query += query_gen.create_function_code(action)
    query += query_gen.create_data(action)
    query += query_gen.create_crc16(query)
    # 確認：READY=1, MOVE=0, ALM_A=0
    st = Status()
    while(True):
        # クエリ送信
        ser.write_serial(query)
        # 一定時間待機
        standby()
        # レスポンスを読む
        response = ser.read_serial(16)
        # READYが1になるまで待機
        move = st.get_one_status(response, st.MOVE)
        standby()
        if(move == 0):
            break
    ##################################################
    #####             メインループ                 #####
    ##################################################
    for _ in range(5):
        ##### ダイレクトデータ運転 #####
        # クエリ作成
        action = query_gen.WRITE_REGISTERS
        query = query_gen.create_slave_address()
        query += query_gen.create_function_code(action)
        ### センサ値によってpositionを変更
        val = get_value(ard)
        p = val * 40    # 5000付近の値にスケーリング
        print(p)
        # 各コマンドの詳細はマニュアルp.292-293
        query += query_gen.create_data(action,
                                       method=2,
                                       position=p,
                                       speed=10000,
                                       start_shift_rate=1000000,
                                       stop_rate=1000000)
        query += query_gen.create_crc16(query)
        # クエリを送る
        ser.write_serial(query)
        standby()
        response = ser.read_serial(16)
        standby()
        ##### 状態確認 #####
        # クエリ作成：MOVE=0になるまでループ
        action = query_gen.READ_REGISTER
        query = query_gen.create_slave_address()
        query += query_gen.create_function_code(action)
        query += query_gen.create_data(action)
        query = query_gen.add_crc16(query)
        while(True):
            # クエリ送信
            ser.write_serial(query)
            # 一定時間待機
            standby()
            # レスポンスを読む
            response = ser.read_serial(16)
            # READYが1になるまで待機
            move = st.get_one_status(response, st.MOVE)
            print("moving")
            standby()
            if(move == 0):
                print("stop")
                time.sleep(1)
                break
    ##### 接続終了 #####
    ard.close_serial()
    ser.close_serial()
    print("##### closed serial #####")

if __name__ == "__main__":
    main()
