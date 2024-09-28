from machine import Pin, PWM
import time
from io_map import IOMap

ALERT_VOLUME = 3

PIR = Pin(IOMap["PIR"], Pin.IN)
buzzer = PWM(Pin(IOMap["buzzer"]))
buzzer.duty(0)

# Main loop
while True:
    motion = PIR.value()
    if motion == 1:

        # reaction
        buzzer.duty(ALERT_VOLUME)
        buzzer.freq(200)
        time.sleep(0.25)

    else:
        buzzer.duty(0)

    # framing delay
    time.sleep(0.2)