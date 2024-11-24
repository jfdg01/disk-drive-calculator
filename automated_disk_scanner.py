import os
import json
import time
import pyautogui
import pydirectinput
from typing import Dict, List, Tuple
import mss
import cv2
import numpy as np
import pytesseract
import re
from dataclasses import dataclass, asdict

from constants import *


@dataclass
class Stat:
    type: str
    value: float
    is_percentage: bool


@dataclass
class DiskData:
    main_stat: Stat
    sub_stats: List[Stat]


class AutomatedDiskScanner:
    def __init__(self, start_pos: Tuple[int, int], cell_size: Tuple[int, int],
                 rows: int = 4, cols: int = 8):
        """
        Initialize AutomatedDiskScanner with grid parameters.

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
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        # Resolution and regions (reusing your constants)
        self.resolution = RESOLUTION
        self.main_stat_region = self._calculate_region_pixels(MAIN_STAT_REGION, self.resolution)
        self.sub_stat_region = self._calculate_region_pixels(SUB_STAT_REGION, self.resolution)

        # Create necessary directories
        self.image_dir = self._ensure_directory("images")
        self.output_dir = self._ensure_directory("output")

        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    @staticmethod
    def _calculate_region_pixels(region_percent, resolution):
        """Calculate pixel values from percentage-based region definition."""
        return {
            "left": int((region_percent["left"] / 100) * resolution[0]),
            "top": int((region_percent["top"] / 100) * resolution[1]),
            "width": int((region_percent["width"] / 100) * resolution[0]),
            "height": int((region_percent["height"] / 100) * resolution[1])
        }

    def get_cell_position(self, row: int, col: int) -> Tuple[int, int]:
        """Calculate the screen coordinates for a given grid position."""
        x = self.start_pos[0] + (col * self.cell_size[0])
        y = self.start_pos[1] + (row * self.cell_size[1])
        return (x, y)

    def click_position(self, x: int, y: int, duration: float = 0.2) -> None:
        """Click at the specified coordinates with smooth movement."""
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.3)

    def capture_region(self, output_path: str, region: Dict) -> None:
        """Capture a specific region of the screen."""
        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            cv2.imwrite(output_path, img_bgr)

    def preprocess_image(self, image_path: str):
        """Preprocess the captured image for OCR."""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, GRAY_THRESHOLD, MAX_GRAY_VALUE, cv2.THRESH_BINARY)
        return binary

    def parse_main_stat(self, image_path: str) -> str:
        """Parse main stat from image using OCR."""
        binary = self.preprocess_image(image_path)
        return pytesseract.image_to_string(binary, config=MAIN_STAT_CONFIG)

    def parse_stat_line(self, line: str) -> Stat:
        """Parse a single stat line into structured data."""
        # Remove any unwanted characters and normalize spaces
        line = line.strip().replace('\n', ' ').replace('\r', '')

        # Regular expression patterns
        percentage_pattern = r'([\d.]+)%'
        value_pattern = r'([\d.]+)(?!%)'
        enhancement_pattern = r'\+(\d+)'

        # Initialize variables
        stat_type = line
        value = 0.0
        is_percentage = False
        enhancement_level = 0

        # Extract enhancement level if present
        enhancement_match = re.search(enhancement_pattern, line)
        if enhancement_match:
            enhancement_level = int(enhancement_match.group(1))
            stat_type = re.sub(r'\+\d+', '', stat_type).strip()

        # Check for percentage values
        percentage_match = re.search(percentage_pattern, line)
        if percentage_match:
            value = float(percentage_match.group(1))
            is_percentage = True
        else:
            # Look for regular numeric values
            value_match = re.search(value_pattern, line)
            if value_match:
                value = float(value_match.group(1))

        # Clean up stat type by removing the value and any trailing/leading spaces
        stat_type = re.sub(r'[\d.]+%?', '', stat_type).strip()

        # Add enhancement level back to type if present
        if enhancement_level > 0:
            stat_type = f"{stat_type} +{enhancement_level}"

        return Stat(type=stat_type, value=value, is_percentage=is_percentage)

    def parse_disk_text(self, main_stat_text: str, sub_stat_text: str) -> DiskData:
        """Parse the OCR text into structured disk data."""
        # Parse main stat
        main_stat_lines = [line.strip() for line in main_stat_text.split('\n') if line.strip()]
        main_stat = self.parse_stat_line(main_stat_lines[0] if main_stat_lines else "")

        # Parse sub stats
        sub_stat_lines = [line.strip() for line in sub_stat_text.split('\n') if line.strip()]
        sub_stats = [self.parse_stat_line(line) for line in sub_stat_lines if line]

        return DiskData(main_stat=main_stat, sub_stats=sub_stats)

    def parse_sub_stats(self, image_path: str) -> str:
        """Parse sub stats from image using OCR."""
        binary = self.preprocess_image(image_path)
        return pytesseract.image_to_string(binary, config=SUB_STAT_CONFIG)

    def capture_disk_data(self, disk_index: int) -> Dict:
        """Capture and process data for a single disk position."""
        time.sleep(0.2)  # Wait for UI update

        # Capture main stat
        main_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_main.png")
        self.capture_region(main_stat_path, self.main_stat_region)
        main_stat_text = self.parse_main_stat(main_stat_path)

        # Capture substats
        sub_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_sub.png")
        self.capture_region(sub_stat_path, self.sub_stat_region)
        sub_stat_text = self.parse_sub_stats(sub_stat_path)

        # Parse the text into structured data
        disk_data = self.parse_disk_text(main_stat_text, sub_stat_text)

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
            for row in range(self.rows):
                for col in range(self.cols):
                    disk_index += 1
                    print(f"\nProcessing disk {disk_index} at position ({row}, {col})")

                    # Get and click the grid position
                    x, y = self.get_cell_position(row, col)
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
            return all_disk_data

    def _save_results(self, data: Dict) -> None:
        """Save the results to a JSON file."""
        output_path = os.path.join(self.output_dir, "disk_data.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    # Create and run the automated scanner
    scanner = AutomatedDiskScanner(
        start_pos=START_POS,
        cell_size=CELL_SIZE,
        rows=ROWS,
        cols=COLS
    )

    print(f"Scanner Parameters:")
    print(f"Starting Position: {START_POS}")
    print(f"Cell Size: {CELL_SIZE}")
    print(f"Grid: {scanner.rows}x{scanner.cols}")

    # Start scanning sequence
    disk_data = scanner.scan_all_disks()

    print("\nScanning sequence complete!")
    print(f"Total disks scanned: {len(disk_data)}")


if __name__ == "__main__":
    main()
