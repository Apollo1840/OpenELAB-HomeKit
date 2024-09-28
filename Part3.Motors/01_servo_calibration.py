from machine import Pin, PWM
import time

button = Pin(18, Pin.IN, Pin.PULL_UP)
servo = PWM(Pin(26))
servo.freq(50)

servo.duty(0)
time.sleep(1)

print("ready to start, please press the button")
while True:
    duty = 0
    while True:
        if button.value() == 0:
            duty += 1
            print(duty)
            servo.duty(duty)
            time.sleep(0.2)

"""
ANGLE2DUTY = {
    0: 18,
    90: 68,
    180: 128
}
"""