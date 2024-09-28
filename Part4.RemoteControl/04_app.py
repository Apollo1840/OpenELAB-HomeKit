import network
import socket
import neopixel
import dht
import time
from machine import Pin, PWM, I2C, ADC
from i2c_lcd import I2cLcd
from io_map import IOMap

# Wi-Fi credentials
wifi_name = 'Harmony OS'  # input correct router ID
wifi_password = 'wificonnect'  # input correct router password

MUSIC_VOLUME = 5

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
            setInterval(getStatus, 1000); // Update every second
        }};
    </script>
</head>
<body>
    <span id='status'>Loading...</span>
</body>
</html>
'''

# Dictionary for musical note notation (C4, D4, E4, etc.)
rhythm_SPN = {
    "C4": 261,  # C4
    "D4": 294,  # D4
    "E4": 330,  # E4
    "F4": 349,  # F4
    "G4": 392,  # G4
    "A4": 440,  # A4
    "B4": 494,  # B4
    "C5": 523,  # C5
    "D5": 587,  # D5
    "E5": 659,  # E5
    "F5": 698,  # F5
    "G5": 784,  # G5
}

happy_birthday_melody_spn = [
    "G4", "G4", "A4", "G4", "C5", "B4",  # "Happy birthday to you"
    "G4", "G4", "A4", "G4", "D5", "C5",  # "Happy birthday to you"
    "G4", "G4", "G5", "E5", "C5", "B4", "A4",  # "Happy birthday dear [Name]"
    "F5", "F5", "E5", "C5", "D5", "C5"  # "Happy birthday to you"
]

# Define the color mappings
color_map = {
    'red': (255, 0, 0),
    'oringe': (200, 100, 0),
    'yellow': (200, 200, 0),
    'green': (0, 255, 0),
    'cyan': (0, 100, 255),
    'blue': (0, 0, 255),
    'purple': (100, 0, 255),
    'white': (255, 255, 255)
}

# Initialize peripherals
i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)
led = Pin(IOMap["led"], Pin.OUT)
leds = neopixel.NeoPixel(Pin(IOMap["led_rgb"]), 4)
gas = Pin(IOMap["gas"], Pin.IN, Pin.PULL_UP)
PIR = Pin(IOMap["PIR"], Pin.IN)
servo_window = PWM(Pin(IOMap["servo_n"]), freq=50)
servo_door = PWM(Pin(IOMap["servo_m"]), freq=50)
steam_sensor = ADC(Pin(IOMap["steam_sensor"]))
humid_temp_sensor = dht.DHT11(Pin(IOMap["humid_temp_sensor"]))
buzzer = PWM(Pin(IOMap["buzzer"]))
fan_ = PWM(Pin(IOMap["fan_"], Pin.OUT), 10000, 0)
fan = PWM(Pin(IOMap["fan"], Pin.OUT), 10000, 2)

# Set initial states
fan_.duty(0)
fan.duty(0)
buzzer.duty(0)
led.off()
leds.fill((0, 0, 0))
leds.write()
servo_door.duty(0)
servo_window.duty(0)
steam_sensor.atten(ADC.ATTN_11DB)
steam_sensor.width(ADC.WIDTH_12BIT)
lcd.clear()


# Function to handle requests
def handle_light_color(path):
    # Loop through the color map to handle on/off requests
    for color, rgb in color_map.items():
        if path == f'/{color}/on':
            conn.send(f'HTTP/1.1 200 OK\r\n\r\n{color} on')
            colorWipe(rgb, 50)
            return
        elif path == f'/{color}/off':
            conn.send(f'HTTP/1.1 200 OK\r\n\r\n{color} off')
            colorWipe((0, 0, 0), 50)
            return

    if path == '/sfx1/on':
        conn.send('HTTP/1.1 200 OK\r\n\r\nsfx1 on')
        rainbow(10)
    elif path == '/sfx1/off':
        conn.send('HTTP/1.1 200 OK\r\n\r\nsfx1 off')
        colorWipe((0, 0, 0), 50)
    elif path == '/sfx2/on':
        conn.send('HTTP/1.1 200 OK\r\n\r\nsfx2 on')
        theaterChaseRainbow(20)
    elif path == '/sfx2/off':
        conn.send('HTTP/1.1 200 OK\r\n\r\nsfx2 off')
        colorWipe((0, 0, 0), 50)


def play_tone():
    buzzer.freq(50)
    buzzer.duty(10)
    time.sleep(0.25)
    buzzer.duty(0)


# Function to play the melody using the rhythm dictionary
def play_melody(melody, rhythm_dict, volume=312):
    for note in melody:
        buzzer.freq(rhythm_dict[note])  # Set frequency based on the note
        buzzer.duty(volume)  # Set duty cycle to 50% for sound
        time.sleep(0.25)  # Play note for 0.25 seconds
        buzzer.duty(0)  # Turn off sound between notes
        time.sleep(0.05)  # Short delay between notes


def colorWipe(color, wait, n_leds=4):
    for i in range(n_leds):
        leds[i] = color
        leds.write()
        time.sleep_ms(wait)


def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def rainbow(wait, n_leds=4):
    for j in range(256):
        for i in range(n_leds):
            idx = int((i * 256 / n_leds) + j)
            leds[i] = wheel(idx & 255)
        leds.write()
        time.sleep_ms(wait)


def theaterChaseRainbow(wait, n_leds=4):
    for j in range(0, 256, 4):
        for q in range(3):
            for i in range(0, n_leds, 3):
                if i + q < n_leds:  # Ensure the index is within bounds
                    idx = (i + j) % 256
                    leds[i + q] = wheel(idx)
            leds.write()
            time.sleep_ms(wait)
            for i in range(0, n_leds, 3):
                if i + q < n_leds:  # Ensure the index is within bounds
                    leds[i + q] = (0, 0, 0)  # Turn off the LED


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

    try:
        path = str(conn.recv(1024)).split(' ')[1]
    except IndexError:
        path = '/'

    if "status" not in path:
        print(path)
        print('Got a connection from {}'.format(str(addr)))

    try:
        if path == '/':
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>ESP32 ip:' + ip + '</html>\r\n\r\n'
            conn.send(response)

        # LED control
        elif path == '/led/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nturn on the LED')
            led.on()
        elif path == '/led/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\nturn off the LED')
            led.off()

        # WINDOW control
        elif path == '/window/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nopen the window')
            servo_window.duty(77)  # Approximate duty for 2.5ms pulse (180 degrees)
        elif path == '/window/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\nclose the window')
            servo_window.duty(26)  # Approximate duty for 0.5ms pulse (0 degrees)

        # MUSIC control
        elif path == '/music/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nplay music')
        elif path == '/music/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\nplay music')
            play_melody(happy_birthday_melody_spn, rhythm_SPN, volume=MUSIC_VOLUME)

        # BUZZ control
        elif path == '/buz/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nbuzzer')
        elif path == '/buz/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')
            play_tone()

        # Door control
        elif path == '/door/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nopen the door')
            servo_door.duty(120)  # Adjust duty as needed
        elif path == '/door/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\nclose the door')
            servo_door.duty(20)  # Adjust duty as needed

        # Fan control
        elif path == '/fan/on':
            conn.send('HTTP/1.1 200 OK\r\n\r\nturn on the fan')
            fan.duty(700)
        elif path == '/fan/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\nturn off the fan')
            fan.duty(0)

        # LightShow control
        handle_light_color(path)

        # steam sensing
        if path == '/rain/on':
            rain_val = steam_sensor.read()
            conn.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(rain_val))
        elif path == '/rain/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')

        # gas sensing
        elif path == '/gas/on':
            gas_val = gas.value()
            if gas_val > 512:
                conn.send('HTTP/1.1 200 OK\r\n\r\ndangerous: {}'.format(gas_val))
            else:
                conn.send('HTTP/1.1 200 OK\r\n\r\nsafe')
        elif path == '/gas/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')

        # body sensing
        if path == '/body/on':
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + DYNAMIC_STATUS_PAGE.format("/body/status"))
        elif path == '/body/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')
        elif path == '/body/status':
            status = 'someone' if PIR.value() == 1 else 'no one'
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + status)

        # temperature and humidity sensing
        elif path == '/temp/on':
            humid_temp_sensor.measure()
            temp = humid_temp_sensor.temperature()
            conn.send('HTTP/1.1 200 OK\r\n\r\n{} 。C'.format(temp))
        elif path == '/temp/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')

        elif path == '/humidity/on':
            humid_temp_sensor.measure()
            humidity = humid_temp_sensor.humidity()
            conn.send('HTTP/1.1 200 OK\r\n\r\n{} %'.format(humidity))
        elif path == '/humidity/off':
            conn.send('HTTP/1.1 200 OK\r\n\r\noff')

    except OSError as e:
        if e.errno == 104:
            pass
    conn.close()
