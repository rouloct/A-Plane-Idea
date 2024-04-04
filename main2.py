import RPi.GPIO as GPIO
import time

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

p.start(deg_to_duty_cycle(0))
time.sleep(0.5)


try:
    while True:
        user_cmd = input('')

        cmds = {
            'a': -90, 
            'q': -45, 
            's':0,
            'd': 90, 
            'e': 45, 
        }

        degrees = cmds.get(user_cmd)

        if degrees is not None:
            p.ChangeDutyCycle(deg_to_duty_cycle(degrees))
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
