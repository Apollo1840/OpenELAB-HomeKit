from machine import Pin
from io_map import IOMap

# Define button and LED pins
button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)  # Assuming the button is connected to GPIO 12
led = Pin(IOMap["led"], Pin.OUT)

# Main loop
while True:
    btn1_val = button1.value()  # Read the button state

    if btn1_val == 0:  # If button is pressed
        led.on()  # Turn LED on
    else:
        led.off()  # Turn LED off
