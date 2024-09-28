from machine import I2C, Pin
from i2c_lcd import I2cLcd
from io_map import IOMap
import time

# Initialize I2C and LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, IOMap["LCD"], 2, 16)

# Initialize button
button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)

# Initialize the counter
count = 0


def button_counter(button):
    global count  # Declare count as a global variable so it can be updated
    btnVal = button.value()

    if btnVal == 0:  # Button pressed
        time.sleep(0.01)  # Debouncing delay

        while button.value() == 0:  # Wait until button is released
            pass

        # Increment count after button is released
        count += 1

    return count


while True:
    # Get the current button count
    button_counter(button1)

    # Calculate whether the count is even or odd
    switch_state = count % 2

    # Clear the LCD and display the current switch state (0 or 1)
    lcd.clear()
    lcd.putstr(str(switch_state))  # Convert switch_state to string before displaying

    # Delay for 0.1 seconds
    time.sleep(0.1)
