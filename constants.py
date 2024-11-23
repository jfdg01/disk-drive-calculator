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