# -*- coding: utf-8 -*-

# 文字列(str)へ一度変換してからCRC-16を計算する

def addCRC16(cmd):
    # CRC16でエラーチェック値を計算する
    crc = makeCRC16(cmd)
    # エラーチェック値をクエリの末尾に追加する
    # 上位と下位を入れ替える
    reversed = transposeHigherLower(crc)
    # エラーチェック値は下位→上位の順
    cmd = cmd + reversed
    return cmd

def makeCRC16(cmd):
    # bytearrayへ変換
    listo = bytearray(cmd)
    # ***** CRC-16の計算 *****
    crc_registor = 0xFFFF
    for data_byte in listo:
        # CRCレジスタとデータバイトのXOR
        tmp = crc_registor ^ data_byte
        # シフト回数を記憶
        shift_num = 0
        # シフトが 8回になるまで繰り返す
        while(shift_num < 8):
            if(tmp%2 == 1): # 桁あふれが1なら
                tmp = tmp >> 1
                shift_num += 1
                tmp = 0xA001 ^ tmp
            else:
                tmp = tmp >> 1
                shift_num += 1
        crc_registor = tmp
    crc = crc_registor.to_bytes(2, 'big')
    # ***********************
    return crc

def transposeHigherLower(crc):
    # 文字列に置き換える
    tmp = crc.hex()
    # 入れ替え処理
    tmp = tmp[2:] + tmp[:2]
    # byte型に変換（型をbyteに戻す）
    re = bytes.fromhex(tmp)
    return re

if __name__ == '__main__':
    commando = b"\x01\x03\x00\x7f\x00\x01"
    ans = b"\xb5\xd2"
    commando = addCRC16(commando)
    print(commando)
