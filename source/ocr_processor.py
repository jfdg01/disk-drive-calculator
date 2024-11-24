import json
import os
from typing import Dict
from pytesseract import pytesseract
from utils import parse_main_stat, parse_sub_stats, DiskData, Stat
from constants import TESSERACT_PATH


def parse_disk_text(main_stat_text, sub_stat_text):
    # Check if either of the texts are None and throw an error if so
    if (main_stat_text is None) or (sub_stat_text is None):
        raise ValueError("Both main_stat_text and sub_stat_text must be provided.")

    # Parse the main stat
    main_stat_parts = main_stat_text.strip().split()
    main_stat = {
        "name": main_stat_parts[0],
        "value": main_stat_parts[1]
    }

    # Split the substats into lines and clean them
    sub_stat_lines = [line.strip() for line in sub_stat_text.splitlines() if line.strip()]
    substats = []
    i = 0

    while i < len(sub_stat_lines):
        # Extract name and potential level
        full_name = sub_stat_lines[i]
        i += 1

        level = 0
        if "+" in full_name:
            parts = full_name.split("+")
            name = parts[0].strip()
            level = int(parts[1])
        else:
            name = full_name

        # Extract value
        value = None
        if i < len(sub_stat_lines):
            value_part = sub_stat_lines[i]
            if value_part.endswith("%") or value_part.isdigit():
                value = value_part if value_part.endswith("%") else int(value_part)
                i += 1

        substats.append({
            "name": name,
            "level": level,
            "value": value
        })

    # Assemble the final dictionary
    result = {
        "disk1": {
            "main_stat": main_stat,
            "substats": substats
        }
    }

    return result


class OCRProcessor:
    def __init__(self):
        """Initialize OCRProcessor with paths and configurations."""
        self.image_dir = self._ensure_directory("../images")
        self.output_dir = self._ensure_directory("../output")
        pytesseract.tesseract_cmd = TESSERACT_PATH

    @staticmethod
    def _ensure_directory(dir_name: str) -> str:
        """Create directory if it doesn't exist and return its path."""
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def process_images(self):
        """Process images using OCR and save results to JSON."""
        disk_data = {}

        # Iterate over all main stat images
        for main_stat_file in sorted(os.listdir(self.image_dir)):
            if not main_stat_file.endswith("_main.png"):
                continue

            # Derive the disk index and corresponding sub stat file
            disk_index = main_stat_file.split("_")[1]
            sub_stat_file = f"disk_{disk_index}_sub.png"

            # Parse the images
            main_stat_path = os.path.join(self.image_dir, main_stat_file)
            sub_stat_path = os.path.join(self.image_dir, sub_stat_file)

            print(f"Processing disk {disk_index}...")
            main_stat_text = parse_main_stat(main_stat_path)
            sub_stat_text = parse_sub_stats(sub_stat_path)

            # Parse OCR results into structured data
            disk_data[f"disk_{disk_index}"] = parse_disk_text(main_stat_text, sub_stat_text)

        # Save results to JSON
        self._save_results(disk_data)
        return disk_data

    def _save_results(self, disk_data: Dict[str, Dict], filename: str = "disk_data.json") -> None:
        """
        Save the processed disk data into a JSON file.

        Args:
            disk_data (Dict[str, Dict]): The structured data for the disks.
            filename (str): The name of the JSON file to save. Default is "disk_data.json".
        """
        file_path = os.path.join(self.output_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(disk_data, json_file, indent=4, ensure_ascii=False)
            print(f"Results successfully saved to {file_path}")
        except Exception as e:
            print(f"Failed to save results to JSON: {e}")


if __name__ == "__main__":
    processor = OCRProcessor()
    processor.process_images()
