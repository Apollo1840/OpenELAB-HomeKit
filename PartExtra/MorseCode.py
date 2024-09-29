# import machine, time and LCD 
from machine import Pin, PWM
from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from io_map import IOMap

correct_password = "-.-"  # set a correct password

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)

button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)
button2 = Pin(IOMap["button_left"], Pin.IN, Pin.PULL_UP)

pwm = PWM(Pin(IOMap["servo_m"]))
pwm.freq(50)

time_pressing = 0
password = ""  # input password

lcd.putstr("Enter password")
while True:
    if (button1.value() == 0):
        sleep_ms(10)
        while (button1.value() == 0):  # until button release
            time_pressing = time_pressing + 1  # count the time that the button is pressed
            sleep_ms(200)  # delay 200ms
            if (button1.value() == 1):  # released
                input_char = "-" if time_pressing>3 else "."
                password += input_char

                lcd.clear()  # lcd.move_to(1, 1)
                lcd.putstr('{}'.format(password))

                time_pressing = 0

    btnVal2 = button2.value()
    if (btnVal2 == 0):
        if (password == correct_password):  # input the correct password
            lcd.clear()
            lcd.putstr("open")
            pwm.duty(128)  # the door will open
            password = ""  # clear password
            sleep_ms(1000)
        else:  # input a wrong password
            lcd.clear()
            lcd.putstr("error")
            pwm.duty(25)  # close the door
            sleep_ms(2000)
            lcd.clear()
            lcd.putstr("enter again")
            password = ""  # clear password
