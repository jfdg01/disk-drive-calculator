from source.json_to_db_data_converter import convert_json_to_db
from source.ocr_data_parser import OCRDataParser
from source.ocr_image_processor import OCRImageProcessor
from source.screen_scanner import ScreenScanner


def main():
    suffix = "" # "_test"

    images_path = "../images"
    raw_json_path = "../output/raw_data" + suffix + ".json"
    disk_json_path = "../output/disk_data" + suffix + ".json"
    database_path = "../db/disk_database" + suffix + ".db"

    # Screenshot and save all the images on the game screen
    # screen_scanner = ScreenScanner(images_path)
    # screen_scanner.capture_and_save_disk_images()

    # Process all images with OCR and dump the raw data into a JSON file
    image_processor = OCRImageProcessor()
    image_processor.process_images(images_path, raw_json_path)

    # Load the raw data from the JSON file and beautify it
    OCRDataParser.load_and_parse_ocr_file(raw_json_path, disk_json_path)

    # Convert the JSON data to the database
    convert_json_to_db(disk_json_path, database_path)


if __name__ == "__main__":
    main()
