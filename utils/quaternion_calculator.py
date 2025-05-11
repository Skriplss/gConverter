import math

class QuaternionCalculator:
    @staticmethod
    def euler_to_quaternion(x: float, y: float, z: float) -> tuple[float, float, float, float]:

        roll = math.radians(x)
        pitch = math.radians(y)
        yaw = math.radians(z)

        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        x = 0.0 if abs(x) < 1e-10 else round(x, 9)
        y = 0.0 if abs(y) < 1e-10 else round(y, 9)
        z = 0.0 if abs(z) < 1e-10 else round(z, 9)
        w = 0.0 if abs(w) < 1e-10 else round(w, 9)

        return x, y, z, w