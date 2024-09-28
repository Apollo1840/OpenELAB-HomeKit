import neopixel
from machine import Pin
import time
from io_map import IOMap

# Define RGB colors
COLOR_RGB = {
    "red": [100, 0, 0],
    "green": [0, 100, 0],
    "blue": [0, 0, 100],
    "yellow": [100, 100, 0],
    "white": [100, 100, 100],
    "off": [0, 0, 0]
}

# Define NeoPixel pin and number of LEDs
leds = neopixel.NeoPixel(Pin(IOMap["led_rgb"], Pin.OUT), 4)


def show_color(color):
    for i in range(4):  # For each of the 4 LEDs
        leds[i] = color  # Set the color of each LED
    leds.write()  # Send the data to the NeoPixels


def lightshow(rgb_colors):
    for clr in rgb_colors:
        show_color(clr)
        time.sleep_ms(500)  # Delay before changing to the next color


# Main loop
while True:
    # Define a list of colors for the sequence
    rgb_colors = [
        COLOR_RGB["red"],
        COLOR_RGB["green"],
        COLOR_RGB["blue"],
        COLOR_RGB["yellow"],
        COLOR_RGB["white"],
        COLOR_RGB["off"]
    ]
    lightshow(rgb_colors)
