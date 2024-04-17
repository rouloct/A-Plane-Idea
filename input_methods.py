import pigpio
from global_vars import pi, start_tick


def input_callback(pin: int, level: int, tick: float) -> None:
    """ Callback function for reading PWM input.

    Args:
        pin (int): _description_
        level (int): _description_
        tick (float): _description_
    """
    
    if level == 1:
        global start_tick
        start_tick = tick
    else:
        pulse_width = tick - start_tick
        print(f"Pulse width {pulse_width} received from pin {pin}.")
        # TODO: Implement servo control.
    
    
def init_input(pin: int) -> pigpio._callback:
    """ Setup a GPIO for input for reading PWM signals.

    Args:
        pin (int): The GPIO pin (using BCM)

    Returns:
        pigio._callback: The callback function.
    """
    
    pi.set_mode(pin, pigpio.INPUT)
    return pi.callback(pin, pigpio.EITHER_EDGE, input_callback)
