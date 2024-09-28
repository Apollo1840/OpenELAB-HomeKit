from machine import Pin, PWM
from io_map import IOMap
import time

MUSIC_VOLUME = 5

PIR = Pin(IOMap["PIR"], Pin.IN)
buzzer = PWM(Pin(IOMap["buzzer"]))
buzzer.duty(0)

# Dictionary for solfège notation (do, re, mi, etc.)
rhythm = {
    "do": 261,  # C4
    "re": 294,  # D4
    "mi": 330,  # E4
    "fa": 349,  # F4
    "sol": 392,  # G4
    "la": 440,  # A4
    "si": 494,  # B4
    "high_do": 523,  # C5 (octave higher)
    "high_re": 587,  # D5
    "high_mi": 659,  # E5
    "high_fa": 698,  # F5
    "high_sol": 784,  # G5
}

# Define the Happy Birthday melody with just the solfège notes
melody = [
    "re", "la", "sol", "high_do", "si",
    "sol", "la", "sol", "high_re", "high_do",
    "sol", "high_sol", "high_mi", "high_do",
    "si", "la", "high_fa", "high_mi", "high_do",
    "high_re", "high_do"
]


# Function to play the melody using the rhythm dictionary
def play_melody(melody, rhythm_dict=rhythm, volume=512):
    for note in melody:
        buzzer.freq(rhythm_dict[note])  # Set frequency based on the note

        buzzer.duty(volume)  # Set duty cycle to 50% for sound
        time.sleep(0.25)  # Play note for 0.25 seconds

        buzzer.duty(0)  # Turn off sound between notes
        time.sleep(0.05)  # Short delay between notes

# Main loop
while True:
    motion = PIR.value()
    if motion == 1:
        # Play melody when motion is detected using solfège notation
        play_melody(melody, volume=MUSIC_VOLUME)
    else:
        buzzer.duty(0)  # Turn off the buzzer when no motion is detected
    time.sleep(0.2)
