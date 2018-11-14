# -*- coding: utf-8 -*-

# スレーブアドレス設定
BROADCAST = 0
ANKLE_R = 1
ANKLE_L = 2
VERTICAL_SWING_R = 3
VERTICAL_SWING_L = 4
LATERAL_SWING_R = 5
LATERAL_SWING_L = 6

slaveAddressData = [b"\x00", # ブロードキャスト
                    b"\x01", # 足首 - 右
                    b"\x02", # 足首 - 左
                    b"\x03", # 足振り前後 - 右
                    b"\x04", # 足振り前後 - 左
                    b"\x05", # 足振り左右 - 右
                    b"\x06"] # 足振り左右 - 左

# ファンクションコード一覧
READ_REGISTER = 0
WRITE_REGISTER = 1
DIGNOSE = 2
WRITE_REGISTERS = 3
READ_WRITE_REGISTERS = 4

functionCodeData = [b"\x03", # 保持レジスタからの読み出し
                    b"\x06", # 保持レジスタへの書き込み
                    b"\x08", # 診断
                    b"\x10", # 複数の保持レジスタへの書き込み
                    b"\x17"] # 複数の保持レジスタの読み出し/書き込み

def createSlaveAddress():
    # モーター1台のため未実装
    # 00hでブロードキャスト
    # TODO 複数台のモーター制御
    return b"\x01"

def createFunctionCode(f):
    return functionCodeData[f]

def createData(fc, meth=0, pos=0, sp=0, strt=0, stp=0):
    if(fc == functionCodeData[READ_REGISTER]):
        ### リモートI/Oアクセス
        # レジスタアドレス007f, レジスタ数0001
        return b"\x00\x7f\x00\x01"
    elif(fc == functionCodeData[WRITE_REGISTERS]):
        ### ダイレクトデータ運転
        # 書き込みレジスタ先頭アドレス
        head_register_adress = b"\x00\x58"
        # 書き込みレジスタ数
        register_number = b"\x00\x10"
        # 書き込みバイト数
        byte_number = b"\x20"
        # 運転データNo.
        operation_data_no = b"\x00\x00\x00\x00"
        # 方式
        method = meth.to_bytes(4, "big")
        # 位置
        position = pos.to_bytes(4, "big")
        # 速度
        speed = sp.to_bytes(4, "big")
        # 起動・変速レート
        start_shift_rate = strt.to_bytes(4, "big")
        # 停止レート
        stop_rate = stp.to_bytes(4, "big")
        # 運転電流
        operating_current = b"\x00\x00\x03\xe8"
        # 反映トリガ
        reflect_trigger = b"\x00\x00\x00\x01"
        # データを作成
        result = head_register_adress + register_number + byte_number + \
                    operation_data_no + method + position + speed + \
                    start_shift_rate + stop_rate + operating_current + \
                    reflect_trigger
        return result

def test():
    sa = createSlaveAddress(ANKLE_R)
    fc = createFunctionCode(WRITE_REGISTERS)
    d = createData(fc, meth=2, pos=8500, sp=2000, strt=1500, stp=1500)
    query_without_crc = sa + fc + d
    # 結果を表示
    print(query_without_crc)

if __name__ == "__main__":
    test()
