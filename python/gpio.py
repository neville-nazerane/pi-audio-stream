import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gpio_pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 0, 1, 5, 6, 12, 13, 19, 16, 26, 20, 21]

for pin in gpio_pins:
    GPIO.setup(pin, GPIO.OUT)

try:
    for pin in gpio_pins:
        print(f"Turning on Pin {pin}")
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        print(f"Turning off Pin {pin}")
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
