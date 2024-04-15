from global_vars import PI


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
    """ Set the angle of a servos.

    Args:
        pin (int): The gpio pin (using BCM)
        angle (int): The angle between -90 (left) and 90 (right)
    """
    
    PI.set_servo_pulsewidth(user_gpio=pin, pulsewidth=angle_to_pw(angle=angle))
    print(f"Setting pin {pin} to {angle} degrees.")
