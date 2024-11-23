import time
import keyboard
import pyautogui
import sys
from typing import Optional, Tuple


class MouseTracker:
    def __init__(self, interval: float = 0.5):
        """
        Initialize the MouseTracker.

        Args:
            interval: Time between position updates in seconds
        """
        self.interval = interval
        self.is_running = False
        self.last_position: Optional[Tuple[int, int]] = None

    def get_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        x, y = pyautogui.position()
        return (x, y)

    def track(self):
        """Start tracking mouse position."""
        print("Starting mouse position tracking...")
        print("Press 'q' to quit, 's' to save current position")
        print("\nMouse Positions:")

        self.is_running = True
        saved_positions = []

        try:
            while self.is_running:
                current_pos = self.get_position()

                # Only print if position has changed
                if current_pos != self.last_position:
                    print(f"\rCurrent Position: x={current_pos[0]}, y={current_pos[1]}     ", end="")
                    self.last_position = current_pos

                # Check for 'q' to quit
                if keyboard.is_pressed('q'):
                    print("\n\nQuitting...")
                    break

                # Check for 's' to save position
                if keyboard.is_pressed('s'):
                    saved_positions.append(current_pos)
                    print(f"\nSaved position {len(saved_positions)}: {current_pos}")
                    # Wait a bit to avoid multiple saves
                    time.sleep(0.3)

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\n\nTracking interrupted by user")
        finally:
            self.is_running = False

        # Print summary of saved positions
        if saved_positions:
            print("\nSaved Positions:")
            for i, pos in enumerate(saved_positions, 1):
                print(f"Position {i}: {pos}")

        return saved_positions


def main():
    tracker = MouseTracker(interval=0.5)
    saved_positions = tracker.track()

    if saved_positions:
        # If we have at least 2 positions, we can calculate cell size
        if len(saved_positions) >= 2:
            p1, p2 = saved_positions[:2]
            cell_width = abs(p2[0] - p1[0])
            cell_height = abs(p2[1] - p1[1])
            print(f"\nCalculated cell size: ({cell_width}, {cell_height})")
            print(f"Grid origin: {saved_positions[0]}")


if __name__ == "__main__":
    main()