import math

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

SUBSTATS = {
    "CRIT Rate": 2.4, "CRIT DMG": 4.8, "Anomaly Proficiency": 9, "ATK%": 3, "Flat ATK": 19,
    "Flat HP": 112, "HP%": 3, "Flat DEF": 15, "DEF%": 4.8, "PEN": 9
}


def disk_potential(level, substats, starting_substats=4):
    # Constants
    MAX_LEVEL = 15
    LEVELS_PER_UPGRADE = 3
    ALPHA = 0.15  # Exponential decay rate

    # Calculate current value of the substats
    current_value = sum(SUBSTAT_WEIGHTS[stat] * value for stat, value in substats.items())

    # Calculate remaining upgrades
    total_upgrades = max(0, (MAX_LEVEL - level) // LEVELS_PER_UPGRADE)
    meaningful_upgrades = total_upgrades - (1 if starting_substats == 3 else 0)

    # Average potential gain per upgrade
    average_gain = sum(SUBSTAT_WEIGHTS.values()) / len(SUBSTAT_WEIGHTS)

    # Expected value of the 4th substat (only applies for 3-starting substat disks)
    fourth_substat_value = 0
    if starting_substats == 3 and level < MAX_LEVEL:
        # Expectation: average weight multiplied by average base value
        average_weight = sum(SUBSTAT_WEIGHTS.values()) / len(SUBSTAT_WEIGHTS)
        average_base_value = sum(SUBSTATS.values()) / len(SUBSTATS)
        fourth_substat_value = average_weight * average_base_value

    # Potential from future upgrades
    future_potential = meaningful_upgrades * average_gain

    # Add the 4th substat value to potential if applicable
    if starting_substats == 3:
        future_potential += fourth_substat_value

    # Apply exponential decay for higher levels
    level_penalty = math.exp(-ALPHA * level)

    # Combine current value and future potential
    total_potential = (current_value + future_potential) * level_penalty

    return total_potential


def main():
    level = 6
    substats_3 = {"CRIT Rate": 2.4, "ATK%": 3, "Flat ATK": 19}  # Disk with 3 starting substats
    substats_4 = {"CRIT Rate": 2.4, "ATK%": 3, "Flat ATK": 19, "CRIT DMG": 9}  # Disk with 4 starting substats

    print("3-substat Disk Potential:", disk_potential(level, substats_3, starting_substats=3))
    print("4-substat Disk Potential:", disk_potential(level, substats_4, starting_substats=4))

if __name__ == "__main__":
    main()