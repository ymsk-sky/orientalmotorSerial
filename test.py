# -*- coding: utf-8 -*-

DRIVE_OUTPUT_STATUS = ["M0_R", "M1_R", "M2_R", "START_R",
                       "HOME_END", "READY", "INFO", "ALM_A",
                       "SYS_BSY", "AREA0", "AREA1", "AREA2",
                       "TIM", "MOVE", "IN_POS", "TLC"]

# command = b"\x01\x03\x00\x7f\x00\x01"
command = b"\x01\x03\x02\xaf\x42\x45\x85"
drive_output = (command[3] << 8) + command[4]

print(drive_output)
print(bin(drive_output))
print("")

for x in range(16):
    ans = (drive_output >> x) & 1
    if ans:
        print(DRIVE_OUTPUT_STATUS[x] + "\t:ON")
    else:
        print(DRIVE_OUTPUT_STATUS[x] + "\t:OFF")
