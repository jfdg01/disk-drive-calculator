import time
from pydoc import resolve

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


def parse_main_stat(image_path):
    """
    Parse the main stat portion using a particular configuration option for tesseract.

    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    # Ensure the images directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)

    # Use Tesseract to extract text using psm 7 (single line of text)
    text = pytesseract.image_to_string(binary, config='--psm 7')

    return text


def parse_sub_stats(image_path):
    """
    Parse a disk image to extract text.

    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    # Ensure the images directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the image

    image = cv2.imread(image_path)
    # Save each image for debugging
    cv2.imwrite(os.path.join(output_dir, 'original.png'), image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(output_dir, 'gray.png'), gray)

    _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    cv2.imwrite(os.path.join(output_dir, 'binary.png'), binary)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(binary, config='--psm 11')

    return text


def main():
    print("Welcome to the Disk CLI!")

    # Output folder for captured images
    output_folder = "captured_images"
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
    print(main_stat_text + "\n" + sub_stat_text)


if __name__ == "__main__":
    main()
