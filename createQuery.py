# -*- coding: utf-8 -*-

READ_REGISTER = 0
WRITE_REGISTER = 1
DIGNOSE = 2
WRITE_REGISTERS = 3
READ_WRITE_REGISTERS = 4


functionCodeData = [b"\x03", b"\x06", b"\x08", b"\x10", b"\x17"]

def createSlaveAddress():
    # モーター1台のため未実装
    # 00hでブロードキャスト
    # TODO 複数台のモーター制御
    return b"\x01"

def createFunctionCode(f):
    return functionCodeData[f]

def createData(fc, me=0, pos=0, sp=0, strt=0, stp=0):
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
        method = me.to_bytes(4, "big")
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
    sa = createSlaveAddress()
    fc = createFunctionCode(WRITE_REGISTERS)
    d = createData(fc, me=2, pos=8500, sp=2000, strt=1500, stp=1500)
    query_without_crc = sa + fc + d
    # 結果を表示
    print(query_without_crc)

if __name__ == "__main__":
    test()
