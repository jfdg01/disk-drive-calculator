from xml.dom.xmlbuilder import DOMBuilder, DOMBuilderFilter

SUBSTAT_WEIGHTS = {
    "CRIT Rate": 10,
    "CRIT DMG": 10,
    "ATK%": 7,
    "Flat ATK": 5,
    "PEN": 5,
    "Anomaly Proficiency": 5,
    "Flat HP": 0,
    "HP%": 0,
    "Flat DEF": 0,
    "DEF%": 0,
}

RESOLUTION = (1920, 1080)
# RESOLUTION = (2560, 1440)

# START_POS = (260, 280)  # Top-left cell center
START_POS_PERCENTAGE = (0.1354, 0.2593)  # (x%, y%)
START_POS = (int(START_POS_PERCENTAGE[0] * RESOLUTION[0]), int(START_POS_PERCENTAGE[1] * RESOLUTION[1]))

# HORIZONTAL_DIFF = 402 - 260  # Difference between adjacent columns
HORIZONTAL_DIFF_PERCENTAGE = 0.07396  # Percentage of screen width
HORIZONTAL_DIFF = int(HORIZONTAL_DIFF_PERCENTAGE * RESOLUTION[0])

# VERTICAL_DIFF = 465 - 280  # Difference between adjacent rows
VERTICAL_DIFF_PERCENTAGE = 0.1713  # Percentage of screen height
VERTICAL_DIFF = int(VERTICAL_DIFF_PERCENTAGE * RESOLUTION[1])

# CELL_SIZE = (HORIZONTAL_DIFF, VERTICAL_DIFF)
CELL_SIZE_PERCENTAGE = (HORIZONTAL_DIFF, VERTICAL_DIFF)
CELL_SIZE = (int(HORIZONTAL_DIFF_PERCENTAGE * RESOLUTION[0]), int(VERTICAL_DIFF_PERCENTAGE * RESOLUTION[1]))

DATABASE_URL = "http://localhost:8090/api"
API_URL = "http://localhost:8000"

ROWS = 4
COLS = 8
GRAY_THRESHOLD = 120
MAX_GRAY_VALUE = 255
MAIN_STAT_CONFIG = '--psm 7' # Treat the image as a single text line
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
IMAGE_EXTENSION = "jpg" # Extension to use for the output: jpg or png, seems to be no difference

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

MAIN_STATS_STARTING_VALUES = {
    "Flat HP": 550, "Flat ATK": 79, "Flat DEF": 46, "HP%": 7.5, "ATK%": 7.5, "DEF%": 12, "CRIT Rate": 6, "CRIT DMG": 12,
    "Anomaly Proficiency": 23, "PEN": 6, "Element DMG Bonus": 7.5, "Anomaly Mastery": 7.5, "Impact": 4.5,
    "Energy Regen%": 15
}

MAIN_STAT_LEVELS = {
    "Flat HP": [0, 550, 660, 770, 880, 990, 1100, 1210, 1320, 1430, 1540, 1650, 1760, 1870, 1980, 2090, 2200],
    "Flat ATK": [0, 79, 94, 110, 126, 142, 158, 173, 189, 205, 221, 237, 252, 268, 284, 300, 316],
    "Flat DEF": [0, 46, 55, 64, 73, 82, 92, 101, 110, 119, 128, 138, 147, 156, 165, 174, 184],
    "ATK%": [0, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24, 25.5, 27, 28.5, 30],
    "HP%": [0, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24, 25.5, 27, 28.5, 30],
    "DEF%": [0, 12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 31.2, 33.6, 36, 38.4, 40.8, 43.2, 45.6, 48],
    "CRIT Rate": [0, 6, 7.2, 8.4, 9.6, 10.8, 12, 13.2, 14.4, 15.6, 16.8, 18, 19.2, 20.4, 21.6, 22.8, 24],
    "CRIT DMG": [0, 12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 31.2, 33.6, 36, 38.4, 40.8, 43.2, 45.6, 48],
    "Anomaly Proficiency": [0, 23, 27, 32, 36, 41, 46, 50, 55, 59, 64, 69, 73, 78, 82, 87, 92],
    "PEN Ratio": [0, 6, 7.2, 8.4, 9.6, 10.8, 12, 13.2, 14.4, 15.6, 16.8, 18, 19.2, 20.4, 21.6, 22.8, 24],
    "Element DMG Bonus": [0, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24, 25.5, 27, 28.5, 30],
    "Anomaly Mastery": [0, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24, 25.5, 27, 28.5, 30],
    "Impact": [0, 4.5, 5.4, 6.3, 7.2, 8.1, 9, 9.9, 10.8, 11.7, 12.6, 13.5, 14.4, 15.3, 16.2, 17.1, 18],
    "Energy Regen": [0, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60],
}

MAIN_STATS_UPGRADE_VALUES = {
    "Flat HP": 10, "Flat ATK": 10, "Flat DEF": 10, "HP%": 10, "ATK%": 10, "DEF%": 10, "CRIT Rate": 10, "CRIT DMG": 10,
    "Anomaly Proficiency": 10, "PEN": 10, "Element DMG Bonus": 10,
}

TOP = 46.09375
LEFT = 73.4
WIDTH = 21.97
HEIGHT = 4.84375
TOP_MAIN = 38.854166666

MAIN_STAT_REGION = {
    "left": LEFT,
    "top": TOP_MAIN,
    "width": WIDTH,
    "height": HEIGHT
}

FULL_SUB_STAT_REGION = {
    "left": LEFT,
    "top": TOP,
    "width": WIDTH,
    "height": HEIGHT * 4
}

SUB_STAT_REGION_1 = {
    "left": LEFT,
    "top": TOP + HEIGHT * 0,
    "width": WIDTH,
    "height": HEIGHT
}

SUB_STAT_REGION_2 = {
    "left": LEFT,
    "top": TOP + HEIGHT * 1,
    "width": WIDTH,
    "height": HEIGHT
}

SUB_STAT_REGION_3 = {
    "left": LEFT,
    "top": TOP + HEIGHT * 2,
    "width": WIDTH,
    "height": HEIGHT
}

SUB_STAT_REGION_4 = {
    "left": LEFT,
    "top": TOP + HEIGHT * 3,
    "width": WIDTH,
    "height": HEIGHT
}
