import turtle
import numpy as np
import random
import time
from visualization import Visualization

class Navigation:
    """Base class for all navigation modes."""

    def __init__(self,  Kp=0, Ki=1, Kd=0):
        """Initialize turtle and setup screen."""
        self.screen = turtle.Screen()
        self.screen.setup(width=400, height=400)
        self.screen.bgcolor("white")

        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color("black")
        self.turtle.speed(0)

        # Goal coordinates
        self.goal_x = 300
        self.goal_y = 300

        # PID parameters
        self.Kp = 0.01
        self.Ki = 0.01
        self.Kd = 0.01
        self.prev_error = 0
        self.integral = 0

        # Max speed
        self.max_speed = 50  

        self.spawn_turtle()
        self.draw_goal_marker()

    def spawn_turtle(self):
        """Spawn turtle in an opposite quadrant at least 200 pixels from the goal."""
        half_canvas = 400 // 2  # 200
        min_distance = 200
        margin = 50

        spawn_zones = [
            (-half_canvas + margin, half_canvas - margin),   # Top-left (-200, 200)
            (-half_canvas + margin, -half_canvas + margin),  # Bottom-left (-200, -200)
            (half_canvas - margin, -half_canvas + margin)    # Bottom-right (200, -200)
        ]

        valid_spawns = [
            (random.randint(x, x + 100), random.randint(y, y + 100))
            for x, y in spawn_zones
            if abs(self.goal_x - x) >= min_distance and abs(self.goal_y - y) >= min_distance
        ]

        start_x, start_y = random.choice(valid_spawns)
        self.turtle.penup()
        self.turtle.goto(start_x, start_y)
        self.turtle.pendown()

    def draw_goal_marker(self):
        """Draw a red circle around the goal."""
        marker = turtle.Turtle()
        marker.hideturtle()
        marker.speed(0)
        marker.penup()
        marker.goto(self.goal_x, self.goal_y - 20)
        marker.pendown()
        marker.pensize(2)
        marker.pencolor("red")
        marker.circle(20)
    
    def close_screen(self):
        """Close the turtle screen after a delay."""
        time.sleep(1)
        self.screen.bye()  # Closes the turtle graphics window

class ManualNavigation(Navigation):
    """Manual control using arrow keys."""

    def __init__(self):
        super().__init__()
        self.key_states = {"Up": False, "Down": False, "Left": False, "Right": False}
        self.bind_keys()
        self.run()

    def bind_keys(self):
        """Bind key events for movement."""
        self.screen.listen()
        for key in ["Up", "Down", "Left", "Right"]:
            self.screen.onkeypress(lambda k=key: self.set_key_state(k, True), key)
            self.screen.onkeyrelease(lambda k=key: self.set_key_state(k, False), key)

    def set_key_state(self, key, state):
        """Update key press state."""
        self.key_states[key] = state

    def run(self):
        """Move turtle based on key presses."""
        speed = 5

        while True:
            dx, dy = 0, 0
            if self.key_states["Up"]: dy += speed
            if self.key_states["Down"]: dy -= speed
            if self.key_states["Left"]: dx -= speed
            if self.key_states["Right"]: dx += speed

            if dx or dy:
                angle = np.degrees(np.arctan2(dy, dx))
                self.turtle.setheading(angle)
                self.turtle.forward(np.sqrt(dx**2 + dy**2))

            if self.reached_goal():
                print("Goal Reached!")
                break

            self.screen.update()
            time.sleep(0.05)

        self.screen.mainloop()

    def reached_goal(self):
        """Check if the turtle has reached the goal."""
        x, y = self.turtle.position()
        if np.linalg.norm([self.goal_x - x, self.goal_y - y]) < 5:
            print("Goal Reached!")
            self.close_screen()
            return True
        return False
    
