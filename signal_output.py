import pigpio


class SignalOutput:
    
    
    def __init__(self, pi: pigpio.pi, *, name: str = None, channel: int = -1, pin: int = None) -> None:
        """ Initialize a servo.

        Args:
            pi (pigpio.pi): The pi to connect to.
            name (str, optional): The signal output's name (used for print statements). Defaults to None.
            channel (int, optional): The signal output's channel (used for print statements). Defaults to None.
            pin (int, optional): The signal output's pin between 1 and 31 using BCM. Defaults to None.
        """
        
        self._pi = pi
        self.name = name
        self.channel = channel
        self._pin = pin
        
        if pin is None or type(pin) is not int or not (1 <= pin <= 31):
            print(pin)
            print(f"Error: {self} initialization failed - Invalid pin: {pin}")
            return

        try:
            # Set pin's mode to output
            pi.set_mode(gpio=pin, mode=pigpio.OUTPUT) 
        except pigpio.error:
            print(f"Error: {self} initialization failed - Unknown error.")
        else:
            print(f"{self} initialized.")
            self._pin = pin
            # Set pin's angle to center.
            self.set_servo_value(value=0, is_angle=True)
            
    
    def set_servo_value(self, value: int, is_angle: bool) -> None:
        """ Set the servo's pulsewidth

        Args:
            value (int): Pulsewidth in microseconds or angle in degrees
            is_angle (bool): the value is an angle if True, else pulsewidth
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
        desc = ""
        if self.name:
            desc += f'"{self.name}"'
        if self.channel:
            comma = ", " if desc else ""
            desc += f"{comma}Channel {self.channel}" 
        if self._pin:
            comma = ", " if desc else ""
            desc += f"{comma}Pin {self._pin}"
        if not desc:
            desc = "Unknown"
        return f"Output [{desc}]"
