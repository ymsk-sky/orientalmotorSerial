# -*- coding: utf-8 -*-

# commando = b"\x01\x03\x00\x7f\x00\x01"
commando = b"\x01\x03\x02\xaf\x42\x45\x85"

print(bin(commando[3]))
print(bin(commando[4]))
print(bin((commando[3] << 8) + commando[4]))


#print(listo[3].to_bytes(1, 'big'))
#print(listo[3].to_bytes(1, 'little'))

# print(data_byte.to_bytes(1, 'big'))
# print(format(0xFFFF, '016b'))