class PIDNavigation(Navigation):
    """PID control to move the turtle to the goal."""

    def __init__(self,  Kp=0.2, Ki=0.5, Kd=0):
        super().__init__( Kp, Ki, Kd)
        self.start_button = turtle.Turtle()
        self.visualizer = Visualization([], [], [])
        # self.start_time = None

        self.setup_start_button()
        self.screen.mainloop()
        # self.start_time = None

    def setup_start_button(self):
        """Creates a start button on the turtle screen."""
        self.start_button.penup()
        self.start_button.goto(0, -150)
        self.start_button.write("Click to Start PID", align="center", font=("Arial", 14, "bold"))
        self.screen.onclick(self.start_pid)

    def start_pid(self, x, y):
        """Begins PID-based movement when the user clicks."""
        self.start_button.clear()
        self.start_time = time.time()
        self.move_to_goal_pid()
    
    def move_to_goal_pid(self):
        """Move the turtle to the goal using adaptive velocity control."""
        while True:
            x, y = self.turtle.position()
            goal_angle = np.degrees(np.arctan2(self.goal_y - y, self.goal_x - x))
            current_angle = self.turtle.heading()
            angle_error = (goal_angle - current_angle + 180) % 360 - 180

            distance_error = np.linalg.norm([self.goal_x - x, self.goal_y - y])
            time_elapsed = time.time() - self.start_time

            if distance_error < 5:
                print("Goal Reached!")
                self.close_screen()
                break

            dt = time.time() - self.start_time
            v, ω = self.compute_pid(distance_error, dt, angle_error)

            # **Prioritize Rotation if Facing Away from Goal**
            if abs(angle_error) > 30:
                v *= 0.5  # Reduce forward speed if heading is very wrong

            # **Apply Controls**
            self.turtle.left(ω)
            self.turtle.forward(v)

            self.visualizer.update(time_elapsed, distance_error, v)
            self.screen.update()
            time.sleep(0.05)

        self.visualizer.show()



    def move_to_goal_pid2(self):
        """Moves turtle to goal using PID control."""
        # self.start_time = time.time()
        
        while True:
            x, y = self.turtle.position()
            error = np.linalg.norm([self.goal_x - x, self.goal_y - y])
            time_elapsed = time.time() - self.start_time
            

            if error < 5:
                print("Goal Reached!")
                self.close_screen()
                break
            dt = time.time() - self.start_time

            speed = min(self.compute_pid(error, dt), self.max_speed)
            self.turtle.setheading(self.turtle.towards(self.goal_x, self.goal_y))
            self.turtle.forward(speed)

            self.visualizer.update(time_elapsed, error, speed)

            self.screen.update()
            time.sleep(0.05)
        self.visualizer.show()

    def compute_pid(self, distance_error, dt, angle_error):
        """Compute linear velocity (v) and angular velocity (ω) dynamically."""
        self.integral += distance_error * dt
        derivative = (distance_error - self.prev_error) / dt if dt > 0 else 0

        # **Dynamic Linear Velocity (v) based on distance and ω**
        Kv = 0.8  # Adjust for faster acceleration
        v = Kv * distance_error * (1 / (1 + abs(angle_error) / 30))  # Reduce v if angle error is large

        # **Dynamic Angular Velocity (ω) based on angle error**
        Kω = 0.1  # Base correction
        Kω2 = 0.05  # Extra term to ensure ω is strong when v is high
        ω = Kω * angle_error + Kω2 * (angle_error / (1 + abs(v)))

        # **Limit ω to avoid extreme turning**
        ω = max(min(ω, 20), -20)  

        self.prev_error = distance_error
        return v, ω



    def compute_pid2(self, error, dt):
        """Compute PID control output."""
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        self.prev_error = error
        return min(output, self.max_speed)

