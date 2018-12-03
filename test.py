# -*- coding: utf-8 -*-

class A():
    def __init__(self):
        print("classA init")

    def a(self):
        print("classA a method")

class ChildA(A):
    def __init__(self):
        print("classChildA init")

    def child_a(self):
        A().a()
        print("classChildA child_a method")

def main():
    c = ChildA()
    c.child_a()

def a():
    response = b"\x01\x03\x04\x00\x00\x01\x7f\xba\x43"
    temperature = ((response[3] << 24) + (response[4] << 16)
                   + (response[5] << 8) + response[6]) / 10
    return temperature

def test():
    ans = a()
    print(ans, type(ans))

if __name__ == "__main__":
    # main()
    test()
