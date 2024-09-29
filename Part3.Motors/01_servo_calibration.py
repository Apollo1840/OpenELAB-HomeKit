from machine import Pin, PWM
import time

TEST_SERVO_PIN = 26
TEST_BUTTON_PIN = 18

button = Pin(TEST_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
servo = PWM(Pin(TEST_SERVO_PIN))
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