import os
import json
import time
from typing import Dict

import pyautogui
from dataclasses import asdict

from constants import _calculate_region_pixels, MAIN_STAT_REGION, SUB_STAT_REGION, RESOLUTION, ROWS, COLS
from utils import capture_region, parse_main_stat, parse_sub_stats, parse_disk_text, get_cell_position, click_position


class AutomatedDiskScanner:
    def __init__(self):
        """
        Initialize AutomatedDiskScanner with grid parameters
        """

        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        self.main_stat_region = _calculate_region_pixels(MAIN_STAT_REGION, RESOLUTION)
        self.sub_stat_region = _calculate_region_pixels(SUB_STAT_REGION, RESOLUTION)

        # Create necessary directories
        self.image_dir = self._ensure_directory("images")
        self.output_dir = self._ensure_directory("output")

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def capture_disk_data(self, disk_index: int) -> Dict:
        """Capture and process data for a single disk position."""
        time.sleep(0.2)  # Wait for UI update

        # Capture main stat
        main_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_main.png")
        capture_region(main_stat_path, self.main_stat_region)
        main_stat_text = parse_main_stat(main_stat_path)

        # Capture substats
        sub_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_sub.png")
        capture_region(sub_stat_path, self.sub_stat_region)
        sub_stat_text = parse_sub_stats(sub_stat_path)

        # Parse the text into structured data
        disk_data = parse_disk_text(main_stat_text, sub_stat_text)

        # Convert to dictionary format
        return asdict(disk_data)

    def scan_all_disks(self) -> Dict:
        """
        Scan all disk positions in the grid and save the results.
        Returns the complete dataset of all scanned disks.
        """
        print("Starting automated disk scan in 5 seconds...")
        print("Move mouse to upper-left corner to abort.")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        all_disk_data = {}
        disk_index = 0

        try:
            for row in range(ROWS):
                for col in range(COLS):
                    disk_index += 1
                    print(f"\nProcessing disk {disk_index} at position ({row}, {col})")

                    # Get and click the grid position
                    x, y = get_cell_position(row, col)
                    click_position(x, y)

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
            return all_disk_data

    def _save_results(self, data: Dict) -> None:
        """Save the results to a JSON file."""
        output_path = os.path.join(self.output_dir, "disk_data.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
