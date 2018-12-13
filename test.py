# -*- coding: utf-8 -*-

import os
import serial
import time

import py_control as ctl

import sensor_test

# 高速原点回帰運動
def test1():
    sc = ctl.SerialCommunication()
    drv = serial.Serial()
    sc.set_serial(client=drv, port_type='MotorDriver', baudrate=115200,
                  parity='E', stopbits=1, timeout=0.01)
    sc.open_serial(drv)

    po = ctl.ProvisionOperation()
    po.high_speed_return_to_origin_operation(drv, slave=1)
    time.sleep(3)
    po.high_speed_return_to_origin_operation(drv, slave=2)

    sc.close_serial(drv)


def test2():
    head = b"\xFF"
    if(head == b"\xFF"):
        response = b"\x01\x11\x02\x22\x34"
        if(response == b"\x01\x11\x02\x22\x34"):
            data = response[:-1]
            raw = (int.from_bytes(data, "big") >> 1).to_bytes(len(data), "big")
            value_list = []
            for x in range(len(raw)):
                if(x%2 == 0):
                    value = (raw[x] << 8) + raw[x+1]
                    value_list.append(value)
            print(value_list)
if __name__ == "__main__":
    # test1()
    test2()
