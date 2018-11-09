# -*- coding: utf-8 -*-

# response = b"\x01\x03\x00\x7f\x00\x01\xb5\xd2"

crc = b"\x66"

print(crc)

tmp = crc.decode()
print(tmp)
crc = tmp.encode()

print(crc)
print(type(crc))
