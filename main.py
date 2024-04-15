import pigpio
from gpiozero import Servo
from time import sleep

# Edit this list with the servos
PINS = [None, None, None, None]

SERVO_MIN_PW = 1
SERVO_MAX_PW = 2


def set_servo_angle(servo: Servo, angle: int):
    angle = 0 if angle < 0 else 180 if angle > 180 else angle
    servo.value = (angle / 180) * (SERVO_MAX_PW - SERVO_MIN_PW) + SERVO_MIN_PW


def main() -> None:
    servos: list[Servo] = [Servo(pin) for pin in PINS]
    pi: pigpio.pi = pigpio.pi()
    
    try:
        for servo in servos:
            set_servo_angle(servo=servo, angle=90)
        
        sleep(0.5)
        
        for servo in servos:
            set_servo_angle(servo=servo, angle=0)
            
        sleep(0.5)
        
        for servo in servos:
            set_servo_angle(servo=servo, angle=180)
        
    except Exception:
        for servo in servos:
            servo.close()
        
    
if __name__ == '__main__':
    main()
    