from math import gcd

def lcm(a, b, precision=1e-5):
    if a == 0 or b == 0:
        return 0
    scale = 10 ** 5  # Scale to handle floating points
    a_scaled = int(a * scale)
    b_scaled = int(b * scale)
    result = abs(a_scaled * b_scaled) // gcd(a_scaled, b_scaled)
    return result / scale



