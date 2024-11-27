from source.disk_database import DiskDatabase
from source.disk_manager import DiskManager
from source.json_to_db_data_converter import convert_json_to_db
from source.ocr_data_parser import OCRDataParser
from source.ocr_image_processor import OCRImageProcessor
from source.screen_scanner import ScreenScanner

suffix = ""  # "_test"

images_path = "../images" + suffix
raw_json_path = "../output/raw_data" + suffix + ".json"
disk_json_path = "../output/disk_data" + suffix + ".json"
database_path = "../db/disk_database" + suffix + ".db"


def main():
    # Screenshot and save all the images on the game screen
    # while True:
    #     screen_scanner = ScreenScanner(images_path)
    #     screen_scanner.capture_and_save_disk_images()
    #     # Ask the user if they want to continue
    #     user_input = input("Do you want to scan again? (yes/no) (y/n): ").strip().lower()
    #     if user_input != 'yes' or user_input != 'y' or user_input != 'n' or user_input != 'no':
    #         print("Invalid input. Please enter 'yes' or 'no'.")
    #     if user_input == 'no' or user_input == 'n':
    #         break

    # Process all images with OCR and dump the raw data into a JSON file
    image_processor = OCRImageProcessor()
    image_processor.process_images(images_path, raw_json_path)

    # Load the raw data from the JSON file and beautify it
    OCRDataParser.load_and_parse_ocr_file(raw_json_path, disk_json_path)

    # Convert the JSON data to the database
    convert_json_to_db(disk_json_path, database_path)

    # Evaluate the disks in the database
    evaluate_disks(database_path)


def evaluate_disks(db_path):
    # Initialize DiskDatabase (assumes implementation exists)
    db = DiskDatabase(db_path)
    disk_manager = DiskManager(db)

    # Example: Add, rank, and display disks
    ranked_disks = disk_manager.rank_disks()
    disk_manager.display_ranking(ranked_disks)


def do():
    OCRDataParser.load_and_parse_ocr_file(raw_json_path, disk_json_path)
    convert_json_to_db(disk_json_path, database_path)
    evaluate_disks(database_path)

if __name__ == "__main__":
    do()
