import os
import json
import cv2
from pytesseract import pytesseract

from source.constants import TESSERACT_PATH, GRAY_THRESHOLD, MAX_GRAY_VALUE, MAIN_STAT_CONFIG


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
    return result.strip()  # Strip any trailing spaces or newlines


class OCRImageProcessor:
    def __init__(self):
        """Initialize OCRImageProcessor with Tesseract path configuration."""
        pytesseract.tesseract_cmd = TESSERACT_PATH

    @staticmethod
    def _get_image_subdirectories(base_dir: str) -> list:
        """Retrieve all subdirectories in the base directory."""
        base_dir = os.path.abspath(base_dir)
        if not os.path.exists(base_dir):
            print(f"Base directory {base_dir} does not exist.")
            return []

        subdirectories = [
            os.path.join(base_dir, sub_dir)
            for sub_dir in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, sub_dir))
        ]
        return sorted(subdirectories)

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.abspath(dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def process_images(self, base_dir: str, output_file: str):
        """Process images from subdirectories in the base directory and save results.

        Args:
            base_dir (str): Parent directory containing subdirectories with images.
            output_file (str): Path to the output JSON file for saving results.
        """
        image_dirs = self._get_image_subdirectories(base_dir)

        if not image_dirs:
            print(f"No subdirectories found in base directory: {base_dir}")
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
    base_dir = "../../images"  # Parent directory containing subdirectories like "images_1", "images_2", etc.
    output_file_path = "../../output/raw_data.json"  # Provide the output file path

    processor = OCRImageProcessor()
    processor.process_images(base_dir, output_file_path)