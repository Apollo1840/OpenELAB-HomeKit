# Configuration on PC

### Step 1: Install Thonny

Run command: 

```bash
    sudo apt update
    sudo apt install thonny -y
```

### Step 2: Burn MicroPython Firmware to ESP32 to Enable Python on ESP32

First install esptool to burn the firmware.

```bash
    sudo apt install python3-pip
    pip3 install esptool --user
```

    # Action: Plug-in: PC --(USB-Type C Cable)-- ESP32 Board

Then find the location of the device.

```bash
    ls /dev/ttyUSB*   # note the location, eg. /dev/ttyUSB0
```
    
Burn the firmware to the location(eg. `/dev/ttyUSB0`).

```bash
    # (un-tested)
    # assuming you are in ./OpenELAB-HomeKit, if not, navigate to there
    sudo esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ./Python/firmware/esp32-20210903-v1.17.bin
```

Open the Thonny, we are going to set ESP32 Board as the interpreter.

    # Action: Press: Win button on your PC
    # Action: Type: thonny
    # Action: Type: Enter Button (when you see Thonny app)

In the menu bar, you will see the `Run` panel.
    
    # (un-tested)
    # Action: Click: (Menu) Tools > Options > interpreter
    # Action: Select: MicroPython(ESP32)

Now you are done. It is highly recommended to open the file views.

    # Action: Click: (Menu) View > Files

## Appendix

### Install CH340 Driver

```bash
    # (un-tested)
    cd ./Python/firmware/CH341SER_LINUX/driver
    sudo make
    sudo make load
    cd ..
    cd ..
    cd ..
    cd ..
```