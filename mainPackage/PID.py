class PID:
    def __init__(self, P: float, I: float, D: float, maxI: float):
        """This class implements a PID controller.

        Args:
            P (float): The proportional gain
            I (float): The integral gain
            D (float): The derivative gain
            maxI (float): The absolute maximum value for the integral term (to prevent windup)
        """
        self.kP = P
        self.kI = I
        self.kD = D
        self.maxI = maxI
        self.integral: float = 0
        self.prevError: float = 0
        pass

    def getControl(self, target: float, volume, dt: float) -> float:
        """This function calculates the control value for the given error and time step.

        Args:
            target (float): the target value
            volume (float): the current value
            dt (float): the time step

        Returns:
            float: the control value
        """
        error = target - volume

        self.integral += error * dt
        self.integral = max(min(self.integral, self.maxI), -self.maxI)

        derivative = (error - self.prevError) / dt

        return self.kP * error + self.kI * self.integral + self.kD * derivative

    def setParams(self, P: float = None, I: float = None, D: float = None, maxI: float = None) -> None:
        """This function sets the parameters of the PID controller.

        Args:
            P (float): The proportional gain
            I (float): The integral gain
            D (float): The derivative gain
            maxI (float): The absolute maximum value for the integral term (to prevent windup)
        """
        if P is not None:
            self.kP = P
        if I is not None:
            self.kI = I
        if D is not None:
            self.kD = D
        if maxI is not None:
            self.maxI = maxI
        pass
