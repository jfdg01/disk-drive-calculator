#main.py
from flask import Flask, request, render_template, redirect, url_for
import random

app = Flask(__name__)

def generate_disk():
    # Define slot-specific main stats
    main_stats = {
        1: ["Flat HP"],
        2: ["Flat ATK"],
        3: ["Flat DEF"],
        4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
        5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
        6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"],
    }

    # Define elemental subtypes
    elemental_types = ["Physical", "Fire", "Ice", "Electric", "Ether"]

    # Define possible substats
    substats = [
        "CRIT Rate", "CRIT DMG", "Anomaly Proficiency", "ATK%", "Flat ATK",
        "Flat HP", "HP%", "Flat DEF", "DEF%", "PEN"
    ]

    # Define S-rank rarity properties
    rarity_data = {
        "initial_substats": (3, 4),
        "substat_values": {
            "HP%": 3, "ATK%": 3, "DEF%": 4.8, "CRIT Rate": 2.4, "CRIT DMG": 4.8,
            "PEN": 9, "PEN Ratio": 9, "Anomaly Proficiency": 9, "Flat HP": 112, "Flat ATK": 19, "Flat DEF": 15
        }
    }

    # Step 1: Select the slot (1-6)
    slot = random.randint(1, 6)

    # Step 2: Select the main stat for the slot
    main_stat = random.choice(main_stats[slot])
    if slot == 5 and main_stat == "Element DMG Bonus":
        main_stat = random.choice(elemental_types)  # Refine Elemental into a specific type

    # Step 3: Determine the number of initial substats
    initial_substat_count = random.randint(*rarity_data["initial_substats"])

    # Step 4: Select substats, excluding the main stat and avoiding duplicates
    available_substats = [s for s in substats if s != main_stat]
    selected_substats = random.sample(available_substats, initial_substat_count)

    # Initialize substat upgrades
    substat_upgrades = {stat: 0 for stat in selected_substats}

    # Return the generated disk as a dictionary
    return {
        "Slot": slot,
        "Main Stat": main_stat,
        "Level": 0,
        "Rarity": "S",
        "Substats": substat_upgrades,
        "Substat Values": rarity_data["substat_values"],
    }

def calculate_main_stat_score(slot, main_stat):
    """Assign weight to main stat based on slot."""
    main_stat_weights = {
        1: {"Flat HP": 10},
        2: {"Flat ATK": 10},
        3: {"Flat DEF": 10},
        4: {"CRIT Rate": 10, "CRIT DMG": 10, "HP%": 5, "ATK%": 5, "DEF%": 5, "Anomaly Proficiency": 4},
        5: {"Element Damage Bonus": 10, "ATK%": 8, "HP%": 4, "DEF%": 4},
        6: {"ATK%": 10, "HP%": 5, "DEF%": 5, "Energy Regen%": 5, "Anomaly Mastery": 4},
    }

    # Get weights for the slot, default to 4 if the main stat isn't explicitly listed
    slot_weights = main_stat_weights.get(slot, {})
    return slot_weights.get(main_stat, 4)  # Default weight is 4 for less desirable stats.

def calculate_substat_potential(disk):
    """Evaluate the potential of substats based on current substats and possible upgrades."""
    substat_weights = {
        "CRIT Rate": 10, "CRIT DMG": 10, "ATK%": 8,
        "Flat ATK": 5, "PEN": 5, "Anomaly Proficiency": 5,
        "Flat HP": 2, "HP%": 2, "Flat DEF": 2, "DEF%": 2,
    }

    # Score for the current substats
    current_score = sum(substat_weights.get(stat, 0) for stat in disk["Substats"])

    # Maximum potential improvement per substat based on remaining rolls
    remaining_rolls = 5  # Fixed as disks can be upgraded 5 times
    max_potential_score = sum(
        substat_weights.get(stat, 0) * remaining_rolls
        for stat in disk["Substats"]
    )

    return current_score, max_potential_score

def evaluate_disk(disk):
    """Combine scores to evaluate the current state and potential of the disk."""
    # Main stat contribution
    main_stat_score = calculate_main_stat_score(disk["Slot"], disk["Main Stat"])

    # Substat contributions
    current_score, potential_score = calculate_substat_potential(disk)

    # Total score as a heuristic combination
    total_score = main_stat_score + current_score + potential_score

    return {
        "Main Stat Score": main_stat_score,
        "Current Substat Score": current_score,
        "Potential Substat Score": potential_score,
        "Total Score": total_score,
    }

