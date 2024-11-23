import random

MAIN_STATS = {
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

def generate_disk():
    """Generate a disk with randomized attributes."""

    slot = random.randint(1, 6)
    main_stat = random.choices(list(MAIN_STATS[slot].keys()), weights=list(MAIN_STATS[slot].values()))[0]
    if slot == 5 and main_stat == "Element DMG Bonus":
        main_stat = random.choice(ELEMENTAL_TYPES) + " DMG Bonus"

    initial_substat_count = random.randint(3, 4)
    available_substats = [s for s in SUBSTATS if s != main_stat]
    selected_substats = random.sample(available_substats, initial_substat_count)

    substat_upgrades = {stat: 0 for stat in selected_substats}

    return {
        "Slot": slot,
        "Main Stat": main_stat,
        "Level": 0,
        "Rarity": "S",
        "Substats": substat_upgrades,
        "Substat Values": {stat: SUBSTATS[stat] for stat in SUBSTATS},
    }

def calculate_main_stat_score(slot, main_stat):
    slot_weights = MAIN_STATS.get(slot, {})
    return slot_weights.get(main_stat, 4)

def calculate_substat_potential(disk):
    substat_weights = {
        "CRIT Rate": 10, "CRIT DMG": 10, "ATK%": 8,
        "Flat ATK": 5, "PEN": 5, "Anomaly Proficiency": 5,
        "Flat HP": 2, "HP%": 2, "Flat DEF": 2, "DEF%": 2,
    }

    current_score = sum(substat_weights.get(stat, 0) for stat in disk["Substats"])
    remaining_rolls = 5
    max_potential_score = sum(
        substat_weights.get(stat, 0) * remaining_rolls
        for stat in disk["Substats"]
    )

    return current_score, max_potential_score


def evaluate_disk(disk):
    main_stat_score = calculate_main_stat_score(disk["Slot"], disk["Main Stat"])
    current_score, potential_score = calculate_substat_potential(disk)
    total_score = main_stat_score + current_score + potential_score

    return {
        "Main Stat Score": main_stat_score,
        "Current Substat Score": current_score,
        "Potential Substat Score": potential_score,
        "Total Score": total_score,
    }


def display_disk(disk):
    print(f"Slot: {disk['Slot']}, Main Stat: {disk['Main Stat']}, Level: {disk['Level']}")
    for substat, upgrade in disk["Substats"].items():
        print(f"  {substat}: {'+' + str(upgrade) if upgrade > 0 else ''}")
    print()

    evaluation = evaluate_disk(disk)
    print("Evaluation:")
    print(f"  Main Stat Score: {evaluation['Main Stat Score']}")
    print(f"  Current Substat Score: {evaluation['Current Substat Score']}")
    print(f"  Potential Substat Score: {evaluation['Potential Substat Score']}")
    print(f"  Total Score: {evaluation['Total Score']}")


def input_disk():
    slot = int(input("Enter Slot (1-6): "))

    main_stats_map = {
        1: ["Flat HP"],
        2: ["Flat ATK"],
        3: ["Flat DEF"],
        4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
        5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
        6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"],
    }

    if slot in [1, 2, 3]:
        main_stat = main_stats_map[slot][0]
    else:
        main_stat_options = main_stats_map[slot]
        for i, stat in enumerate(main_stat_options, 1):
            print(f"{i}: {stat}")
        main_stat_index = int(input("Select Main Stat: ")) - 1
        main_stat = main_stat_options[main_stat_index]

    substats_map = [
        "CRIT Rate", "CRIT DMG", "Anomaly Proficiency", "ATK%", "Flat ATK",
        "Flat HP", "HP%", "Flat DEF", "DEF%", "PEN"
    ]

    available_substats = [s for s in substats_map if s != main_stat]
    substats_count = int(input("Enter number of initial substats (3 or 4): "))
    selected_substats = []
    for _ in range(substats_count):
        for i, substat in enumerate(available_substats, 1):
            print(f"{i}: {substat}")
        substat_index = int(input("Select Substat: ")) - 1
        selected_substats.append(available_substats[substat_index])

    disk = {
        "Slot": slot,
        "Main Stat": main_stat,
        "Level": 0,
        "Rarity": "S",
        "Substats": {stat: 0 for stat in selected_substats},
        "Substat Values": {
            "HP%": 3, "ATK%": 3, "DEF%": 4.8, "CRIT Rate": 2.4, "CRIT DMG": 4.8,
            "PEN": 9, "PEN Ratio": 9, "Anomaly Proficiency": 9, "Flat HP": 112, "Flat ATK": 19, "Flat DEF": 15
        },
    }
    return disk


def main():
    print("Welcome to the Disk CLI!")
    while True:
        print("1. Generate Disk")
        print("2. Input Disk")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            disk = generate_disk()
            display_disk(disk)
        elif choice == "2":
            disk = input_disk()
            display_disk(disk)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
