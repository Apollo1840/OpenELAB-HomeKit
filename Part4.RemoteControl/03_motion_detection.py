import network
import socket
import time
from machine import Pin, PWM, I2C, ADC
from i2c_lcd import I2cLcd
import _thread
from io_map import IOMap

# Wi-Fi credentials
wifi_name = 'Harmony OS'  # input correct router ID
wifi_password = 'wificonnect'  # input correct router password

DYNAMIC_STATUS_PAGE = '''
<html>
<head>
    <script>
        function getStatus() {{
            fetch('{}')
                .then(response => response.text())
                .then(data => {{
                    document.getElementById('status').innerHTML = data;
                }});
        }}
        window.onload = function() {{
            getStatus();
            setInterval(getStatus, 500); // Update every half second
        }};
    </script>
</head>
<body>
    <span id='status'>Loading...</span>
</body>
</html>
'''

PIR = Pin(IOMap["PIR"], Pin.IN)
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
    print("Connected to WiFi, IP: {}".format(ip))

    if lcd is not None:
        lcd.putstr('ip:\n' + ip)
    return ip


def create_server():
    # Create a TCP server socket
    addr = ('0.0.0.0', 80)  # Listen on all interfaces, port 80
    s = socket.socket()
    s.bind(addr)
    s.listen(1)  # Allow only 1 client connection
    print("Server listening on", addr)
    return s


ip = connect_wifi(lcd)
s = create_server()

while True:
    conn, addr = s.accept()
    path = str(conn.recv(1024)).split(' ')[1]

    if "status" not in path:
        print('Got a connection from {}'.format(str(addr)))

    try:
        # body sensing
        if path == '/body/on':
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + DYNAMIC_STATUS_PAGE.format("/body/status"))
        elif path == '/body/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')
        elif path == '/body/status':
            status = 'someone' if PIR.value() == 1 else 'no one'
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + status)

    except OSError as e:
        if e.errno == 104:
            pass
    conn.close()
