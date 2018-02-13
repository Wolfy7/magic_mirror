#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

PIR_GPIO = 23 # Pin 16 (GPIO 23)

#Board Mode: Angabe der Pin-Nummer
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_GPIO, GPIO.IN)

def PIR_callback(channel):
    print("Es gab eine Bewegung")


print("Start....")

while True:
    print(GPIO.input(PIR_GPIO))
    time.sleep(0.1)


"""
try:
    GPIO.add_event_detect(PIR_GPIO, GPIO.RISING, callback=PIR_callback)
    while True:
        #pass
        #print("Test")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Beende...")
"""

GPIO.cleanup()

print("Ende....")
