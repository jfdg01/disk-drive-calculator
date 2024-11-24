import os
import time
import pyautogui
from constants import ROWS, COLS, RESOLUTION, MAIN_STAT_REGION, FULL_SUB_STAT_REGION, SUB_STAT_REGION_1, \
    SUB_STAT_REGION_2, SUB_STAT_REGION_3, SUB_STAT_REGION_4
from utils import capture_region, get_cell_position, click_position


def _calculate_region_pixels(region_percent, resolution):
    """Calculate pixel values from percentage-based region definition."""
    return {
        "left": int((region_percent["left"] / 100) * resolution[0]),
        "top": int((region_percent["top"] / 100) * resolution[1]),
        "width": int((region_percent["width"] / 100) * resolution[0]),
        "height": int((region_percent["height"] / 100) * resolution[1])
    }


class ScreenScanner:
    def __init__(self):
        """Initialize ScreenScanner with grid parameters."""
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        # Convert regions from percentages to pixels
        self.main_stat_region = _calculate_region_pixels(MAIN_STAT_REGION, RESOLUTION)
        self.full_sub_stat_region = _calculate_region_pixels(FULL_SUB_STAT_REGION, RESOLUTION)
        # create a region for each of the 4 substats
        self.substat_region_1 = _calculate_region_pixels(SUB_STAT_REGION_1, RESOLUTION)
        self.substat_region_2 = _calculate_region_pixels(SUB_STAT_REGION_2, RESOLUTION)
        self.substat_region_3 = _calculate_region_pixels(SUB_STAT_REGION_3, RESOLUTION)
        self.substat_region_4 = _calculate_region_pixels(SUB_STAT_REGION_4, RESOLUTION)

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
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        disk_index = 0

        try:
            for row in range(ROWS):
                for col in range(COLS):
                    disk_index += 1
                    print(f"\nCapturing disk {disk_index} at position ({row}, {col})")

                    # Get and click the grid position
                    x, y = get_cell_position(row, col)
                    click_position(x, y)

                    # Capture screenshots
                    main_stat_path = os.path.join(self.image_dir, f"disk_{disk_index}_main.png")
                    sub_stat_path_1 = os.path.join(self.image_dir, f"disk_{disk_index}_sub_1.png")
                    sub_stat_path_2 = os.path.join(self.image_dir, f"disk_{disk_index}_sub_2.png")
                    sub_stat_path_3 = os.path.join(self.image_dir, f"disk_{disk_index}_sub_3.png")
                    sub_stat_path_4 = os.path.join(self.image_dir, f"disk_{disk_index}_sub_4.png")

                    capture_region(main_stat_path, self.main_stat_region)
                    capture_region(sub_stat_path_1, self.substat_region_1)
                    capture_region(sub_stat_path_2, self.substat_region_2)
                    capture_region(sub_stat_path_3, self.substat_region_3)
                    capture_region(sub_stat_path_4, self.substat_region_4)

        except Exception as e:
            print(f"Error during screen scanning: {e}")
        finally:
            print("\nScreen scanning complete!")


if __name__ == "__main__":
    scanner = ScreenScanner()
    scanner.capture_disk_images()
