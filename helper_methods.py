def degrees_to_duty_cycle(degrees: float = 0) -> float:
    a = -90 # min degree
    b = 90 # max degree
    c = 3 # min duty
    d = 12 # max duty
    deg = a if deg < a else b if deg > b else deg

    return c + ((d - c) / (b - a)) * (deg - a)