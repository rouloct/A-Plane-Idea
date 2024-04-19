import pigpio
import traceback
from signal_output import OutputManager
from signal_input import InputManager

# Add pin numbers here. Pigpio uses BCM setup instead of Board.
AIL_SERVO_PIN = 15
AIL_INPUT_PIN = 21

ELE_SERVO_PIN = 18
ELE_INPUT_PIN = 16


def main() -> None:
    try:
        pi = pigpio.pi() # Setup pi
        
        # aileron = Servo(pi, name="Aileron", pin=AIL_SERVO_PIN) # Set output for aileron PWM.
        # Input(pi, name="Aileron", pin=AIL_INPUT_PIN, channel=1, servo=aileron) # Set input for aileron PWM.
        
        # elevator = Servo(pi, name="Elevator", pin=ELE_SERVO_PIN) # Set output for elevator PWM.
        # Input(pi, name="Elevator", pin=ELE_INPUT_PIN, channel=2, servo=elevator) # Set input for elevator PWM.
        om = OutputManager(pi=pi)
        im = InputManager(pi=pi, output_manager=om)
        
        im.add_input("Aileron", 1, 21, 0)
        
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
