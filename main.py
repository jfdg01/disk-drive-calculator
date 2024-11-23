import time
import cv2
import pytesseract
import os
import mss
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

RESOLUTION = (1920, 1080)

MAIN_STAT_REGION = {
    "left": 74.0,
    "top": 38.89,
    "width": 20.83,
    "height": 4.63
}

SUB_STAT_REGION = {
    "left": 74.0,
    "top": 46.3,
    "width": 20.83,
    "height": 18.52
}


def calculate_region_pixels(region_percent, resolution):
    left = int((region_percent["left"] / 100) * resolution[0])
    top = int((region_percent["top"] / 100) * resolution[1])
    width = int((region_percent["width"] / 100) * resolution[0])
    height = int((region_percent["height"] / 100) * resolution[1])
    return {"left": left, "top": top, "width": width, "height": height}


def capture_region(output_path, region):
    """
    Capture a fixed region of the screen.

    :param output_path: Path to save the captured image.
    :param region: A dictionary with the region to capture (x, y, width, height).
    """
    with mss.mss() as sct:
        # Capture the specified region
        screenshot = sct.grab(region)
        # Convert to a numpy array and save as an image
        img = np.array(screenshot)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR
        cv2.imwrite(output_path, img_bgr)
        print(f"Captured image saved to {output_path}")


def ensure_images_directory_exists():
    output_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    return binary


def parse_main_stat(image_path):
    ensure_images_directory_exists()
    binary = preprocess_image(image_path)
    text = pytesseract.image_to_string(binary, config='--psm 7')
    return text


def parse_sub_stats(image_path):
    ensure_images_directory_exists()
    binary = preprocess_image(image_path)
    text = pytesseract.image_to_string(binary, config='--psm 11')
    return text


def parse_stat_value(stat_text):
    """
    Parse a stat value, handling both percentage and flat values.
    Returns a tuple of (value, is_percentage)
    """
    stat_text = stat_text.strip()
    if '%' in stat_text:
        try:
            return float(stat_text.replace('%', '')), True
        except ValueError:
            return 0, False
    try:
        return float(stat_text), False
    except ValueError:
        return 0, False


def format_stat_value(value, is_percentage):
    """
    Format a stat value for display
    """
    if is_percentage:
        return f"{value}%"
    return str(value)


def process_stat_line(line):
    """
    Process a single stat line, separating the stat type and value.
    Returns a tuple of (stat_type, value, is_percentage)
    """
    line = line.strip()
    if not line:
        return None, 0, False

    # Handle cases where the value might be on a separate line
    if line.endswith('%'):
        try:
            value = float(line.replace('%', ''))
            return None, value, True
        except ValueError:
            pass
    elif line.replace('.', '').isdigit():
        try:
            value = float(line)
            return None, value, False
        except ValueError:
            pass

    # Handle "+N" suffix
    parts = line.split()
    if len(parts) >= 2 and parts[-1].startswith('+') and parts[-1][1:].isdigit():
        parts = parts[:-1]  # Remove the "+N" part
        line = ' '.join(parts)

    # Check if the line ends with a number or percentage
    if '%' in line:
        try:
            value_start = line.rindex(' ')
            value_text = line[value_start:].strip()
            stat_type = line[:value_start].strip()
            value = float(value_text.replace('%', ''))
            return stat_type, value, True
        except (ValueError, IndexError):
            return line, 0, False
    else:
        try:
            # Find the last space in the line
            value_start = line.rindex(' ')
            value_text = line[value_start:].strip()
            stat_type = line[:value_start].strip()
            value = float(value_text)
            return stat_type, value, False
        except (ValueError, IndexError):
            return line, 0, False


def beautify_stats(text):
    """
    Process the OCR extracted text and return a structured dictionary of stats.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    stats = {
        'main_stat': None,
        'sub_stats': []
    }

    # Process the first line as main stat
    if lines:
        stat_type, value, is_percentage = process_stat_line(lines[0])
        if stat_type and value:
            stats['main_stat'] = {
                'type': stat_type,
                'value': value,
                'is_percentage': is_percentage
            }

    # Process remaining lines as sub stats
    current_stat = None
    for line in lines[1:]:
        stat_type, value, is_percentage = process_stat_line(line)

        # If we got a stat type without value
        if stat_type and value == 0:
            current_stat = stat_type
            continue

        # If we got a value without type, and we have a current_stat
        if not stat_type and value != 0 and current_stat:
            stats['sub_stats'].append({
                'type': current_stat,
                'value': value,
                'is_percentage': is_percentage
            })
            current_stat = None
            continue

        # If we got both type and value
        if stat_type and value != 0:
            stats['sub_stats'].append({
                'type': stat_type,
                'value': value,
                'is_percentage': is_percentage
            })
            current_stat = None

    return stats


def display_beautified_stats(stats):
    """
    Display the beautified stats in a clean format
    """
    if stats['main_stat']:
        print(f"Main Stat: {stats['main_stat']['type']} - "
              f"{format_stat_value(stats['main_stat']['value'], stats['main_stat']['is_percentage'])}")

    if stats['sub_stats']:
        print("\nSub Stats:")
        for stat in stats['sub_stats']:
            print(f"  {stat['type']}: "
                  f"{format_stat_value(stat['value'], stat['is_percentage'])}")
    print()


def process_ocr_output(text):
    """
    Process OCR output and display beautified stats
    """
    stats = beautify_stats(text)
    display_beautified_stats(stats)
    return stats


def main():
    print("Welcome to the Disk CLI!")

    # Output folder for captured images
    output_folder = "temp"
    os.makedirs(output_folder, exist_ok=True)

    # Give time to change screens
    print("Waiting 2 seconds...")
    time.sleep(2)

    # Capture main stat region and parse a screenshot
    mainstat_name = "mainstat-screenshot.png"
    main_stat_region = calculate_region_pixels(MAIN_STAT_REGION, RESOLUTION)

    # Capture sub stat region and parse a screenshot
    image_name = "substat-screenshot.png"
    sub_stat_region = calculate_region_pixels(SUB_STAT_REGION, RESOLUTION)

    output_path = os.path.join(output_folder, mainstat_name)
    capture_region(output_path, main_stat_region)
    main_stat_text = parse_main_stat(output_path)

    output_path = os.path.join(output_folder, image_name)
    capture_region(output_path, sub_stat_region)
    sub_stat_text = parse_sub_stats(output_path)

    print("\nExtracted Text:")
    combined_text = main_stat_text + "\n" + sub_stat_text
    print(combined_text)
    print("\nProcessed Text:")
    process_ocr_output(combined_text)


if __name__ == "__main__":
    main()
