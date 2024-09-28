# import machine, time, dht
import machine
import time
import dht
from machine import I2C, Pin, PWM
from i2c_lcd import I2cLcd
from io_map import IOMap

STATE2DUTY_DOOR = {
    "close": 18,
    "open": 38,  # 45 degree, + 1/4 * 180 duty_range
}
THRESHOLD_TEMPERATURE = 25
THRESHOLD_HUMIDITY = 50

pwm_door = PWM(Pin(IOMap["servo_m"]))
pwm_door.freq(50)

fan_ = PWM(Pin(IOMap["fan_"], Pin.OUT), 10000, 0)
fan = PWM(Pin(IOMap["fan"], Pin.OUT), 10000, 2)
fan_.duty(0)
fan.duty(0)

humid_temp_sensor = dht.humid_temp_sensor11(machine.Pin(IOMap["humid_temp_sensor"]))

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)

while True:
    humid_temp_sensor.measure()  # humid_temp_sensor11 mesures data for one time
    temperature = humid_temp_sensor.temperature()
    humidity = humid_temp_sensor.humidity()

    # call the built-in functions of humid_temp_sensor to attain temperature and humidity value, and print them on Shell

    lcd.move_to(1, 0)
    lcd.putstr('T= {} 。C'.format(time))

    lcd.move_to(1, 1)
    lcd.putstr('H= {} %'.format(humidity))

    if temperature > THRESHOLD_TEMPERATURE and humidity > THRESHOLD_HUMIDITY:
        pwm_door.duty(STATE2DUTY_DOOR["open"])
        fan.duty(700)

    else:
        pwm_door.duty(STATE2DUTY_DOOR["close"])
        fan.duty(0)

    time.sleep_ms(1000)
