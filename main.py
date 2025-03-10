import turtle
from goal1 import ManualNavigation, PIDNavigation, PIDManualNavigation
from goal2 import GridNavigation  # Import new independent grid navigation

def main():
    """Main function to select and run the desired navigation mode."""
    print("Select Mode:")
    print("1 - Manual Navigation (Arrow Keys)")
    print("2 - PID Controlled Navigation (Click to Start)")
    print("3 - PID + Manual (PID Navigation with Interference)")
    print("4 - Grid Drawing with Accel/Decel Profile (Click to Start)")

    mode = input("Enter mode (1/2/3/4): ").strip()

    if mode == "1":
        print("Starting Manual Navigation Mode...")
        ManualNavigation()
    elif mode == "2":
        print("Starting PID Navigation Mode...")
        PIDNavigation()
    elif mode == "3":
        print("Starting PID + Manual Navigation Mode...")
        PIDManualNavigation()
    elif mode == "4":
        print("Starting Grid Drawing Mode with Acceleration/Deceleration Profile...")
        nav = GridNavigation()
        nav.start()

    else:
        print("Invalid mode! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
