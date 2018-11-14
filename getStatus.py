# -*- coding: utf-8 -*-

class Status():
    # ドライバ出力状態一覧（ハイフンはアンダースコアに置換）
    M0_R = 0        # R-OUT0
    M1_R = 1        # R-OUT1
    M2_R = 2        # R-OUT2
    START_R = 3     # R-OUT3
    HOME_END = 4    # R-OUT4
    READY = 5       # R-OUT5
    INFO = 6        # R-OUT6
    ALM_A = 7       # R-OUT7
    SYS_BSY = 8     # R-OUT8
    AREA0 = 9       # R-OUT9
    AREA1 = 10      # R-OUT10
    AREA2 = 11      # R-OUT11
    TIM = 12        # R-OUT12
    MOVE = 13       # R-OUT13
    IN_POS = 14     # R-OUT14
    TLC = 15        # R-OUT15

    def getAllStatus(self, cmd):
        drive_output = (cmd[3] << 8) + cmd[4]

    def getOneStatus(self, cmd, bit_num):
        drive_output = (cmd[3] << 8) + cmd[4]
        result = (drive_output >> bit_num) & 1
        return result

    def get_one_status(self, response, bit_number):
        # ドライバの出力のみを取得
        driver_output = (response[3] << 8) + response[4]
        # 目的の状態分, 右シフトしてビット演算(&1)でマスク
        result = (driver_output >> bit_number) & 1
        return result

    def printReady(self, r):
        print(self.READY)
        print(r)

def test():
    st = Status()
    command = b"\x01\x03\x02\xaf\x42\x85"
    for x in range(16):
        print(type(st.getOneStatus(command, x)))
    print("")
    for x in range(16):
        print(st.get_one_status(command, x), end="")
    print("")
    print(st.READY)
    print("")
    st.printReady(st.READY)

if __name__ == "__main__":
    test()
