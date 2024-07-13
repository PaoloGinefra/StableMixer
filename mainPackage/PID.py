class PID:
    def __init__(self, P: float, I: float, D: float, maxI: float):
        """This class implements a PID controller.

        Args:
            P (float): The proportional gain
            I (float): The integral gain
            D (float): The derivative gain
            maxI (float): The absolute maximum value for the integral term (to prevent windup)
        """
        self.P = P
        self.I = I
        self.D = D
        self.maxI = maxI
        self.integral: float = 0
        self.lastError: float = 0
        pass

    def getControl(self, error: float, dt: float) -> float:
        """This function calculates the control value for the given error and time step.

        Args:
            error (float): the error value
            dt (float): the time step

        Returns:
            float: the control value
        """
        self.integral += error * dt
        self.integral = max(min(self.integral, self.maxI), -self.maxI)
        return self.P * error + self.I * self.integral + self.D * (error - self.lastError) / dt
