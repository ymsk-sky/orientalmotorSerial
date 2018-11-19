# -*- coding: utf-8 -*-

import time
import concurrent.futures

a = 10

def func1():
    global a
    while(True):
        print(a)
        time.sleep(0.1)

def func2():
    global a
    while(True):
        a += 1
        print("func2: increment a")
        time.sleep(1)

def main():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(func1)
    executor.submit(func2)

def test():
    val = 2147483648
    val2 = 2147483648
    print(val)
    print(type(val))
    print(val2)
    print(type(val2))

if __name__ == "__main__":
    # main()
    test()
