import turtle
import time
import matplotlib.pyplot as plt
# from visualization import Visualization

class Visualization:
    def __init__(self):
        """Initialize real-time plots."""
        plt.ion()  # Enable interactive mode
        self.fig, self.axs = plt.subplots(3, 1, figsize=(8, 9))

        # Velocity vs Time
        self.axs[0].set_title("Velocity vs Time")
        self.axs[0].set_xlabel("Time (s)")
        self.axs[0].set_ylabel("Velocity (px/s)")
        self.vel_line, = self.axs[0].plot([], [], label="Velocity", color="blue")
        self.axs[0].legend()
        self.axs[0].grid(True)

        # Acceleration vs Time
        self.axs[1].set_title("Acceleration vs Time")
        self.axs[1].set_xlabel("Time (s)")
        self.axs[1].set_ylabel("Acceleration (px/s²)")
        self.acc_line, = self.axs[1].plot([], [], label="Acceleration", color="red")
        self.axs[1].legend()
        self.axs[1].grid(True)

    def update(self, time_elapsed, velocity, acceleration):
        """Update the visualization with new data."""
        x_data = list(self.vel_line.get_xdata())
        y_vel_data = list(self.vel_line.get_ydata())
        y_acc_data = list(self.acc_line.get_ydata())

        x_data.append(time_elapsed)
        y_vel_data.append(velocity)
        y_acc_data.append(acceleration)

        self.vel_line.set_xdata(x_data)
        self.vel_line.set_ydata(y_vel_data)
        self.axs[0].relim()
        self.axs[0].autoscale_view()

        self.acc_line.set_xdata(x_data)
        self.acc_line.set_ydata(y_acc_data)
        self.axs[1].relim()
        self.axs[1].autoscale_view()

        plt.draw()
        plt.pause(0.001)  # Allow real-time updates without blocking

    def show(self):
        """Display the final plots after execution."""
        plt.ioff()  # Disable interactive mode
        plt.show()

# Run the navigation

