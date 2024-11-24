import json
from dataclasses import dataclass

import cv2
import numpy as np
import mss
import pyautogui
import time
import re
from typing import Dict, List, Tuple

from pytesseract import pytesseract

from constants import START_POS, CELL_SIZE, GRAY_THRESHOLD, MAX_GRAY_VALUE, MAIN_STAT_CONFIG, SUB_STAT_CONFIG


@dataclass
class Stat:
    type: str
    value: float
    is_percentage: bool


@dataclass
class DiskData:
    main_stat: Stat
    sub_stats: List[Stat]


def get_cell_position(row: int, col: int) -> Tuple[int, int]:
    """Calculate the screen coordinates for a given grid position."""
    x = START_POS[0] + (col * CELL_SIZE[0])
    y = START_POS[1] + (row * CELL_SIZE[1])
    return x, y


def click_position(x: int, y: int, duration: float = 0.2) -> None:
    """Click at the specified coordinates with smooth movement."""
    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.3)


def capture_region(output_path: str, region: Dict) -> None:
    """Capture a specific region of the screen."""
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(output_path, img_bgr)


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


def parse_stat_line(line: str) -> Stat:
    """Parse a single stat line into structured data."""
    # Remove any unwanted characters and normalize spaces
    line = line.strip().replace('\n', ' ').replace('\r', '')

    # Regular expression patterns
    percentage_pattern = r'([\d.]+)%'
    value_pattern = r'([\d.]+)(?!%)'
    enhancement_pattern = r'\+(\d+)'

    # Initialize variables
    stat_type = line
    value = 0.0
    is_percentage = False
    enhancement_level = 0

    # Extract enhancement level if present
    enhancement_match = re.search(enhancement_pattern, line)
    if enhancement_match:
        enhancement_level = int(enhancement_match.group(1))
        stat_type = re.sub(r'\+\d+', '', stat_type).strip()

    # Check for percentage values
    percentage_match = re.search(percentage_pattern, line)
    if percentage_match:
        value = float(percentage_match.group(1))
        is_percentage = True
    else:
        # Look for regular numeric values
        value_match = re.search(value_pattern, line)
        if value_match:
            value = float(value_match.group(1))

    # Clean up stat type by removing the value and any trailing/leading spaces
    stat_type = re.sub(r'[\d.]+%?', '', stat_type).strip()

    # Add enhancement level back to type if present
    if enhancement_level > 0:
        stat_type = f"{stat_type} +{enhancement_level}"

    return Stat(type=stat_type, value=value, is_percentage=is_percentage)


def parse_sub_stats(image_path: str) -> str:
    """Parse sub stats from image using OCR."""
    binary = preprocess_image(image_path)
    return pytesseract.image_to_string(binary, config=SUB_STAT_CONFIG)
