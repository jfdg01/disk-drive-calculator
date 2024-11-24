START_POS = (260, 280)  # Top-left cell center
HORIZONTAL_DIFF = 402 - 260  # Difference between adjacent columns
VERTICAL_DIFF = 465 - 280  # Difference between adjacent rows
CELL_SIZE = (HORIZONTAL_DIFF, VERTICAL_DIFF)
ROWS = 4
COLS = 8
GRAY_THRESHOLD = 120
MAX_GRAY_VALUE = 255
MAIN_STAT_CONFIG = '--psm 7'
SUB_STAT_CONFIG = '--psm 11'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

MAIN_STATS = {
    1: ["Flat HP"],
    2: ["Flat ATK"],
    3: ["Flat DEF"],
    4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
    5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
    6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"],
}

MAIN_STAT_WEIGHTS = {
    1: {"Flat HP": 10},
    2: {"Flat ATK": 10},
    3: {"Flat DEF": 10},
    4: {"HP%": 0, "ATK%": 5, "DEF%": 0, "CRIT Rate": 10, "CRIT DMG": 10, "Anomaly Proficiency": 0},
    5: {"HP%": 0, "ATK%": 8, "DEF%": 0, "PEN Ratio": 5, "Element DMG Bonus": 10},
    6: {"HP%": 0, "ATK%": 10, "DEF%": 0, "Anomaly Mastery": 0, "Impact": 0, "Energy Regen%": 0},
}

ELEMENTAL_TYPES = ["Physical", "Fire", "Ice", "Electric", "Ether"]

SUBSTATS = {
    "CRIT Rate": 2.4, "CRIT DMG": 4.8, "Anomaly Proficiency": 9, "ATK%": 3, "Flat ATK": 19,
    "Flat HP": 112, "HP%": 3, "Flat DEF": 15, "DEF%": 4.8, "PEN": 9
}

SUBSTAT_WEIGHTS = {
    "CRIT Rate": 10, "CRIT DMG": 10, "ATK%": 8,
    "Flat ATK": 5, "PEN": 5, "Anomaly Proficiency": 5,
    "Flat HP": 2, "HP%": 2, "Flat DEF": 2, "DEF%": 2,
}

RESOLUTION = (1920, 1080)

MAIN_STAT_REGION = {
    "left": 74.0,
    "top": 38.89,
    "width": 20.83,
    "height": 4.63
}

FULL_SUB_STAT_REGION = {
    "left": 74.0,
    "top": 46.3,
    "width": 20.83,
    "height": 18.52
}

SUB_STAT_REGION_1 = {
    "left": 74.0,
    "top": 46.3,
    "width": 20.83,
    "height": 4.63
}

SUB_STAT_REGION_2 = {
    "left": 74.0,
    "top": 46.3 + 4.63,
    "width": 20.83,
    "height": 4.63
}

SUB_STAT_REGION_3 = {
    "left": 74.0,
    "top": 46.3 + 4.63 * 2,
    "width": 20.83,
    "height": 4.63
}

SUB_STAT_REGION_4 = {
    "left": 74.0,
    "top": 46.3 + 4.63 * 3,
    "width": 20.83,
    "height": 4.63
}

START_POS_PERCENTAGE = (0.1354, 0.2593)  # (x%, y%)
HORIZONTAL_DIFF_PERCENTAGE = 0.07396  # Percentage of screen width
VERTICAL_DIFF_PERCENTAGE = 0.1713  # Percentage of screen height
CELL_SIZE_PERCENTAGE = (HORIZONTAL_DIFF, VERTICAL_DIFF)