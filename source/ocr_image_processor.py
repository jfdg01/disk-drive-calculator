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
        """Initialize OCRImageProcessor with paths and configurations."""
        self.image_dir = self._ensure_directory("../images_6")
        self.output_dir = self._ensure_directory("../output")
        pytesseract.tesseract_cmd = TESSERACT_PATH

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def process_images(self):
        """Process images using OCR and save raw results to a JSON file."""
        ocr_data = {}

        pictures = os.listdir(self.image_dir)

        for stat_picture in pictures:

            if stat_picture.endswith("png"):
                image_extension = "png"
            else:
                image_extension = "jpg"

            if not stat_picture.endswith("_main." + image_extension):
                continue

            # Derive the disk index and corresponding sub stat file
            disk_index = stat_picture.split("_")[1]
            sub_stat_files = [
                f"disk_{disk_index}_sub_{i}." + image_extension
                for i in range(1, 5)
            ]

            # Parse the images
            main_stat_path = os.path.join(self.image_dir, stat_picture)
            sub_stat_paths = [
                os.path.join(self.image_dir, sub_stat_file)
                for sub_stat_file in sub_stat_files
            ]

            print(f"Processing disk {disk_index}...")
            ocr_data[f"disk_{disk_index}"] = {
                "main_stat": parse_main_stat(main_stat_path),
                "sub_stats": [parse_main_stat(path) for path in sub_stat_paths]
            }

        # Save raw OCR results
        self._save_results(ocr_data, "../output/raw_data.json")
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
    processor = OCRImageProcessor()
    processor.process_images()
