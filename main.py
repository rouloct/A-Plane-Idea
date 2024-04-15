import RPi.GPIO as GPIO
import time
from classes import Servo


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("HI RORY!!!!")
    servo1 = Servo(18)

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
                servo1.set_duty_cycle(degrees)
                time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
    
    except Exception:
        GPIO.cleanup()
