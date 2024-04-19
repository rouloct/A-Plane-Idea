import pigpio
from signal_output import SignalOutput


class SignalInput:
    
    
    def __init__(self, pi: pigpio.pi, *, name: str = None, channel: int = None, pin: int = None, output: SignalOutput = None, error_threshold: int = 0) -> None:
        """ Initialize an input.

        Args:
            pi (pigpio.pi): The pi to connect to.
            name (str, optional): The signal input's name (used for print statements). Defaults to None.
            channel (int, optional): The signal input's channel (used for print statements). Defaults to None
            pin (int, optional): The input's pin between 1 and 31 using BCM. Defaults to None.
            output (SignalOutput, optional): The input's output to communicate with. Defaults to None.
            error_threshold (int, optional): Will not respond to a pulsewidth less than the error threshold distance from the last pulsewidth..
            e.g. if the last pulsewidth was 1500us and the threshold is 15, will not respond to the pulesewidths between 1485us and 1515us.
        """
        
        self._pi = pi
        self.name = name
        self.channel = channel
        self._pin = pin
        self._output = output
        self._error_threshold = error_threshold if error_threshold >= 0 else 0
        self._start_tick = None
        self._last_pulse_width = None
                
        if pin is None or type(pin) is not int or not (1 <= pin <= 31):
            print(f"Error: {self} initialization failed - Invalid pin: {pin}")
            return

        try:
            # Set pin to "Input" mode
            pi.set_mode(pin, pigpio.INPUT) 
            # Set callback to the method, calls it everytime the input pin receives PWM signal from the pin
            pi.callback(pin, pigpio.EITHER_EDGE, self._input_callback) 
        except pigpio.error:
            print(f"Error: {self} initialization failed - Unknown error.")
        else:
            print(f"{self} initialized.")
            self._pin = pin


    def _input_callback(self, pin: int, level: int, tick: float) -> None:
        """ Callback function for reading PWM input. Called when PWM signal is received.

        Args:
            pin (int): The pin number using BCM.
            level (int): ? 
            tick (float): ?
        """
        
        if level == 1:
            self._start_tick = tick
            return
        
        pulse_width = tick - self._start_tick
        
        if self._last_pulse_width is None or abs(pulse_width - self._last_pulse_width) > self._error_threshold:
            print(f"Pulse width {pulse_width}us received on {self}.")
            self._last_pulse_width = pulse_width
            self._manage_output(pulse_width)
            
            
    def _manage_output(self, pulse_width: int) -> None:
        """ Code to manage the output. Called by self._input_callback when PWM signal is received. 
        
        Separate function is used for clarity and readibility.

        Args:
            pulse_width (int): The pulse width received in microseconds.
        """
        if self._output:
            self._output.set_servo_value(value=pulse_width, is_angle=False)
    
        
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
        return f"Input [{desc}]"
