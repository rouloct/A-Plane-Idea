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
            pi.set_mode(gpio=pin, mode=pigpio.OUTPUT)
        except pigpio.error:
            print(f"Error: {self} initialization to pin {pin} failed - Unknown error.")
        else:
            print(f"{self} initialized on pin {pin}.")
            self._pin = pin
            self.set_servo_angle(0)
            
    
    def set_servo_angle(self, angle: int) -> None:
        """ Set the servo's angle (-90 for left, 0 for middle, 90 for right), if valid.

        Args:
            angle (int): The angle between -90 and 90.
        """
        
        if self._pin is None:
            print(f"Error: Cannot set angle on {self} - No pin found.")
            return
        
        if type(angle) is not int or not (-90 <= angle <= 90):
            print(f"Error: Cannot set angle on {self} - Invalid angle: {angle}")
            return

        pw_min = 500
        pw_max = 2500
        angle_min = -90
        angle_max = 90
            
        pulse_width = (angle - angle_min) * (pw_max - pw_min) / (angle_max - angle_min) + pw_min
            
        try:
            self._pi.set_servo_pulsewidth(user_gpio=self._pin, pulsewidth=pulse_width)
            print(f"Setting {self} to {angle} degrees via pulse width of {pulse_width:.0f}us.")
        except pigpio.error:
            print(f"Error: Setting {self} to {angle} degrees via pulse width of {pulse_width:.0f}us failed - Unknown error.")


    def __str__(self) -> str:
        return f"Servo [{self.name}, {self._pin}]" if self._pin is not None else f"Servo [{self.name}]"
