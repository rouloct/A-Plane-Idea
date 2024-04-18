import pigpio
import traceback
from global_vars import pi
from servos import Servo
from inputs import Input

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
AIL1_SERVO_PIN = 15

AIL1_INPUT_PIN : int = 23


def main() -> None:
    
    try:
        pi = pigpio.pi()
        
        Servo(pi, name="Aileron 1", pin=AIL1_INPUT_PIN)
        Input(pi, name="Aileron 1", pin=23)
        
        input("Program running... Press ENTER to stop.")
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. ", end='')
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program...")
 
        pi.stop()
        exit()


if __name__ == '__main__':
    main()
