import json
import os
import time
import pydirectinput
from typing import Dict, Tuple
from stat_beautifier import beautify_stats
from constants import MAIN_STAT_REGION, SUB_STAT_REGION, RESOLUTION

# Import the capture and parsing functions from main.py
from main import (
    calculate_region_pixels,
    capture_region,
    parse_main_stat,
    parse_sub_stats,
)


class DiskScanner:
    def __init__(self, grid_origin: Tuple[int, int], cell_size: Tuple[int, int],
                 rows: int = 4, cols: int = 8):
        """
        Initialize the DiskScanner with grid parameters.

        Args:
            grid_origin: (x, y) coordinates of the top-left corner of the grid
            cell_size: (width, height) of each grid cell
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.grid_origin = grid_origin
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols

        # Reuse existing constants
        self.main_stat_region = calculate_region_pixels(MAIN_STAT_REGION, RESOLUTION)
        self.sub_stat_region = calculate_region_pixels(SUB_STAT_REGION, RESOLUTION)

        # Ensure output directories exist
        self.image_dir = self._ensure_directory("images")
        self.output_dir = self._ensure_directory("output")

        # Initialize PyDirectInput
        pydirectinput.FAILSAFE = True
        pydirectinput.PAUSE = 0.5

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def get_grid_position(self, row: int, col: int) -> Tuple[int, int]:
        """Calculate the screen coordinates for a given grid position."""
        x = self.grid_origin[0] + (col * self.cell_size[0])
        y = self.grid_origin[1] + (row * self.cell_size[1])
        return (x, y)

    def click_position(self, x: int, y: int) -> None:
        """
        Click at the specified coordinates using PyDirectInput.
        Implements a more reliable clicking mechanism.
        """
        # Move to position first
        pydirectinput.moveTo(x, y)
        time.sleep(0.1)  # Small pause to ensure movement is complete

        # Perform click
        # pydirectinput.click(x, y)
        time.sleep(0.3)  # Wait for click to register and UI to update

    def capture_disk_data(self, disk_index: int) -> Dict:
        """Capture and process data for a single disk position."""
        # Small pause to ensure UI has updated
        time.sleep(0.2)

        # Capture main stat
        main_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_main.png")
        capture_region(main_stat_path, self.main_stat_region)
        main_stat_text = parse_main_stat(main_stat_path)

        # Capture substats
        sub_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_sub.png")
        capture_region(sub_stat_path, self.sub_stat_region)
        sub_stat_text = parse_sub_stats(sub_stat_path)

        # Process the combined text
        combined_text = main_stat_text + "\n" + sub_stat_text
        return beautify_stats(combined_text)

    def scan_all_disks(self) -> None:
        """
        Scan all disk positions in the grid and save the results.
        """
        print("Starting disk scan in 5 seconds...")
        print("Move mouse to upper-left corner to abort.")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        all_disk_data = {}
        disk_index = 0

        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    disk_index += 1
                    print(f"\nProcessing disk {disk_index} at position ({row}, {col})")

                    # Get and click the grid position
                    x, y = self.get_grid_position(row, col)
                    self.click_position(x, y)

                    # Capture and process the disk data
                    disk_data = self.capture_disk_data(disk_index)
                    all_disk_data[f"disk_{disk_index}"] = disk_data

                    # Save incremental results
                    self._save_results(all_disk_data)

        except Exception as e:
            print(f"Error during scanning: {e}")
        finally:
            # Save final results
            self._save_results(all_disk_data)
            print("\nScan complete! Results saved to disk_data.json")

    def _save_results(self, data: Dict) -> None:
        """Save the current results to a JSON file."""
        output_path = os.path.join(self.output_dir, "disk_data.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)


def get_mouse_position():
    """
    Helper function to get current mouse position.
    """
    print("Move your mouse to the desired position.")
    print("You have 5 seconds...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    pos = pydirectinput.position()
    print(f"Position: {pos}")
    return pos
