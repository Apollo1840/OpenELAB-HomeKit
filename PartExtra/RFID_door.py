# you need to upload the RFID_library/*.py s first
# IMPORTANT: check your own PASSKEY

from machine import Pin, PWM,I2C, Pin
import time
from mfrc522_i2c import mfrc522
from io_map import IOMap

PASSKEY = 656

pwm = PWM(Pin(IOMap["servo_n"]))
pwm.freq(50)

button1 = Pin(IOMap["button_right"], Pin.IN, Pin.PULL_UP)

#i2c config
addr = IOMap["RFID"]
scl = 22
sda = 21
    
rc522 = mfrc522(scl, sda, addr)
rc522.PCD_Init()
rc522.ShowReaderDetails()  # show detailed information about PCD - MFRC522 reader

data = 0

while True:
    if rc522.PICC_IsNewCardPresent():
        #print("Is new card present!")
        if rc522.PICC_ReadCardSerial() == True:
            print("Card UID:")
            #print(rc522.uid.uidByte[0 : rc522.uid.size])
            for i in rc522.uid.uidByte[0 : rc522.uid.size]:
                data = data + i
        print(data)
        if(data == PASSKEY):
            pwm.duty(128)
            print("open")
        else:
            print("error")
        data = 0
    btnVal1 = button1.value()
    if(btnVal1 == 0):
        pwm.duty(25)
        print("close")
    time.sleep(1)