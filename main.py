import pigpio
import traceback
from servos import Servo
from inputs import Input

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
AIL_SERVO_PIN = 15
AIL_INPUT_PIN = 21

ELE_SERVO_PIN = 18
ELE_INPUT_PIN = 16


def main() -> None:
    
    try:
        pi = pigpio.pi()
        
        aileron = Servo(pi, name="Aileron", pin=AIL_SERVO_PIN)
                    
        Input(pi, name="Aileron", pin=AIL_INPUT_PIN, servo=aileron)
        
        elevator = Servo(pi, name="Elevator", pin=ELE_SERVO_PIN)
        
        Input(pi, name="Elevator", pin=ELE_INPUT_PIN, servo=elevator)
        
        input("Program running... Press ENTER to stop ")
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. ", end='')
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program.")
 
        pi.stop()
        exit()


if __name__ == '__main__':
    main()
