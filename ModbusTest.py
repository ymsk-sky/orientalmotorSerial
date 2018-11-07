import serial

client = serial.Serial("/dev/tty.usbserial-FT1GOG9N", 115200, timeout=0.01, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
size = 16
print(client.name)
commando = b"\x01\x10\x18\x00\x00\x02\x04\x00\x00\x00\x02\xd8\x6e"
client.write(commando)
result = client.read(size)
print(result)
commando = b"\x01\x10\x18\x02\x00\x02\x04\x00\x00\x21\x34\xc1\xf1"
client.write(commando)
result = client.read(size)
print(result)
commando = b"\x01\x10\x18\x04\x00\x02\x04\x00\x00\x07\xd0\x5b\xf0"
client.write(commando)
result = client.read(size)
print(result)
commando = b"\x01\x10\x18\x06\x00\x02\x04\x00\x00\x05\xdc\xdb\x4c"
client.write(commando)
result = client.read(size)
print(result)
commando = b"\x01\x10\x18\x08\x00\x02\x04\x00\x00\x05\xdc\x5a\xc0"
client.write(commando)
result = client.read(size)
print(result)
commando = b"\x01\x10\x00\x7c\x00\x02\x04\x00\x00\x00\x08\xf5\x18"
client.write(commando)
result = client.read(size)
print('result')
commando = b"\x01\x10\x00\x7c\x00\x02\x04\x00\x00\x00\x00\xf4\xde"
client.write(commando)
result = client.read(size)
print(result)
client.close()
