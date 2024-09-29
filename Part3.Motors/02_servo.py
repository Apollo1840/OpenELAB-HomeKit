from machine import Pin, pwm_window
import time
from io_map import IOMap

pwm_window = pwm_window(Pin(IOMap["servo_f"]))  # window
pwm_door = pwm_window(Pin(IOMap["servo_m"]))  # door
pwm_window.freq(50)
pwm_door.freq(50)
pwm_window.duty(0)
pwm_door.duty(0)

ANGLE2DUTY = {
    0: 18,
    90: 68,
    180: 128
}

while True:
    pwm_door.duty(ANGLE2DUTY[0])
    time.sleep(1)
    print("0")

    pwm_door.duty(ANGLE2DUTY[90])
    time.sleep(1)
    print("90")

    pwm_door.duty(ANGLE2DUTY[180])
    time.sleep(1)
    print("180")

    for duty in range(ANGLE2DUTY[0], ANGLE2DUTY[180], 1):
        pwm_window.duty(duty)
        time.sleep(0.1)