def display_disk(disk):
    print(f"{disk['Slot']} [{disk['Main Stat']}] lvl {disk['Level']}")
    for substat, upgrade in disk["Substats"].items():
        print(f"{substat} {'+' + str(upgrade) if upgrade > 0 else ''}")
    print()

    # Display evaluation
    evaluation = evaluate_disk(disk)
    print("Evaluation:")
    print(f"Main Stat Score: {evaluation['Main Stat Score']}")
    print(f"Current Substat Score: {evaluation['Current Substat Score']}")
    print(f"Potential Substat Score: {evaluation['Potential Substat Score']}")
    print(f"Total Score: {evaluation['Total Score']}\n")


def input_disk():
    # Input slot
    slot = int(input("Enter Slot (1-6): "))

    # Define main stats map
    main_stats_map = {
        1: ["Flat HP"],
        2: ["Flat ATK"],
        3: ["Flat DEF"],
        4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
        5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
        6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"],
    }

    # Automatically select main stat for slots 1, 2, or 3
    if slot in [1, 2, 3]:
        main_stat = main_stats_map[slot][0]
    else:
        # Display options and allow manual selection for other slots
        main_stat_options = main_stats_map[slot]
        print(f"Available Main Stats for Slot {slot}:")
        for i, stat in enumerate(main_stat_options, 1):
            print(f"{i}: {stat}")

        main_stat_index = int(input("Select Main Stat: ")) - 1
        main_stat = main_stat_options[main_stat_index]

    # Input substats
    substats_map = [
        "CRIT Rate", "CRIT DMG", "Anomaly Proficiency", "ATK%", "Flat ATK",
        "Flat HP", "HP%", "Flat DEF", "DEF%", "PEN"
    ]

    # Filter out the main stat from the substats list
    available_substats = [s for s in substats_map if s != main_stat]

    substats_count = int(input("Enter number of initial substats (3 or 4): "))
    while substats_count not in [3, 4]:
        substats_count = int(input("Enter number of initial substats (3 or 4): "))

    selected_substats = []
    print("Available Substats:")
    for i, substat in enumerate(available_substats, 1):
        print(f"{i}: {substat}")
    for _ in range(substats_count):
        while True:
            substat_index = int(input(f"Select Substat {_ + 1}: ")) - 1
            chosen_substat = available_substats[substat_index]

            # Ensure no duplicates
            if chosen_substat in selected_substats:
                print("Substat already selected. Choose another.")
            else:
                selected_substats.append(chosen_substat)
                break

    # Create the disk with input values
    disk = {
        "Slot": slot,
        "Main Stat": main_stat,
        "Level": 0,
        "EXP": 0,
        "Max Level": 15,
        "Rarity": "S",
        "Substats": {stat: 0 for stat in selected_substats},
        "Available Substats": [s for s in available_substats if s not in selected_substats],
        "Substat Values": {
            "HP%": 3, "ATK%": 3, "DEF%": 4.8, "CRIT Rate": 2.4, "CRIT DMG": 4.8,
            "PEN": 9, "PEN Ratio": 9, "Anomaly Proficiency": 9, "Flat HP": 112, "Flat ATK": 19, "Flat DEF": 15
        },
    }
    return disk

current_disk = None


def update_disk(disk, form_data):
    """Update disk properties based on form data."""
    disk["Slot"] = int(form_data.get("slot", disk["Slot"]))
    disk["Main Stat"] = form_data.get("main_stat", disk["Main Stat"])

    # Update substats
    new_substats = form_data.getlist("substats")
    disk["Substats"] = {stat: disk["Substats"].get(stat, 0) for stat in new_substats}

    return disk

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    global current_disk
    if request.method == 'POST':
        current_disk = generate_disk()  # Generate a new disk

    # If GET, show the existing disk and its evaluation
    evaluation = evaluate_disk(current_disk)
    return render_template('show_disk.html', disk=current_disk, evaluation=evaluation)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    global current_disk
    # Define slot-specific main stats
    main_stats_map = {
        1: ["Flat HP"],
        2: ["Flat ATK"],
        3: ["Flat DEF"],
        4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
        5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
        6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"],
    }

    if request.method == 'POST':
        # Update disk with submitted form data
        current_disk = update_disk(current_disk, request.form)
        return redirect(url_for('generate'))  # Redirect to re-evaluate the disk

    # Determine the main stats for the current slot
    slot = current_disk["Slot"]
    main_stats = main_stats_map.get(slot, [])

    # Show edit form
    return render_template('edit_disk.html', disk=current_disk, main_stats=main_stats)


if __name__ == '__main__':
    app.run(debug=True)

# def main():
#     disk = input_disk()
#
#     display_disk(disk)
#
#     choice = input("Press ENTER to leave")