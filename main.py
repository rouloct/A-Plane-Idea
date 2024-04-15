import pigpio
from gpiozero import Servo
from time import sleep

# Edit this list with the servos
PINS = [8, None, None, None]

SERVO_MIN_PW = 1000 # In microseconds
SERVO_MAX_PW = 2000


def set_servo_angle(servo: Servo, angle: int) -> None:
    angle = 0 if angle < 0 else 180 if angle > 180 else angle
    servo.value = (angle / 180) * (SERVO_MAX_PW - SERVO_MIN_PW) + SERVO_MIN_PW
    print(servo.value)


def main() -> None:
    servos: list[Servo] = [Servo(pin) for pin in PINS if pin is not None]
    pi: pigpio.pi = pigpio.pi()
    
    try:
        for servo in servos:
            print(1)
            set_servo_angle(servo=servo, angle=90)
            
        
        sleep(0.5)
        
        for servo in servos:
            print(2)
            
            set_servo_angle(servo=servo, angle=0)
            
        sleep(0.5)
        
        for servo in servos:
            print(3)
            
            set_servo_angle(servo=servo, angle=180)
        
    except Exception as e:
        print("EXCEPTION: ")
        print(e)
        for servo in servos:
            servo.close()
        
    
if __name__ == '__main__':
    main()
    