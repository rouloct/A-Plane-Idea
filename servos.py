import pigpio

class Servo:
    def __init__(self, pi: pigpio.pi, *, name: str = None, pin: int = None) -> None:
        """ Initialize a servo.

        Args:
            pi (pigpio.pi): The pi to connect to.
            name (str, optional): The servo's name (used for print statements). Defaults to None.
            pin (int, optional): The servo's pin between 1 and 31 using BCM. Defaults to None.
        """
        
        self._pi = pi
        self.name = name if name is not None else "Unnamed"
        self._pin = None
        
        if pin is None or type(pin) is not int or not (1 <= pin <= 31):
            print(pin)
            print(f"Error: {self} initialization failed - Invalid pin: {pin}")
            return

        try:
            # Set pin's mode to output
            pi.set_mode(gpio=pin, mode=pigpio.OUTPUT) 
        except pigpio.error:
            print(f"Error: {self} initialization to pin {pin} failed - Unknown error.")
        else:
            print(f"{self} initialized on pin {pin}.")
            self._pin = pin
            # Set pin's angle to center.
            self.set_servo_value(value=0, is_angle=True)
            
    
    def set_servo_value(self, value: int, is_angle: bool) -> None:
        """ Set the servo's pulsewidth

        Args:
            value (int): The value (pulsewidth or angle)
            is_angle (bool): the value is an angle if True, otherwise it is a pulsewidth
        """
        
        if is_angle:
            pw_min = 500
            pw_max = 2500
            angle_min = -90
            angle_max = 90
                
            pulse_width = (value - angle_min) * (pw_max - pw_min) / (angle_max - angle_min) + pw_min
        else:
            pulse_width = value
    
        if self._pin is None:
            print(f"Error: Cannot set value on {self} - No pin found.")
            return
        
        if type(value) is not int or not (500 <= pulse_width <= 2500):
            print(f"Error: Cannot set value on {self} - Invalid value: {value}")
            return

        try:
            self._pi.set_servo_pulsewidth(user_gpio=self._pin, pulsewidth=pulse_width)
            print(f"Sending {self} pulse width of {pulse_width:.0f}us.")
        except pigpio.error:
            print(f"Error: Sending {self} pulse width of {pulse_width:.0f}us failed - Unknown error.")


    def __str__(self) -> str:
        return f"Servo [{self.name}, {self._pin}]" if self._pin is not None else f"Servo [{self.name}]"
