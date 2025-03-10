import turtle
import time
from visualization import Visualization

class PIDController:
    """PID Controller with gradual acceleration transitions."""
    def __init__(self, kp, ki, kd, min_output, max_output, accel_rate=2.0):
        self.kp = kp  # Proportional Gain
        self.ki = ki  # Integral Gain
        self.kd = kd  # Derivative Gain
        self.min_output = min_output  # Lower bound (for deceleration)
        self.max_output = max_output  # Upper bound (for acceleration)
        self.accel_rate = accel_rate  # Maximum rate of change of acceleration (px/s³)
        self.prev_error = 0
        self.integral = 0
        self.current_acceleration = 0  # Smoothly controlled acceleration

    def compute(self, target, current, dt):
        """Compute the PID output with smooth acceleration changes."""
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error

        # Compute desired acceleration from PID
        desired_acceleration = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Gradually adjust acceleration within the allowed rate of change
        if desired_acceleration > self.current_acceleration:
            self.current_acceleration += min(self.accel_rate * dt, desired_acceleration - self.current_acceleration)
        else:
            self.current_acceleration -= min(self.accel_rate * dt, self.current_acceleration - desired_acceleration)

        # Clamp final acceleration within bounds
        self.current_acceleration = max(self.min_output, min(self.current_acceleration, self.max_output))

        return self.current_acceleration


class GridNavigation:
    def __init__(self):
        """Initialize the turtle and PID controllers."""
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color("black")
        self.turtle.speed(0)

        self.grid_size = 100  # Size of each grid square
        self.grid_steps = 4  # 4x4 grid
        self.time_elapsed = 0  # Cumulative time tracker

        # PID Controllers with acceleration limits
        self.velocity_pid = PIDController(kp=2.0, ki=0.1, kd=0.5, min_output=-3, max_output=15)
        self.angular_pid = PIDController(kp=1.5, ki=0.05, kd=0.3, min_output=-10, max_output=10)  # Adjusted for smooth turning

        # Real-time visualization
        self.visualization = Visualization()

    def move_with_pid(self, distance):
        """Move forward using PID control with limited acceleration and deceleration."""
        time_step = 0.1
        traveled = 0
        velocity = 0
        prev_velocity = 0

        while traveled < distance:
            # PID-controlled acceleration with limits (-3 to 15)
            acceleration = self.velocity_pid.compute(distance - traveled, velocity, time_step)
            velocity += acceleration * time_step

            step = velocity * time_step
            self.turtle.forward(step)
            traveled += step

            # Compute actual acceleration for visualization
            actual_acceleration = (velocity - prev_velocity) / time_step
            self.visualization.update(self.time_elapsed, velocity, actual_acceleration)

            # Update time and previous velocity
            self.time_elapsed += time_step
            prev_velocity = velocity
            time.sleep(time_step)

        self.turtle.forward(distance - traveled)  # Ensure exact stopping

    def turn_with_pid(self, angle):
        """Turn with controlled angular velocity."""
        time_step = 0.1
        rotated = 0
        angular_velocity = 0
        prev_angular_velocity = 0

        while abs(rotated) < abs(angle):
            # PID-controlled angular acceleration
            angular_acceleration = self.angular_pid.compute(angle - rotated, angular_velocity, time_step)
            angular_velocity += angular_acceleration * time_step

            turn_step = angular_velocity * time_step
            self.turtle.left(turn_step)
            rotated += turn_step

            # Update time
            self.time_elapsed += time_step
            time.sleep(time_step)

        self.turtle.left(angle - rotated)  # Ensure exact rotation

    def draw_grid(self):
        """Make the turtle draw a 4x4 grid while following the path closely."""
        for _ in range(self.grid_steps):
            for _ in range(self.grid_steps):
                self.move_with_pid(self.grid_size)  # Move forward
            self.turn_with_pid(90)  # Turn left
            self.move_with_pid(self.grid_size)  # Move to next row
            self.turn_with_pid(90)

        print("Grid Drawing Completed!")
        self.visualization.show()  # Show final visualization

    def start(self):
        """Start grid drawing mode."""
        print("Starting Grid Drawing with PID Control...")
        self.draw_grid()


# Run the navigation
if __name__ == "__main__":
    nav = GridNavigation()
    nav.start()
