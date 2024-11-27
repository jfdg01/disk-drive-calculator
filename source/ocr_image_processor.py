import os
import json
import cv2
from pytesseract import pytesseract

from constants import TESSERACT_PATH, GRAY_THRESHOLD, MAX_GRAY_VALUE, MAIN_STAT_CONFIG


def preprocess_image(image_path: str):
    """Preprocess the captured image for OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, GRAY_THRESHOLD, MAX_GRAY_VALUE, cv2.THRESH_BINARY)
    return binary


def parse_main_stat(image_path: str) -> str:
    """Parse main stat from image using OCR."""
    binary = preprocess_image(image_path)
    result = pytesseract.image_to_string(binary, config=MAIN_STAT_CONFIG)
    return result


class OCRImageProcessor:
    def __init__(self):
        """Initialize OCRImageProcessor with Tesseract path configuration."""
        pytesseract.tesseract_cmd = TESSERACT_PATH

    @staticmethod
    def _get_matching_image_dirs(base_pattern: str) -> list:
        """Retrieve all directories matching the given pattern."""
        base_dir = os.path.dirname(base_pattern)
        prefix = os.path.basename(base_pattern)
        matching_dirs = [
            os.path.join(base_dir, d)
            for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d)) and d.startswith(prefix)
        ]
        return matching_dirs

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.abspath(dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def process_images(self, base_pattern: str, output_file: str):
        """Process images from directories matching the pattern and save results.

        Args:
            base_pattern (str): Base directory pattern to search for image folders.
                                Example: "../images" will match "../images*", "../images_1", etc.
            output_file (str): Path to the output JSON file for saving results.
        """
        image_dirs = self._get_matching_image_dirs(base_pattern)

        if not image_dirs:
            print(f"No directories found matching pattern: {base_pattern}")
            return {}

        ocr_data = {}

        for image_dir in image_dirs:
            folder_name = os.path.basename(image_dir)
            print(f"Processing folder: {folder_name}")

            pictures = os.listdir(image_dir)

            for stat_picture in pictures:
                if stat_picture.endswith("png"):
                    image_extension = "png"
                else:
                    image_extension = "jpg"

                if not stat_picture.endswith("_main." + image_extension):
                    continue

                # Derive the disk index and corresponding sub stat files
                disk_index = stat_picture.split("_")[1]
                sub_stat_files = [
                    f"disk_{disk_index}_sub_{i}." + image_extension
                    for i in range(1, 5)
                ]

                # Parse the images
                main_stat_path = os.path.join(image_dir, stat_picture)
                sub_stat_paths = [
                    os.path.join(image_dir, sub_stat_file)
                    for sub_stat_file in sub_stat_files
                ]

                print(f"  Processing disk {disk_index}...")
                ocr_data[f"{folder_name}_disk_{disk_index}"] = {
                    "main_stat": parse_main_stat(main_stat_path),
                    "sub_stats": [parse_main_stat(path) for path in sub_stat_paths if os.path.exists(path)]
                }

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        self._ensure_directory(output_dir)

        # Save raw OCR results
        self._save_results(ocr_data, output_file)
        return ocr_data

    @staticmethod
    def _save_results(data, filename):
        """Save OCR data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"OCR data successfully saved to {filename}.")
        except Exception as e:
            print(f"Error saving OCR data: {e}")


if __name__ == "__main__":
    # Example usage
    base_pattern = "../images"  # Base directory to match patterns like "../images*", "../images_1", etc.
    output_file_path = "../output/raw_data.json"  # Provide the output file path

    processor = OCRImageProcessor()
    processor.process_images(base_pattern, output_file_path)