# -*- coding: utf-8 -*-

crc = b"\xb5\xd2"

# 文字列に置き換える
tmp = crc.hex()
# 2文字(1バイトずつ)を入れ替える
tmp = tmp[2:] + tmp[:2]
# bytes型に変換
re = bytes.fromhex(tmp)

print(crc)
print(re)
