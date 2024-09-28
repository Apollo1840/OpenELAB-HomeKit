from machine import Pin, PWM
import time
from io_map import IOMap

MUSIC_VOLUME = 5

# Dictionary for musical note notation (C4, D4, E4, etc.)
rhythm_SPN = {
    "C4": 261,  # C4
    "D4": 294,  # D4
    "E4": 330,  # E4
    "F4": 349,  # F4
    "G4": 392,  # G4
    "A4": 440,  # A4
    "B4": 494,  # B4
    "C5": 523,  # C5
    "D5": 587,  # D5
    "E5": 659,  # E5
    "F5": 698,  # F5
    "G5": 784,  # G5
}

twinkle_twinkle_melody_spn = [
    "C4", "C4", "G4", "G4", "A4", "A4", "G4",  # "Twinkle, twinkle, little star"
    "F4", "F4", "E4", "E4", "D4", "D4", "C4",  # "How I wonder what you are"
    "G4", "G4", "F4", "F4", "E4", "E4", "D4",  # "Up above the world so high"
    "G4", "G4", "F4", "F4", "E4", "E4", "D4",  # "Like a diamond in the sky"
    "C4", "C4", "G4", "G4", "A4", "A4", "G4",  # "Twinkle, twinkle, little star"
    "F4", "F4", "E4", "E4", "D4", "D4", "C4"  # "How I wonder what you are"
]

jingle_bells_melody_spn = [
    "E4", "E4", "E4",  # "Jingle bells"
    "E4", "E4", "E4",  # "Jingle bells"
    "E4", "G4", "C4", "D4", "E4",  # "Jingle all the way"
    "F4", "F4", "F4", "F4", "F4", "E4", "E4", "E4", "E4", "E4",  # "Oh what fun it is to ride"
    "E4", "D4", "D4", "E4", "D4", "G4"  # "In a one-horse open sleigh"
]

london_bridge_melody_spn = [
    "G4", "A4", "G4", "F4", "E4", "F4", "G4",  # "London Bridge is falling down"
    "D4", "E4", "F4",  # "Falling down"
    "G4", "E4", "F4", "G4", "E4", "F4", "G4",  # "London Bridge is falling down"
    "D4", "G4", "E4"  # "My fair lady"
]

happy_birthday_melody_spn = [
    "G4", "G4", "A4", "G4", "C5", "B4",  # "Happy birthday to you"
    "G4", "G4", "A4", "G4", "D5", "C5",  # "Happy birthday to you"
    "G4", "G4", "G5", "E5", "C5", "B4", "A4",  # "Happy birthday dear [Name]"
    "F5", "F5", "E5", "C5", "D5", "C5"  # "Happy birthday to you"
]

PIR = Pin(IOMap["PIR"], Pin.IN)
buzzer = PWM(Pin(IOMap["buzzer"]))
buzzer.duty(0)


# Function to play the melody using the rhythm dictionary
def play_melody(melody, rhythm_dict=rhythm_SPN, volume=512):
    for note in melody:
        buzzer.freq(rhythm_dict[note])  # Set frequency based on the note

        buzzer.duty(volume)
        time.sleep(0.25)  # Play note for 0.25 seconds

        buzzer.duty(0)  # Turn off sound between notes
        time.sleep(0.05)  # Short delay between notes


# Main loop
while True:
    motion = PIR.value()
    if motion == 1:
        # Play melody when motion is detected using solfège notation
        play_melody(twinkle_twinkle_melody_spn, rhythm_SPN, volume=MUSIC_VOLUME)
    else:
        buzzer.duty(0)  # Turn off the buzzer when no motion is detected
    time.sleep(0.2)
