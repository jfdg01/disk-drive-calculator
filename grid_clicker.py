import time
import pyautogui
from typing import Tuple, List


class GridClicker:
    def __init__(self, start_pos: Tuple[int, int], cell_size: Tuple[int, int], rows: int = 4, cols: int = 8):
        """
        Initialize GridClicker with grid parameters.

        Args:
            start_pos: (x, y) coordinates of the first cell (top-left)
            cell_size: (width, height) of each cell
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.start_pos = start_pos
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols

        # Safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.5  # Default pause between actions

    def get_cell_position(self, row: int, col: int) -> Tuple[int, int]:
        """Calculate the screen coordinates for a given grid position."""
        x = self.start_pos[0] + (col * self.cell_size[0])
        y = self.start_pos[1] + (row * self.cell_size[1])
        return (x, y)

    def click_position(self, x: int, y: int, duration: float = 0.2) -> None:
        """
        Click at the specified coordinates with smooth movement.

        Args:
            x: X-coordinate
            y: Y-coordinate
            duration: Time taken for mouse movement
        """
        # Move to position with smooth motion
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(0.1)  # Small pause to ensure movement is complete

        # Click and wait for action to register
        pyautogui.click()
        time.sleep(0.3)

    def click_all_cells(self, delay: float = 0.5) -> List[Tuple[int, int]]:
        """
        Click all cells in the grid systematically.

        Args:
            delay: Additional delay between clicks in seconds

        Returns:
            List of all clicked coordinates
        """
        clicked_positions = []

        print("Starting grid clicking sequence in 5 seconds...")
        print("Move mouse to upper-left corner to abort.")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    # Calculate position
                    x, y = self.get_cell_position(row, col)
                    print(f"\nClicking position ({row}, {col}) at coordinates ({x}, {y})")

                    # Click and record position
                    self.click_position(x, y)
                    clicked_positions.append((x, y))

                    # Additional delay between clicks
                    time.sleep(delay)

        except Exception as e:
            print(f"\nError during clicking sequence: {e}")

        return clicked_positions


def main():
    # Calculate cell size based on your provided coordinates
    start_pos = (260, 280)  # Top-left cell center
    horizontal_diff = 402 - 260  # Difference between adjacent columns
    vertical_diff = 465 - 280  # Difference between adjacent rows

    cell_size = (horizontal_diff, vertical_diff)

    # Create and run the clicker
    clicker = GridClicker(
        start_pos=start_pos,
        cell_size=cell_size,
        rows=4,
        cols=8
    )

    print(f"Grid Parameters:")
    print(f"Starting Position: {start_pos}")
    print(f"Cell Size: {cell_size}")
    print(f"Grid: {clicker.rows}x{clicker.cols}")

    # Start clicking sequence
    clicked_positions = clicker.click_all_cells(delay=0.1)

    print("\nClicking sequence complete!")
    print(f"Total positions clicked: {len(clicked_positions)}")


if __name__ == "__main__":
    main()