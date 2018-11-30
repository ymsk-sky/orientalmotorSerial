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

if __name__ == "__main__":
    main()
