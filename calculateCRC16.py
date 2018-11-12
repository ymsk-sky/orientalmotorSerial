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
    # 1バイト毎のリストを作成
    byte_list = toListOfByte(cmd)
    # CRC-16の計算
    for b in byte_list:
        crc = b"\xd2\xb5"
    return crc

def transposeHigherLower(crc):
    # 文字列に置き換える
    tmp = crc.hex()
    # 入れ替え処理
    tmp = tmp[2:] + tmp[:2]
    # byte型に変換（型をbyteに戻す）
    re = bytes.fromhex(tmp)
    return re

def toListOfByte(cmd):
    # 文字列へ変換
    cmd_hex = cmd.hex()
    # 2文字(1バイト)毎のリストに変換
    byte_list = [cmd_hex[i: i+2] for i in range(0, len(cmd_hex), 2)]
    return byte_list

if __name__ == '__main__':
    commando = b"\x01\x03\x00\x7f\x00\x01"
    ans = b"\xb5\xd2"
    commando = addCRC16(commando)
    print(commando)
