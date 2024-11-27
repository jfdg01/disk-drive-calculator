import os
import json
import cv2
from pytesseract import pytesseract

from constants import TESSERACT_PATH, GRAY_THRESHOLD, MAX_GRAY_VALUE, MAIN_STAT_CONFIG
from source.disk import Stat, Disk
from source.disk_database import DiskDatabase
from source.disk_manager import DiskManager


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
    def __init__(self, base_dir="../"):
        """Initialize OCRImageProcessor with paths and configurations."""
        self.base_dir = base_dir
        self.image_dirs = self._get_image_dirs()
        self.output_dir = self._ensure_directory(os.path.join(base_dir, "output"))
        pytesseract.tesseract_cmd = TESSERACT_PATH

    def _get_image_dirs(self):
        """Retrieve all directories matching the 'images*' pattern."""
        dirs = [
            os.path.join(self.base_dir, d)
            for d in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, d)) and d.startswith("images")
        ]
        return dirs

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.abspath(dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def process_images(self):
        """Process images using OCR and save raw results to a JSON file."""
        ocr_data = {}

        for image_dir in self.image_dirs:
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

        # Save raw OCR results
        self._save_results(ocr_data, os.path.join(self.output_dir, "raw_data.json"))
        return ocr_data

    def migrate_json_to_db(self):

        json_file = "../output/disk_data.json"
        database = DiskDatabase()

        """Migrate data from JSON to SQLite database."""
        if not os.path.exists(json_file):
            print(f"File {json_file} does not exist.")
            return

        with open(json_file, "r") as file:
            raw_disks = json.load(file)

        disk_manager = DiskManager(database)
        for disk_id, disk_data in raw_disks.items():
            main_stat_data = disk_data.get("main_stat")
            if not main_stat_data:
                print(f"Disk {disk_id} is missing 'main_stat' data. Using default value.")
                main_stat = Stat(
                    name="HP",
                    value=550.0,
                    level=1
                )
            else:
                main_stat = Stat(
                    name=main_stat_data["name"],
                    value=main_stat_data["value"],
                    level=main_stat_data["level"]
                )

            try:
                sub_stats = [Stat(**sub_stat) for sub_stat in disk_data.get("sub_stats", [])]
                disk = Disk(id=disk_id, main_stat=main_stat, sub_stats=sub_stats)

                # check if the disk is already in the database
                if disk_manager.disk_exists(disk):
                    print(f"Disk {disk_id} already exists in the database. Skipping this entry.")
                    continue

                # print(f"Adding disk {disk_id} to the database...")
                disk_manager.add_disk(disk)
            except KeyError as e:
                print(f"Missing key {e} in 'main_stat' or 'sub_stats' for disk {disk_id}. Skipping this entry.")

        database.close()
        print("Migration complete!")

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
    processor.migrate_json_to_db()
