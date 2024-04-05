import RPi.GPIO as GPIO
from helper_methods import degrees_to_duty_cycle
from constants import DEFAULT_PWM_FREQUENCY_IN_HZ

class Servo:
    def __init__(self, pin: int, pwm_freq_hz: int = DEFAULT_PWM_FREQUENCY_IN_HZ) -> None:
        assert pin > 0, "pin must be > 0"
        assert pwm_freq_hz > 0, "pwm_freq_hz must be > 0"
        
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, pwm_freq_hz)
        self.pwm.start(degrees_to_duty_cycle(0))
        self.pin = pin
    
    
    def set_duty_cycle(self, degrees: float) -> None:
        self.pwm.ChangeDutyCycle(degrees_to_duty_cycle(degrees))
        print(f"Set degrees to {degrees} on pin {self.pin}")
        