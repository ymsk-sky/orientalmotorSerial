# -*- coding: utf-8 -*-

def get_x_data(position=0):
    result = b"\x01"
    result += b"\x02\x03"
    result += position.to_bytes(4, 'big', signed=True)
    return result

def main():
    print(get_x_data(1000))
    print(get_x_data(-1000))

if __name__ == "__main__":
    main()
