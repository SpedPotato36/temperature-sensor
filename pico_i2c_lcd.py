from machine import I2C
from time import sleep_ms

class I2cLcd:
    def __init__(self, i2c, addr, rows, cols):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        sleep_ms(50)
        self.init_lcd()

    def write(self, data):
        self.i2c.writeto(self.addr, bytes([data | 0x08]))

    def toggle_enable(self, data):
        sleep_ms(1)
        self.write(data | 0x04)
        sleep_ms(1)
        self.write(data & ~0x04)
        sleep_ms(1)

    def send(self, data, mode=0):
        high = mode | (data & 0xF0)
        low = mode | ((data << 4) & 0xF0)
        self.write(high)
        self.toggle_enable(high)
        self.write(low)
        self.toggle_enable(low)

    def write_cmd(self, cmd):
        self.send(cmd, 0)

    def write_data(self, data):
        self.send(data, 1)

    def init_lcd(self):
        self.write_cmd(0x33)
        self.write_cmd(0x32)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.clear()

    def clear(self):
        self.write_cmd(0x01)
        sleep_ms(2)

    def move_to(self, col, row):
        addr = col + (0x40 * row)
        self.write_cmd(0x80 | addr)

    def putstr(self, string):
        for char in string:
            self.write_data(ord(char))