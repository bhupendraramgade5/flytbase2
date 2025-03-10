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
**v = K_v * distance_error * (1 / (1 + |angle_error| / 30)) ω = Kω * angle_error + Kω2 * (angle_error / (1 + |v|))**

This ensures that the turtle **accelerates quickly** but slows down when turning or close to the goal.

---

## 🏁 Goal 2: Grid-Based PID Navigation 🎯
In **Goal 2**, the turtle follows a **4x4 grid path** while ensuring:
✅ **Smooth Acceleration & Deceleration**  
✅ **Controlled Turns (Stop-and-Turn or Smooth Turning)**  
✅ **Strict Acceleration Limits (-3 to 15 px/s²)**  
✅ **Real-Time Visualization of Motion Data**  

### 🔧 Implementation Details
1. **PID-Based Acceleration & Deceleration**  
   - Acceleration **gradually increases** from 0 to 15 px/s².
   - Deceleration **smoothly decreases** from 0 to -3 px/s².
   - **No velocity cap**, but the turtle must stay **within grid bounds**.
  
2. **PID-Based Turning Control**  
   - **Smooth turns** when possible.  
   - **Stop-and-turn** when necessary (if facing the wrong way).  
   - Uses **angular velocity control** to ensure precise turns.

3. **Real-Time Visualization**  
   - **Velocity vs. Time**  
   - **Acceleration vs. Time**  
   - **Smooth transitions without hysteresis**

### ⚙️ How PID Works in Goal 2
- **Velocity PID Controller (`Kp`, `Ki`, `Kd`)**
  - Ensures smooth motion without sharp jumps.
  - Limits acceleration between **15 px/s² (max)** and **-3 px/s² (min).**
  - Starts from **0 and gradually reaches max acceleration**.

- **Angular PID Controller (`Kp`, `Ki`, `Kd`)**
  - Ensures turns are **smooth and precise**.
  - Controls **angular velocity** based on heading error.

#### 📌 **Equation for Smooth Acceleration**

