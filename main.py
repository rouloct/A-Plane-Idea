import pigpio
import traceback
from global_vars import pi
from servo_methods import init_servo
from input_methods import init_input

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
PINS : list[int] = [15]

INPUT_PIN : int = None


def main() -> None:
    global pi
    
    try:
        pi = pigpio.pi()
        
        for pin in PINS:
            init_servo(pin=pin)
        
        if INPUT_PIN:
            callback = init_input(INPUT_PIN)
            input("Press any key to stop...") # Keep program running.
        
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program...")
        callback.cancel()
        pi.stop()
        exit()

    

if __name__ == '__main__':
    main()
