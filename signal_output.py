import pigpio


class SignalOutput:
    
    
    def __init__(self, name: str, pin: int) -> None:
        self.name = name
        self.pin = pin
    

    def __str__(self) -> str:
        return f"SignalOutput [{self.name}, Pin {self.pin}]"




class OutputManager:
    
    __PW_MIN = 500
    __PW_MAX = 2500
    __ANGLE_MIN = -90
    __ANGLE_MAX = 90
    
    
    def __init__(self, pi: pigpio.pi ) -> None:
        """ A class to manage SignalOutputs. Should be a Singleton.

        Args:
            pi (pigpio.pi): The pi.
        """
        
        self._pi = pi
        self._outputs: list[SignalOutput] = []
        
    
    def add_output(self, name: str, pin: int) -> None:
        """ Create a SignalOutput. No duplicate names or pins.

        Args:
            name (str): The name of the output.
            pin (int): The pin (BWM) of the output.
        """
        
        errors = []
        
        if type(name) is not str:
            errors.append(f"Invalid SignalOutput name type: {type(name)}, name: {name}")
        elif any(output.name == name for output in self._outputs):
            errors.append(f"Duplicate SignalOutput name: {name}")
            
        if type(pin) is not int:
            errors.append(f"Invalid SignalOutput pin type: {type(pin)}, pin: {pin}")
        elif pin < 1 or pin > 31:
            errors.append(f"Invalid SignalOutput pin value: {pin}")
        elif any(output.pin == pin for output in self._outputs):
            errors.append(f"Duplicate SignalOutput pin: {pin}")
            
        if len(errors) > 0:
            print("ERROR: SignalOutput failed to initialize with the following errors-- ", end='')
            print(*errors, sep=' | ', end='.\n')
            
        try:
            output = SignalOutput(name=name, pin=pin)
            self._pi.set_mode(gpio=pin, mode=pigpio.OUTPUT)
        except pigpio.error:
            print(f"ERROR: {output} failed to intialize with unknown exception.")
        else:
            self._outputs.append(output)
            print(f"{output} initialized successfully.")
            # Set angle to center.
            
            
    def set_output_angle_by_name(self, name: str, angle: int) -> None:
        """ Change a SignalOutput's pulsewidth using its name and angle.

        Args:
            name (str): The SignalOutput's name.
            angle (int): The angle (in degrees).
        """
        
        pin = next((output.pin for output in self._outputs if output.name == name), None)
        if pin is None:
            print(f'ERROR: Could not set SignalOutput pulsewidth-- No SignalOutput with name {name}')
        else:
            pulsewidth = self._angle_to_puleswidth(angle=angle)
            self.set_output_pulsewidth_by_pin(pin=pin, pulsewidth=pulsewidth)
        
    
    def set_output_angle_by_pin(self, pin: int, angle: int) -> None:
        """ Change a SignalOutput's pulsewidth using its pin and angle.

        Args:
            pin (int): The SignalOutput's pin.
            angle (int): The angle (in degrees).
        """
        
        if not any(output.pin == pin for output in self._outputs):
            print(f"ERROR: Could not set SignalOutput pulsewidth-- No SignalOutput with pin {pin}")
        else:
            pulsewidth = self._angle_to_puleswidth(angle=angle)
            self.set_output_pulsewidth_by_pin(pin=pin, pulsewidth=pulsewidth)
    
    
    def set_output_pulsewidth_by_name(self, name: str, pulsewidth: int) -> None:
        """ Change a SignalOutput's pulsewidth using its name.

        Args:
            name (str): The SignalOutput's name
            pulsewidth (int): The pulsewidth (in microseconds).
        """
        
        pin = next((output.pin for output in self._outputs if output.name == name), None)
        if pin is None:
            print(f'ERROR: Could not set SignalOutput pulsewidth-- No SignalOutput with name "{name}"')
        else:
            self.set_output_pulsewidth_by_pin(pin=pin, pulsewidth=pulsewidth)
    
    
    def set_output_pulsewidth_by_pin(self, pin: int, pulsewidth: int) -> None:
        """ Change a SignalOutput's pulsewidth using its pin.

        Args:
            pin (int): The SignalOutput's pin.
            pulsewidth (int): The pulsewidth (in microseconds).
        """
        
        output = next((output for output in self._outputs if output.pin == pin), None)
        if output is None:
            print(f"ERROR: Could not set SignalOutput pulsewidth-- No SignalOutput with pin {pin}")
        elif type(pulsewidth) is not int or not (self.__PW_MIN <= pulsewidth <= self.__PW_MAX):
            print(f"ERROR: Could not set {output} pulsewidth-- Invalid pulsewidth of {pulsewidth}")
            return
        
        try:
            self._pi.set_servo_pulsewidth(user_gpio=pin, pulsewidth=pulsewidth)
            print(f"Sending {output} pulse width of {pulsewidth:.0f}us.")
        except pigpio.error:
            print(f"ERROR: Sending {output} pulse width of {pulsewidth:.0f}us failed - Unknown error.")
            
    
    
    def _angle_to_puleswidth(self, angle: int) -> int:
        """ Convert an angle to a pulsewidth between 500 and 2500.

        Args:
            angle (int): The angle. If not in [-90,90], set to the nearest endpoint.
        """
        
        
        if type(angle) is not int:
            angle = 0
        elif angle < self.__ANGLE_MIN:
            angle = self.__ANGLE_MIN
        elif angle > self.__ANGLE_MAX:
            angle = self.__ANGLE_MAX
            
        return (angle - self.__ANGLE_MIN) * (self.__PW_MAX - self.__PW_MIN) / (self.__ANGLE_MAX - self.__ANGLE_MIN) + self.__PW_MIN
        