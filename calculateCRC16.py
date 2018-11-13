# -*- coding: utf-8 -*-

# コマンドの末尾にCRC-16計算結果を正しく追加してそのコマンドを返す
def addCRC16(cmd):
    # CRC16でエラーチェック値を計算する
    crc = makeCRC16(cmd)
    # エラーチェック値をクエリの末尾に追加する
    # 上位と下位を入れ替える
    reversed = transposeHigherLower(crc)
    # エラーチェック値は下位→上位の順
    cmd = cmd + reversed
    return cmd

# CRC-16計算結果を返す
def makeCRC16(cmd):
    # ***** CRC-16の計算 *****
    crc_register = 0xFFFF
    for data_byte in cmd:
        # CRCレジスタとデータバイトのXOR
        tmp = crc_register ^ data_byte
        # シフト回数を記憶
        shift_num = 0
        # シフトが 8回になるまで繰り返す
        while(shift_num < 8):
            # ビット演算(&1)で1桁めのビットを特定
            if(tmp&1 == 1): # 桁あふれが1なら
                tmp = tmp >> 1
                shift_num += 1
                tmp = 0xA001 ^ tmp
            else:
                tmp = tmp >> 1
                shift_num += 1
        crc_register = tmp
    crc = crc_register.to_bytes(2, 'big')
    # ***********************
    return crc

# 2つのbyteを入れ替える
def transposeHigherLower(crc):
    # 文字列に置き換える
    tmp = crc.hex()
    # 入れ替え処理
    tmp = tmp[2:] + tmp[:2]
    # byte型に変換（型をbyteに戻す）
    re = bytes.fromhex(tmp)
    return re

def test():
    # データチェック以外のクエリ
    command = b"\x01\x03\x00\x7f\x00\x01"
    # 答え（手動入力）
    ans = command + b"\xb5\xd2"
    # CRC-16/Modbusを計算してクエリ作成
    command = addCRC16(command)
    # 結果を表示
    print(command)
    print(ans)

if __name__ == '__main__':
    test()
