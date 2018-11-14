# -*- coding: utf-8 -*-

class Test():
    __a = 10
    __b = 20
    c = 30

    def setVal(self, a=1, b=2, c=3):
        self.__a = a
        self.__b = b
        self.c = c
    def printVal(self):
        print(self.__a, self.__b, self.c)

def main():
    t = Test()
    t.printVal()
    t.setVal()
    t.printVal()
    t.setVal(b=1000)
    t.printVal()
    t.c = 333
    t.printVal()
    t.__a = 111
    t.printVal()
    print(t.__a)

if __name__ == "__main__":
    main()