class PIDManualNavigation(PIDNavigation, ManualNavigation):
    """PID control with manual interference."""
    def __init__(self):
        PIDNavigation.__init__(self)
        # ManualNavigation.__init__(self)
        self.key_states = {"Up": False, "Down": False, "Left": False, "Right": False}
        self.bind_keys()
        
        # self.start_time = None
        self.setup_start_button2()  # Ensure start button is set up properly
        self.screen.mainloop()

    def setup_start_button2(self):
        """Override start button to ensure it calls start_pid from this class."""
        self.start_button.penup()
        self.start_button.goto(0, -150)
        self.start_button.write("Click to Start PID + Manual", align="center", font=("Arial", 14, "bold"))
        self.screen.onclick(self.start_pid2)  # Ensure this class's method is called

    def start_pid2(self, x, y):
        """Start PID + Manual mode when the Start Button is clicked."""
        self.start_button.clear()
        self.start_time = time.time()
        self.run()  # Start PID + Manual Navigation

    def bind_keys(self):
        """Bind key events for manual interference."""
        self.screen.listen()
        for key in ["Up", "Down", "Left", "Right"]:
            self.screen.onkeypress(lambda k=key: self.set_key_state(k, True), key)
            self.screen.onkeyrelease(lambda k=key: self.set_key_state(k, False), key)
    
    def run2(self):
        """Move turtle using combined PID control and manual input."""
        self.start_time = time.time()
        visualizer2 = Visualization([], [], [])
        # start_time = time.time()

        while True:
            x, y = self.turtle.position()
            error = np.linalg.norm([self.goal_x - x, self.goal_y - y])
            time_elapsed = time.time() - self.start_time

            if error < 5:
                print("Goal Reached!")
                self.close_screen()
                break

            # PID control
            
            dt = time.time() - self.start_time
            
            pid_speed = self.compute_pid(error, dt)
            self.turtle.setheading(self.turtle.towards(self.goal_x, self.goal_y))
            self.turtle.forward(min(pid_speed, self.max_speed))

            # Manual control
            dx, dy = 0, 0
            if self.key_states["Up"]: dy += 5
            if self.key_states["Down"]: dy -= 5
            if self.key_states["Left"]: dx -= 5
            if self.key_states["Right"]: dx += 5

            if dx != 0 or dy != 0:
                angle = np.degrees(np.arctan2(dy, dx))
                self.turtle.setheading(angle)
                self.turtle.forward(np.sqrt(dx**2 + dy**2))
            
            actual_speed = min(pid_speed, np.sqrt(dx**2 + dy**2))
            visualizer2.update(time_elapsed, error, actual_speed)

            self.screen.update()
            time.sleep(0.05)


            self.screen.update()
            time.sleep(0.05)
        self.visualizer2.show()

    def run(self):
        """Move turtle using combined PID control and manual angular control."""
        self.start_time = time.time()
        visualizer2 = Visualization([], [], [])

        while True:
            x, y = self.turtle.position()
            goal_angle = np.degrees(np.arctan2(self.goal_y - y, self.goal_x - x))
            current_angle = self.turtle.heading()
            angle_error = (goal_angle - current_angle + 180) % 360 - 180

            error = np.linalg.norm([self.goal_x - x, self.goal_y - y])
            time_elapsed = time.time() - self.start_time

            if error < 5:
                print("Goal Reached!")
                self.close_screen()
                break

            dt = time.time() - self.start_time
            pid_v, pid_ω = self.compute_pid(error, dt, angle_error)

            # Manual control for angular velocity (ω)
            manual_ω = 0
            if self.key_states["Left"]: 
                manual_ω -= 3  # Rotate counterclockwise
            if self.key_states["Right"]: 
                manual_ω += 3  # Rotate clockwise

            ω = pid_ω + manual_ω  # Combine PID and manual control
            ω = max(min(ω, 10), -10)  # Limit rotation speed

            # Manual control for linear velocity (v)
            manual_v = 0
            if self.key_states["Up"]: 
                manual_v += 2
            if self.key_states["Down"]: 
                manual_v -= 2

            v = pid_v + manual_v
            v = min(v, self.max_speed)  # Cap max speed

            # Apply control
            self.turtle.left(ω)
            self.turtle.forward(v)

            visualizer2.update(time_elapsed, error, v)
            self.screen.update()
            time.sleep(0.05)

        visualizer2.show()


