from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time
import network  # import network
import socket
from io_map import IOMap

# input correct router ID and password
wifi_name = 'Harmony OS'  # input correct router ID
wifi_password = 'wificonnect'  # input correct router password

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)
led = Pin(IOMap["led"], Pin.OUT)


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


def create_server():
    # Create a TCP server socket
    addr = ('0.0.0.0', 80)  # Listen on all interfaces, port 80
    s = socket.socket()
    s.bind(addr)
    s.listen(1)  # Allow only 1 client connection
    print("Server listening on", addr)
    return s


connect_wifi(lcd)
s = create_server()

while True:
    conn, addr = s.accept()
    print('Got a connection from {}'.format(str(addr)))

    # path: command
    path = str(conn.recv(1024)).split(' ')[1]

    if path == '/led/on':
        led.on()
        # conn.send('HTTP/1.1 200 OK\r\n\r\nled is on')

    elif path == '/led/off':
        led.off()
        # conn.send('HTTP/1.1 200 OK\r\n\r\nled is off')
