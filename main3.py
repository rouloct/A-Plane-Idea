import RPi.GPIO as GPIO
import time
import math

PWM_FREQ_HZ = 50 # PWM frequency in Hz

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.OUT)

p = GPIO.PWM(PIN, PWM_FREQ_HZ)

def deg_to_duty_cycle(deg):
    a = -90 # min degree
    b = 90 # max degree
    c = 3 # min duty
    d = 12 # max duty
    deg = a if deg < a else b if deg > b else deg

    return c + ((d - c) / (b - a)) * (deg - a)

p.start(deg_to_duty_cycle(-90))
time.sleep(0.5)


try:
    while True:
        for i in range(-90, 90):
            p.ChangeDutyCycle(deg_to_duty_cycle(i))
            time.sleep(abs(i) / 500)
        for i in range(90, -90, -1):
            p.ChangeDutyCycle(deg_to_duty_cycle(i))
            time.sleep(abs(i) / 500)

            

except KeyboardInterrupt:
    GPIO.cleanup()
