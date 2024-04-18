import pigpio
import traceback
from global_vars import pi
from servos import Servo
from input_methods import init_input

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
AIL1_PIN = 15

INPUT_PIN : int = None


def main() -> None:
    global pi
    
    callback = None
    
    try:
        pi = pigpio.pi()
        
        ail1 = Servo(name="Aileron 1", pin=AIL1_PIN)
        
        if INPUT_PIN:
            callback = init_input(INPUT_PIN)
            input("Press any key to stop...") # Keep program running.
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program...")
        if callback:
            callback.cancel()
        pi.stop()
        exit()


if __name__ == '__main__':
    main()
