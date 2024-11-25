import json
import os
from typing import Dict
from pytesseract import pytesseract
from utils import parse_main_stat
from constants import TESSERACT_PATH, SUBSTATS, IMAGE_EXTENSION


def parse_disk_text(main_stat_text, sub_stat_texts):
    # DEF +1 9.6%
    # HP 212
    # CRIT Rate 2.4%
    # CRIT DMG +3 21.3%

    def parse_main_stat_text(stat_text):
        if not stat_text:
            return None

        parts = stat_text.strip().split()
        # Extracts the last part of the text, removes any '%' character, and converts it to a float
        stat_data = {"name": None, "value": parts[-1].replace("%", "")}
        # Hack to handle the "2a" value
        if stat_data["value"] == "2a":
            stat_data["value"] = "24"

        # If the name is more than one word, join them
        if len(parts) > 2:
            stat_data["name"] = " ".join(parts[:-1])
        else:
            stat_data["name"] = parts[0]

        return stat_data

    def parse_sub_stat_text(stat_text):
        if not stat_text:
            return None

        parts = stat_text.strip().split()
        stat_data = {
            "name": None,
            "level": 0,
            "value": None
        }

        # Handle special stat names (CRIT Rate, CRIT DMG, Anomaly Proficiency)
        if parts[0] == "CRIT" or parts[0] == "Anomaly":
            stat_data["name"] = f"{parts[0]} {parts[1]}"
            level_and_value_parts = parts[2:]
        else:
            stat_data["name"] = parts[0]
            level_and_value_parts = parts[1:]

        percentage, value_part = False, None
        # Process remaining parts for level and value
        for part in level_and_value_parts:
            # if has level
            if part.startswith("+"):
                # Extract level number
                stat_data["level"] = int(part.replace("+", ""))
            else:
                value_part = part

        # Calculate the value based on the stat name
        if value_part.endswith("%"):
            percentage = True

        # Normalize the stat name
        if not percentage:
            if stat_data["name"] == "ATK":
                stat_data["name"] = "Flat ATK"
            elif stat_data["name"] == "HP":
                stat_data["name"] = "Flat HP"
            elif stat_data["name"] == "DEF":
                stat_data["name"] = "Flat DEF"
        else:
            if stat_data["name"] == "ATK":
                stat_data["name"] = "ATK%"
            elif stat_data["name"] == "HP":
                stat_data["name"] = "HP%"
            elif stat_data["name"] == "DEF":
                stat_data["name"] = "DEF%"

        # Calculate the value based on the stat name and the level using the map
        if stat_data["name"] in SUBSTATS and stat_data["level"] > 0:
            stat_data["value"] = SUBSTATS[stat_data["name"]] * (stat_data["level"] + 1)
        elif stat_data["name"] in SUBSTATS:
            stat_data["value"] = SUBSTATS[stat_data["name"]]
        else:
            stat_data["value"] = 0

        return stat_data

    # Parse main stat
    main_stat = parse_main_stat_text(main_stat_text)

    # Parse substats
    sub_stats = []
    for sub_stat_text in sub_stat_texts:
        if sub_stat_text:
            sub_stats.append(parse_sub_stat_text(sub_stat_text))

    # Assemble the final dictionary
    result = {
        "main_stat": main_stat,
        "sub_stats": sub_stats
    }

    return result


class OCRProcessor:
    def __init__(self):
        """Initialize OCRProcessor with paths and configurations."""
        # self.image_dir = self._ensure_directory("../images")
        self.image_dir = self._ensure_directory("../test/problematic_images")
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
        pictures = os.listdir(self.image_dir)

        centinela = 0
        for stat_picture in pictures:
            if not stat_picture.endswith("_main." + IMAGE_EXTENSION):
                continue
            if centinela == 24:
                print("This")
            centinela += 1
            # Derive the disk index and corresponding sub stat file
            disk_index = stat_picture.split("_")[1]
            sub_stat_file_1 = f"disk_{disk_index}_sub_1." + IMAGE_EXTENSION
            sub_stat_file_2 = f"disk_{disk_index}_sub_2." + IMAGE_EXTENSION
            sub_stat_file_3 = f"disk_{disk_index}_sub_3." + IMAGE_EXTENSION
            sub_stat_file_4 = f"disk_{disk_index}_sub_4." + IMAGE_EXTENSION

            # Parse the images
            main_stat_path = os.path.join(self.image_dir, stat_picture)
            sub_stat_path_1 = os.path.join(self.image_dir, sub_stat_file_1)
            sub_stat_path_2 = os.path.join(self.image_dir, sub_stat_file_2)
            sub_stat_path_3 = os.path.join(self.image_dir, sub_stat_file_3)
            sub_stat_path_4 = os.path.join(self.image_dir, sub_stat_file_4)

            print(f"Processing disk {disk_index}...")
            main_stat_text = parse_main_stat(main_stat_path)
            sub_stat_text_1 = parse_main_stat(sub_stat_path_1)
            sub_stat_text_2 = parse_main_stat(sub_stat_path_2)
            sub_stat_text_3 = parse_main_stat(sub_stat_path_3)
            sub_stat_text_4 = parse_main_stat(sub_stat_path_4)

            # Parse OCR results into structured data
            sub_stat_texts = [sub_stat_text_1, sub_stat_text_2, sub_stat_text_3, sub_stat_text_4]
            disk_data[f"disk_{disk_index}"] = parse_disk_text(main_stat_text, sub_stat_texts)

        # Save results to JSON
        print("disk_data", disk_data)
        self._save_results(disk_data)
        return disk_data

    def _save_results(self, disk_data: Dict[str, Dict], filename: str = "../output/disk_data.json") -> None:
        """
        Save the processed disk data into a JSON file.

        Args:
            disk_data (Dict[str, Dict]): The structured data for the disks.
            filename (str): The name of the JSON file to save. Default is "disk_data.json".
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(disk_data, file, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {filename}.")
        except Exception as e:
            print(f"An error occurred while saving data to {filename}: {e}")


if __name__ == "__main__":
    processor = OCRProcessor()
    processor.process_images()
