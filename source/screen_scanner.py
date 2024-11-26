import os
import cv2
import numpy as np
import mss
import pydirectinput
import time
from typing import Dict, Tuple

from constants import ROWS, COLS, RESOLUTION, MAIN_STAT_REGION, SUB_STAT_REGION_1, \
    SUB_STAT_REGION_2, SUB_STAT_REGION_3, SUB_STAT_REGION_4, START_POS, CELL_SIZE, IMAGE_EXTENSION


def _calculate_region_pixels(region_percent):
    """Calculate pixel values from percentage-based region definition."""
    resolution = RESOLUTION
    region = {
        "left": int((region_percent["left"] / 100) * resolution[0]),
        "top": int((region_percent["top"] / 100) * resolution[1]),
        "width": int((region_percent["width"] / 100) * resolution[0]),
        "height": int((region_percent["height"] / 100) * resolution[1])
    }
    return region


class ScreenScanner:
    def __init__(self):
        """Initialize ScreenScanner with grid parameters."""
        # Safety settings
        pydirectinput.FAILSAFE = True
        pydirectinput.PAUSE = 0.1

        # Convert regions from percentages to pixels
        self.main_stat_region = _calculate_region_pixels(MAIN_STAT_REGION)
        # self.full_sub_stat_region = _calculate_region_pixels(FULL_SUB_STAT_REGION)
        # create a region for each of the 4 substats
        self.substat_region_1 = _calculate_region_pixels(SUB_STAT_REGION_1)
        self.substat_region_2 = _calculate_region_pixels(SUB_STAT_REGION_2)
        self.substat_region_3 = _calculate_region_pixels(SUB_STAT_REGION_3)
        self.substat_region_4 = _calculate_region_pixels(SUB_STAT_REGION_4)

        # Directories for screenshots
        self.image_dir = self._ensure_directory("../images")

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def capture_disk_images(self) -> None:
        """Capture screenshots for all disk positions in the grid."""
        print("Starting screen scanning in 5 seconds...")
        print("Move mouse to upper-left corner to abort.")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        disk_index = 0

        try:
            for row in range(ROWS):
                for col in range(COLS):
                    disk_index += 1
                    disk_index_str = f"{disk_index:03}"  # Format as three digits

                    print(f"\nCapturing disk {disk_index_str} at position ({row}, {col})")

                    # Get and click the grid position
                    x, y = get_cell_position(row, col)
                    click_position(x, y)
                    # Wait for the screen to update
                    time.sleep(0.2)

                    # Capture screenshots
                    main_stat_path = os.path.join(self.image_dir, f"disk_{disk_index_str}_main." + IMAGE_EXTENSION)
                    sub_stat_path_1 = os.path.join(self.image_dir, f"disk_{disk_index_str}_sub_1." + IMAGE_EXTENSION)
                    sub_stat_path_2 = os.path.join(self.image_dir, f"disk_{disk_index_str}_sub_2." + IMAGE_EXTENSION)
                    sub_stat_path_3 = os.path.join(self.image_dir, f"disk_{disk_index_str}_sub_3." + IMAGE_EXTENSION)
                    sub_stat_path_4 = os.path.join(self.image_dir, f"disk_{disk_index_str}_sub_4." + IMAGE_EXTENSION)

                    capture_region(main_stat_path, self.main_stat_region)
                    capture_region(sub_stat_path_1, self.substat_region_1)
                    capture_region(sub_stat_path_2, self.substat_region_2)
                    capture_region(sub_stat_path_3, self.substat_region_3)
                    capture_region(sub_stat_path_4, self.substat_region_4)

        except Exception as e:
            print(f"Error during screen scanning: {e}")
        finally:
            print("\nScreen scanning complete!")


def get_cell_position(row: int, col: int) -> Tuple[int, int]:
    """Calculate the screen coordinates for a given grid position."""
    x = START_POS[0] + (col * CELL_SIZE[0])
    y = START_POS[1] + (row * CELL_SIZE[1])
    return x, y


def click_position(x: int, y: int) -> None:
    """Click at the specified coordinates with smooth movement."""
    pydirectinput.moveTo(x, y, 0.1)
    time.sleep(0.05)
    pydirectinput.click()
    time.sleep(0.05)


def capture_region(output_path: str, region: Dict) -> None:
    """Capture a specific region of the screen."""
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(output_path, img_bgr)


if __name__ == "__main__":
    scanner = ScreenScanner()
    scanner.capture_disk_images()
