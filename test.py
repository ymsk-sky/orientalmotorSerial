# -*- coding: utf-8 -*-

# commando = b"\x01\x03\x00\x7f\x00\x01"
# commando = b"\x00\x01\x99\xa1\xaa\xff"
commando = b"\x01\x03\x00\x7f\x00\x01"

listo = bytearray(commando)
print(listo)

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

print(crc)

#print(listo[3].to_bytes(1, 'big'))
#print(listo[3].to_bytes(1, 'little'))

# print(data_byte.to_bytes(1, 'big'))
# print(format(0xFFFF, '016b'))
