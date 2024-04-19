import pigpio
from signal_output import OutputManager


class SignalInput:
    
    
    def __init__(self, name: str, channel: int, pin: int, error_threshold: int = 0) -> None:
        self.name = name
        self.channel = channel
        self.pin = pin
        self.error_threshold = error_threshold if error_threshold >= 0 else 0
        self.start_tick = None
        self.last_pulsewidth = None
            
    
    def __str__(self) -> str:
        return f"SignalInput [{self.name}, Channel {self.channel}, Pin {self.pin}]"
    
    
class InputManager:
    
    def __init__(self, pi: pigpio.pi, output_manager: OutputManager) -> None:
        """ A class to manage SignalInputs

        Args:
            pi (pigpio.pi): The pi.
            input_manager (inputManager): The inputManager.
        """
        
        self._pi = pi
        self._output_manager = output_manager
        self._stopped = False # Emergency stop.
        self._inputs: list[SignalInput] = []
        
        print(f"\n*** EMERGENCY STOP *** \n Disabled.\n")
        
    
    def add_input(self, name: str, channel: int, pin: int, error_threshold: int = 0):
        """ Create a SignalInput. No duplicate names, channels, or pins.

        Args:
            name (str): The name of the input. Some names have special functions when their input is triggered (switches).
            channel (int): The channel of the input.
            pin (int): The pin of the input.
            error_threshold (int, optional): The pulsewidth error threshold for the input's response. Defaults to 0.
        """
        
        errors = []
        
        if type(name) is not str:
            errors.append(f"Invalid SignalInput name type: {type(name)}, name: {name}")
        elif any(input.name == name for input in self._inputs):
            errors.append(f"Duplicate SignalInput name: {name}")
            
        if type(channel) is not int:
            errors.append(f"Invalid SignalInput channel type: {type(channel)}, channel: {channel}")
        elif any(input.channel == channel for input in self._inputs):
            errors.append(f"Duplicate SignalInput channel: {channel}")
            
        if type(pin) is not int:
            errors.append(f"Invalid SignalInput pin type: {type(pin)}, pin: {pin}")
        elif pin < 1 or pin > 31:
            errors.append(f"Invalid SignalInput pin value: {pin}")
        elif any(input.pin == pin for input in self._inputs):
            errors.append(f"Duplicate SignalInput pin: {pin}")
            
        if len(errors) > 0:
            print("ERROR: SignalInput failed to initialize with the following errors-- ", end='')
            print(*errors, sep=' | ', end='.\n')
            
        try:
            input = SignalInput(name=name, channel=channel, pin=pin, error_threshold=error_threshold)
            self._pi.set_mode(gpio=pin, mode=pigpio.INPUT)
            self._pi.callback(pin, pigpio.EITHER_EDGE, self._input_callback) 
        except pigpio.error:
            print(f"ERROR: {input} failed to intialize with unknown exception.")
        else:
            self._inputs.append(input)
            print(f"{input} initialized successfully.")
            
            
    def _input_callback(self, pin: int, level: int, tick: float) -> None:
        """ Callback function for reading PWM input. Called when PWM signal is received.

        Args:
            pin (int): The pin number using BCM.
            level (int): ? 
            tick (float): ?
        """
        
        input = next((input for input in self._inputs if input.pin == pin), None)
        
        if input is None:
            print(f"ERROR: Failed callback on pin {pin}-- SignalInput not found.")
            return
        
        if level == 1:
            input.start_tick = tick
            return
        
        pulsewidth = tick - input.start_tick
        
        if input.last_pulsewidth is not None and abs(pulsewidth - input.last_pulsewidth) > input.error_threshold:
            self._last_pulse_width = pulsewidth
            self._manage_pulsewidth(input=input, pulsewidth=pulsewidth)
            
            
    def _manage_pulsewidth(self, input: SignalInput, pulsewidth: int) -> None:
        """ Called when receiving a valid pulsewidth in _input_callback. 

        Args:
            input (SignalInput): The SignalInput receiving the signal.
            pulsewidth (int): The pulsewidth received.
        """
                
        if input.name == "EMERGENCY_STOP":
            if self._stopped and pulsewidth < 1200:
                self._stopped = False
                print(f"Pulse width {pulsewidth}us received on {input}... ")
                print(f"\n*** EMERGENCY STOP *** \n Disabled.\n")
                
            elif not self._stopped and pulsewidth > 1200:
                self._stopped = True
                print(f"Pulse width {pulsewidth}us received on {input}... ")
                print(f"\n*** EMERGENCY STOP *** \n Enabled.\n")
                
        elif self._stopped is True:
            return
        
        else:
            print(f"Pulse width {pulsewidth}us received on {input}... ")
            self._output_manager.set_output_pulsewidth_by_name(name=input.name, pulsewidth=pulsewidth)
