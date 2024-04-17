import pigpio
import traceback
from global_vars import PI
from helper_methods import set_servo_angle

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
PINS : list[int] = [15]


def main() -> None:
    """ Main execution block for program.
    
    Exceptions are handled in if __name__ == '__main__' instead to reduce nesting and improve readability.
    """
    
    for pin in PINS:
        PI.set_mode(gpio=pin, mode=pigpio.OUTPUT)
        set_servo_angle(pin=pin, angle=0)
    

if __name__ == '__main__':
    try:
        PI = pigpio.pi()
        main()
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program...")
        PI.stop()
        exit()
