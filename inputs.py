import pigpio
from servos import Servo


class Input:
    def __init__(self, pi: pigpio.pi, *, name: str = None, pin: int = None, servo: Servo = None) -> None:
        """ Initialize an input.

        Args:
            pi (pigpio.pi): The pi to connect to.
            name (str, optional): The input's (used for print statements). Defaults to None.
            pin (int, optional): The input's pin between 1 and 31 using BCM. Defaults to None.
            servo(Servo, optional): The input's servo to communicate with. Defaults to None.
        """
        
        self._pi = pi
        self.name = name if name is not None else "Unnamed"
        self._pin = None
        self._servo = servo
        self._start_tick = None
                
        if pin is None or type(pin) is not int or not (1 <= pin <= 31):
            print(f"Error: {self} initialization failed - Invalid pin: {pin}")
            return

        try:
            pi.set_mode(pin, pigpio.INPUT)
            pi.callback(pin, pigpio.EITHER_EDGE, self._input_callback)
        except pigpio.error:
            print(f"Error: {self} initialization to pin {pin} failed - Unknown error.")
        else:
            print(f"{self} initialized on pin {pin}.")
            self._pin = pin


    def _input_callback(self, pin: int, level: int, tick: float) -> None:
        """ Callback function for reading PWM input.

        Args:
            pin (int): The pin number using BCM.
            level (int): ?
            tick (float): ?
        """
        
        if level == 1:
            self._start_tick = tick
        else:
            pulse_width = tick - self._start_tick
            print(f"Pulse width {pulse_width} received from pin {pin}.")
            self._manage_servo(pulse_width)
            
            
    def _manage_servo(pulse_width: int) -> None:
        # TODO
        pass
    
        
    def __str__(self) -> str:
        return f"Input [{self.name}, {self._pin}]" if self._pin is not None else f"Input [{self.name}]"
    
    
    