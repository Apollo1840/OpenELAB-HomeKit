from machine import ADC, Pin, PWM
import time
from io_map import IOMap

STATE2DUTY_WINDOW = {
    "close": 18,
    "open": 128,
}
THRESHOLD_WET = 8100

pwm = PWM(Pin(IOMap["servo_f"]))
pwm.freq(50)

# set ADC to 0-3.3V
steam_sensor = ADC(Pin(IOMap["steam_sensor"]))
steam_sensor.atten(ADC.ATTN_11DB)
steam_sensor.width(ADC.WIDTH_12BIT)

try:
    while True:
        wet = steam_sensor.read()
        # print(wet)

        if (wet > THRESHOLD_WET):
            pwm.duty(STATE2DUTY_WINDOW["close"])  # close window
        else:
            pwm.duty(STATE2DUTY_WINDOW["open"])  # open window
        time.sleep(0.1)
except:
    pass
