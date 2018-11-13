# -*- coding: utf-8 -*-

READ_REGISTER = 0
WRITE_REGISTER = 1
DIGNOSE = 2
WRITE_REGISTERS = 3
READ_WRITE_REGISTERS = 4


functionCode = [b"\x03", b"\x06", b"\x08", b"\x10", b"\x17"]

def createSlaveAddress():
    # モーター1台のため未実装
    # 00hでブロードキャスト
    # TODO 複数台のモーター制御
    return b"\x01"

def createFunctionCode(f):
    return functionCode[f]

def createData():
    # p.288
    pass

def test():
    sa = createSlaveAddress()
    fc = createFunctionCode(READ_REGISTER)
    d = createData()
    query_without_crc = sa + fc + d
    # 結果を表示
    print(query_without_crc)

if __name__ == "__main__":
    test()
