# 🚀 FlytBase Turtle PID Navigation

## 📌 Overview
This project implements **PID-based navigation** for a turtle in a 2D space, simulating **robotic path-following and grid-based movement**. 

The project consists of two main goals:

- **Goal 1:** Navigate to a goal position using **PID control** with adaptive acceleration and velocity control.
- **Goal 2:** Follow a **grid-based path**, ensuring smooth acceleration, deceleration, and controlled turns using **PID-based linear and angular velocity control**.

The project also includes **real-time visualization** of velocity, acceleration, and error metrics.

---

## 🏹 Goal 1: Turtle Navigation to a Goal 🎯
In **Goal 1**, the turtle starts at a **random position** and moves toward a **fixed goal** using **PID control**. The movement is based on **distance error** and **angular correction**, ensuring the turtle reaches the goal efficiently.

### 🔧 Implementation Details
1. **Random Turtle Spawn** → The turtle spawns in a **random quadrant**, at least **200 pixels away from the goal**.
2. **PID-Based Forward Movement** → The turtle moves toward the goal using **adaptive acceleration and velocity control**.
3. **PID-Based Turning** → If the turtle is not facing the goal, it first rotates using **angular velocity control**.
4. **Goal Detection** → The turtle stops once it reaches the goal.
5. **Real-Time Visualization** → Plots **distance error, velocity, and acceleration over time**.

### ⚙️ How PID Works in Goal 1
- **Proportional (`Kp`)** → Increases speed based on distance error.
- **Integral (`Ki`)** → Helps correct minor errors over time.
- **Derivative (`Kd`)** → Prevents overshooting by damping sudden changes.

#### 📌 **Equations for Velocity (`v`) and Angular Velocity (`ω`)**
