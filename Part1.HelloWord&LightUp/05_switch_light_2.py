from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time
from io_map import IOMap

# Initialize I2C and LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Initialize button
led = Pin(IOMap["led"], Pin.OUT)
button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)
button2 = Pin(IOMap["button_left"], Pin.IN, Pin.PULL_UP)

# Initialize the counter
count = 0


def button_counter(button):
    global count  # Declare count as a global variable so it can be updated
    btnVal = button.value()

    if btnVal == 0:  # Button pressed
        time.sleep(0.01)  # Debouncing delay

        while button.value() == 0:  # Wait until button is released
            pass

        # Increment count after button is released
        count += 1

    return count


while True:
    # Get the current button count
    button_counter(button1)
    button_counter(button2)

    # Calculate whether the count is even or odd
    switch_state = count % 2

    if switch_state == 1:
        led.on()  # Turn LED on
    else:
        led.off()  # Turn LED off

    # Delay for 0.1 seconds
    time.sleep(0.1)
