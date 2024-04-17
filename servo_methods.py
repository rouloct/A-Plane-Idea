from global_vars import pi
import pigpio


def angle_to_pw(angle: int) -> int:
    """ Convert angle in [-90, 90] to a pulsewidth in [500, 2500].

    Args:
        angle (int): -90 represents left, 0 is middle, 90 is right.

    Returns:
        int: pulsewidth in microseconds.
    """
    
    pw_min = 500
    pw_max = 2500
    angle_min = -90
    angle_max = 90
    
    # If the angle is not in [-90, 90], set it to the nearest endpoint.
    angle = -90 if angle < -90 else 90 if angle > 90 else angle
    
    return (angle - angle_min) * (pw_max - pw_min) / (angle_max - angle_min) + pw_min


def set_servo_angle(pin: int, angle: int) -> None:
    """ Set the angle of a servo.

    Args:
        pin (int): The GPIO pin (using BCM)
        angle (int): The angle between -90 (left) and 90 (right)
    """
    
    pulse_width = angle_to_pw(angle)
    pi.set_servo_pulsewidth(user_gpio=pin, pulsewidth=pulse_width)
    print(f"Setting pin {pin} to {angle} degrees via pulse width of {pulse_width:.0f}us.")


def init_servo(pin: int) -> None:
    """ Setup a GPIO pin for input and set its angle to 0 degrees.

    Args:
        pin (int): The GPIO pin (using BCM)
    """
    
    print(f"Initializing GPIO pin {pin} for input...")
    pi.set_mode(gpio=pin, mode=pigpio.INPUT)
    set_servo_angle(pin=pin, angle=0)
    