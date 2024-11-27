from source.data_migration import migrate_json_to_db
from source.ocr_data_parser import OCRDataParser
from source.ocr_image_processor import OCRImageProcessor


def main():
    images_path = "../images"
    raw_output_path = "../output/raw_data.json"
    disk_output_path = "../output/disk_data.json"



    image_processor = OCRImageProcessor()
    image_processor.process_images(images_path, raw_output_path)

    OCRDataParser.load_and_parse_ocr_file(raw_output_path, disk_output_path)
    migrate_json_to_db(disk_output_path)


if __name__ == "__main__":
    main()
