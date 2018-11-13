# -*- coding: utf-8 -*-

# command = b"\x01\x03\x00\x7f\x00\x01"
command = b"\x01\x03\x02\xaf\x42\x45\x85"
drive_output = (command[3] << 8) + command[4]

print(drive_output)
print(bin(drive_output))
print("")

for x in range(16):
    ans = (drive_output >> x) & 1
    print(ans)
