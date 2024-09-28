import time
from machine import Pin, PWM
from io_map import IOMap

pwm_led_y = PWM(Pin(IOMap["led"], Pin.OUT), 10000, 0)

while True:
    pwm_led_y.init()
    for i in range(0, 1023):
        pwm_led_y.duty(i)
        time.sleep_ms(1)
    for i in range(1023, 0, -1):
        pwm_led_y.duty(i)
        time.sleep_ms(1)
    pwm_led_y.deinit()