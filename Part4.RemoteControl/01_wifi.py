from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time
import network  # import network
from io_map import IOMap

# input correct router ID and password
wifi_name = 'Harmony OS'  # input correct router ID
wifi_password = 'wificonnect'  # input correct router password

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)


def connect_wifi(lcd=None):

    print("Setup start")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_name, wifi_password)

    count = 0
    while not wlan.isconnected():
        time.sleep(1)
        count += 1
        print("Connecting to WiFi" + "." * (count % 4))

    ip = wlan.ifconfig()[0]
    print("Connected to WiFi, IP:", ip)

    if lcd is not None:
        lcd.putstr('ip:\n' + ip)


connect_wifi(lcd)
