from machine import Pin, I2C
import ssd1306

# using default address 0x3C
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
display = ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)


display.text('hello world', 0, 0, 1)
# 先頭行に Hello World を印字
for i in range(10000):
    display.rotate(False)
    display.fill(0)
    display.text(f'{i}', 0, 0, 1)
    display.show()
