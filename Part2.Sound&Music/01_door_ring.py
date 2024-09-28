from machine import Pin, PWM
import time
from io_map import IOMap

DOORRING_VOLUME = 10

# Initialize button and buzzer
button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(IOMap["buzzer"]))
buzzer.duty(0)

# Main loop
while True:    
    while button1.value() == 1:  # Wait for button release
        pass

    buzzer.duty(DOORRING_VOLUME)  # Activate the buzzer
    buzzer.freq(600)
    time.sleep(0.5)

    buzzer.freq(400)
    time.sleep(0.5)

    buzzer.duty(0)  # Turn off the buzzer

