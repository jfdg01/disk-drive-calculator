from tkinter.tix import IMAGE

START_POS = (260, 280)  # Top-left cell center
HORIZONTAL_DIFF = 402 - 260  # Difference between adjacent columns
VERTICAL_DIFF = 465 - 280  # Difference between adjacent rows
CELL_SIZE = (HORIZONTAL_DIFF, VERTICAL_DIFF)
ROWS = 4
COLS = 8
GRAY_THRESHOLD = 120
MAX_GRAY_VALUE = 255
MAIN_STAT_CONFIG = '--psm 7'
# SUB_STAT_CONFIG = '--psm 11'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
RESOLUTION = (1920, 1080)
START_POS_PERCENTAGE = (0.1354, 0.2593)  # (x%, y%)
HORIZONTAL_DIFF_PERCENTAGE = 0.07396  # Percentage of screen width
VERTICAL_DIFF_PERCENTAGE = 0.1713  # Percentage of screen height
CELL_SIZE_PERCENTAGE = (HORIZONTAL_DIFF, VERTICAL_DIFF)
IMAGE_EXTENSION = "jpg"

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
    "Anomaly Proficiency": 23, "PEN": 6, "Element DMG Bonus": 7.5, "Anomaly Mastery": 7.5, "Impact": 4.5, "Energy Regen%": 15
}

# HP(110): 550 660 770 880 990 1100 1210 1320 1430 1540 1650 1760 1870 1980 2090 2200 # Total values
#            0 110 220 330 440 550  660  770  880  990  1100 1210 1320 1430 1540 1650 # Agregated sum
#              110 110 110 110 110  110  110  110  110  110  110  110  110  110  110  # Individual sum
#
# ATK(15.8): 79 94 110 126 142 158 173 189 205 221 237 252 268 284 300 316 # Total values
#             0 15 31  47  63  79  94  110 126 142 158 173 189 205 221 237 # Agregated sum
#               15 16  16  16  16  15  16  16  16  16  15  16  16  16  16  # Individual sum
#
# DEF (9.2): 46 55 64 73 82 91 100 109 118 127 136 145 154 163 172 181 # Total values
#             0  9 18 27 36 46  55  64  73  82  92 101 110 119 128 138 # Agregated sum
#                9 9  9  9  10  9   9   9   9   10   9   9   9   9  10  # Individual sum
#
# ATK% (1.5): 7.5 9   10.5 12  13.5 15  16.5 18   19.5 21   22.5 24   25.5 27   28.5 30   # Total values
#             0 1.5 3    4.5 6    7.5 9    10.5 12   13.5 15   16.5 18   19.5 21   22.5   # Agregated sum
#               1.5 1.5  1.5 1.5  1.5 1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5    # Individual sum
#
# HP% (1.5):  7.5 9   10.5 12  13.5 15  16.5 18   19.5 21   22.5 24   25.5 27   28.5 30   # Total values
#             0 1.5 3    4.5 6    7.5 9    10.5 12   13.5 15   16.5 18   19.5 21   22.5   # Agregated sum
#               1.5 1.5  1.5 1.5  1.5 1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5  1.5    # Individual sum
#
# DEF% (2.4): 12 14.4 16.8 19.2 21.6 24  26.4 28.8 31.2 33.6 36  38.4 40.8 43.2 45.6 48   # Total values
#              0 2.4  4.8  7.2  9.6  12  14.4 16.8 19.2 21.6 24  26.4 28.8 31.2 33.6 36   # Agregated sum
#                2.4  2.4  2.4  2.4  2.4 2.4  2.4  2.4  2.4  2.4 2.4  2.4  2.4  2.4  2.4  # Individual sum
#
# CRIT Rate (1.2): 6 7.2 8.4 9.6 10.8 12  13.2 14.4 15.6 16.8 18 19.2 20.4 21.6 22.8 24   # Total values
#                  0 1.2 2.4 3.6 4.8  6   7.2  8.4  9.6  10.8 12 13.2 14.4 15.6 16.8 18   # Agregated sum
#                    1.2 1.2 1.2 1.2  1.2 1.2  1.2  1.2  1.2  1.2 1.2 1.2  1.2  1.2  1.2  # Individual sum
#
# CRIT DMG (2.4): 12 14.4 16.8 19.2 21.6 24  26.4 28.8 31.2 33.6 36  38.4 40.8 43.2 45.6 48   # Total values
#                  0 2.4  4.8  7.2  9.6  12  14.4 16.8 19.2 21.6 24  26.4 28.8 31.2 33.6 36   # Agregated sum
#                    2.4  2.4  2.4  2.4  2.4 2.4  2.4  2.4  2.4  2.4 2.4  2.4  2.4  2.4  2.4  # Individual sum
#
# Anomaly Proficiency (4.6): 23 27 32 36 41 46 50 55 59 64 69 73 78 82 87 92   # Total values
#                             0 4  9  13 18 23 27 32 36 41 46 50 55 59 64 69   # Agregated sum
#                               4  5  4  5  5  4  5  4  5  5  4  5  4  5  5    # Individual sum
#
# PEN (1.2): 6 7.2 8.4 9.6 10.8 12  13.2 14.4 15.6 16.8 18  19.2 20.4 21.6 22.8 24   # Total values
#            0 1.2 2.4 3.6 4.8  6   7.2  8.4  9.6  10.8 12  13.2 14.4 15.6 16.8 18   # Agregated sum
#              1.2 1.2 1.2 1.2  1.2 1.2  1.2  1.2  1.2  1.2 1.2  1.2  1.2  1.2  1.2  # Individual sum

MAIN_STATS_UPGRADE_VALUES = {
    "Flat HP": 10, "Flat ATK": 10, "Flat DEF": 10, "HP%": 10, "ATK%": 10, "DEF%": 10, "CRIT Rate": 10, "CRIT DMG": 10,
    "Anomaly Proficiency": 10, "PEN": 10, "Element DMG Bonus": 10,
}

SUBSTAT_WEIGHTS = {
    "CRIT Rate": 10, "CRIT DMG": 10, "ATK%": 8,
    "Flat ATK": 5, "PEN": 5, "Anomaly Proficiency": 5,
    "Flat HP": 2, "HP%": 2, "Flat DEF": 2, "DEF%": 2,
}

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
