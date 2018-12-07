# -*- coding: utf-8 -*-

import os
import serial
import time

import py_control as ctl

def main():
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

if __name__ == "__main__":
    main()
