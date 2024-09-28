from machine import I2C, Pin
from i2c_lcd import I2cLcd
from io_map import IOMap

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.putstr('Hello World!')
