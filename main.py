import pigpio
import traceback
from signal_output import OutputManager
from signal_input import InputManager

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
AIL_INPUT_PIN = 21
ELE_INPUT_PIN = 20
RUD_INPUT_PIN = 16
EMERGENCY_INPUT_PIN = 17

AIL_OUTPUT_PIN = 4
ELE_OUTPUT_PIN = 3
RUD_OUTPUT_PIN = 2


def main() -> None:
    try:
        pi = pigpio.pi() # Setup pi
        
        om = OutputManager(pi=pi)
        im = InputManager(pi=pi, output_manager=om)
        
        im.add_input(name='AILERON', channel=1, pin=AIL_INPUT_PIN, error_threshold=0)
        im.add_input(name='ELEVATOR', channel=2, pin=ELE_INPUT_PIN, error_threshold=0)
        im.add_input(name='RUDDER', channel=4, pin=RUD_INPUT_PIN, error_threshold=0)
        im.add_input(name='EMERGENCY_STOP', channel=5, pin=EMERGENCY_INPUT_PIN, error_threshold=25)
        
        om.add_output(name='AILERON', pin=AIL_OUTPUT_PIN)
        om.add_output(name='ELEVATOR', pin=ELE_OUTPUT_PIN)
        om.add_output(name='RUDDER', pin=RUD_OUTPUT_PIN)
        
        
        input("Program running... Press ENTER to stop\n") # Keep the program running.
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. ", end='')
    
    except Exception:
        traceback.print_exc()
        
    finally:
        print("Exiting program.")
        pi.stop() # Cleanup.


if __name__ == '__main__':
    main()
