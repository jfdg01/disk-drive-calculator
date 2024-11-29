import json
import os

from source.constants import SUBSTATS, MAIN_STAT_LEVELS


class OCRDataParser:
    @staticmethod
    def parse_disk_text(main_stat_text, sub_stat_texts):
        """Parse main and sub stats from raw OCR text into structured data."""

        def parse_main_stat_text(stat_text):
            if not stat_text:
                return None

            parts = stat_text.strip().split()
            stat_name = " ".join(parts[:-1]) if len(parts) > 2 else parts[0]
            stat_value = float(parts[-1].replace("%", "").replace("a", "4"))

            percentage = False
            if "%" in parts[-1]:
                percentage = True

            if not percentage:
                if stat_name == "ATK":
                    stat_name = "Flat ATK"
                elif stat_name == "HP":
                    stat_name = "Flat HP"
                elif stat_name == "DEF":
                    stat_name = "Flat DEF"
            else:
                if stat_name == "ATK":
                    stat_name = "ATK%"
                elif stat_name == "HP":
                    stat_name = "HP%"
                elif stat_name == "DEF":
                    stat_name = "DEF%"

            level = infer_main_stat_level(stat_name, stat_value)

            return {
                "name": stat_name,
                "value": stat_value,
                "level": level
            }

        def infer_main_stat_level(stat_name, stat_value):
            if stat_name not in MAIN_STAT_LEVELS:
                if stat_name.endswith("Bonus"):
                    stat_name = "Element DMG Bonus"
                else:
                    return None
            levels = MAIN_STAT_LEVELS[stat_name]
            for level, value in enumerate(levels):
                if stat_value <= value:
                    return level - 1 if level > 0 else 0
            return len(levels) - 1

        def parse_sub_stat_text(stat_text):
            if not stat_text:
                return None
            if "Set Effect" in stat_text:
                return None

            parts = stat_text.strip().split()
            stat_data = {"name": None, "level": 0, "value": None}

            if parts[0] == "CRIT" or parts[0] == "Anomaly":
                stat_data["name"] = f"{parts[0]} {parts[1]}"
                level_and_value_parts = parts[2:]
            else:
                stat_data["name"] = parts[0]
                level_and_value_parts = parts[1:]

            percentage, value_part = False, None
            for part in level_and_value_parts:
                if part.startswith("+"):
                    stat_data["level"] = int(part.replace("+", ""))
                else:
                    value_part = part

            if value_part.endswith("%"):
                percentage = True

            if stat_data["name"] == "Anomaly Proficlency":
                stat_data["name"] = "Anomaly Proficiency"

            if stat_data["name"] == "MP" or stat_data["name"] == "AP" or stat_data["name"] == "Ld" or stat_data[
                "name"] == "uP" or stat_data["name"] == "hd":
                stat_data["name"] = "HP"

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

            if stat_data["name"] in SUBSTATS and stat_data["level"] > 0:
                stat_data["value"] = round(SUBSTATS[stat_data["name"]] * (stat_data["level"] + 1), 2)
            elif stat_data["name"] in SUBSTATS:
                stat_data["value"] = SUBSTATS[stat_data["name"]]
            else:
                stat_data["value"] = 0

            return stat_data

        main_stat = parse_main_stat_text(main_stat_text)
        sub_stats = [result for sub_text in sub_stat_texts if
                     sub_text and (result := parse_sub_stat_text(sub_text)) is not None]

        return {"main_stat": main_stat, "sub_stats": sub_stats}

    @staticmethod
    def parse_ocr_data(ocr_data):
        """Parse the entire OCR data structure."""
        parsed_data = {}
        for disk, stats in ocr_data.items():
            parsed_data[disk] = OCRDataParser.parse_disk_text(stats["main_stat"], stats["sub_stats"])
        return parsed_data

    @staticmethod
    def load_and_parse_ocr_file(input_file, output_file):
        """Load OCR data, parse it, and save it as JSON."""

        # Check for the existence of the input file
        if not os.path.exists(input_file):
            print(f"File {input_file} does not exist.")
            return

        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                ocr_data = json.load(file)

            parsed_data = OCRDataParser.parse_ocr_data(ocr_data)

            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(parsed_data, file, indent=4, ensure_ascii=False)

            print(f"Parsed data saved to {output_file}.")
        except Exception as e:
            print(f"Error processing OCR data: {e}")


if __name__ == "__main__":
    OCRDataParser.load_and_parse_ocr_file("../output/raw_data.json", "../output/disk_data.json")
