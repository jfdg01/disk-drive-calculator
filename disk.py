import random
from constants import MAIN_STATS, MAIN_STAT_WEIGHTS, SUBSTATS, SUBSTAT_WEIGHTS, ELEMENTAL_TYPES


class Disk:
    def __init__(self, slot=None, main_stat=None, initial_substat_number=None, substats=None):
        """
        Initialize a Disk instance.

        :param slot: Slot number (1-6). Randomized if not provided.
        :param main_stat: Main stat for the disk. Randomized if not provided.
        :param initial_substat_number: Number of initial substats (3 or 4). Randomized if not provided.
        :param substats: Predefined substats. Randomized if not provided.
        """
        self.slot = slot or random.randint(1, 6)
        self.main_stat = main_stat or self._generate_main_stat()
        self.initial_substat_number = initial_substat_number or random.randint(3, 4)
        self.level = 0
        self.substats = substats or self._generate_substats()
        self.substat_values = SUBSTATS  # Reference to predefined substat upgrade values

    def _generate_main_stat(self):
        """
        Randomly generate a main stat based on slot-specific probabilities.
        """
        main_stat = random.choices(MAIN_STATS[self.slot], weights=list(MAIN_STAT_WEIGHTS[self.slot].values()))[0]
        if self.slot == 5 and main_stat == "Element DMG Bonus":
            main_stat = random.choice(ELEMENTAL_TYPES) + " DMG Bonus"
        return main_stat

    def _generate_substats(self):
        """
        Randomly generate substats based on the initial substat number.
        """
        available_substats = [s for s in SUBSTATS if s != self.main_stat]
        selected_substats = random.sample(available_substats, self.initial_substat_number)
        return {stat: 0 for stat in selected_substats}

    def level_up(self):
        """
        Level up the disk, adding a new substat if necessary or upgrading existing ones.
        """
        self.level += 1

        # If the disk starts with 3 substats, add the 4th substat at level 1
        if self.initial_substat_number == 3 and len(self.substats) < 4:
            available_substats = [s for s in SUBSTATS if s != self.main_stat and s not in self.substats]
            new_substat = random.choice(available_substats)
            self.substats[new_substat] = 0
            print(f"Added new substat: {new_substat}")
            return  # End the level-up here as we've just added the new substat

        # Otherwise, upgrade a random substat
        substat_to_upgrade = random.choice(list(self.substats.keys()))
        upgrade_value = self.substat_values[substat_to_upgrade]
        self.substats[substat_to_upgrade] += upgrade_value
        print(f"Upgraded substat: {substat_to_upgrade} by +{upgrade_value}")

    def calculate_main_stat_score(self):
        """
        Calculate the score of the main stat based on its slot and value.
        """
        return MAIN_STAT_WEIGHTS.get(self.slot, {}).get(self.main_stat, 0)

    def calculate_substat_potential(self):
        """
        Calculate the current and potential substat scores with an adjusted heuristic that
        factors in both the substat weights and the variance (risk) of upgrading them,
        including the new substat penalty for disks with 3 initial substats.
        """
        current_score = sum(SUBSTAT_WEIGHTS.get(stat, 0) for stat in self.substats)

        # Calculate expected value for each substat based on weight and potential upgrade
        expected_value_score = sum(
            SUBSTAT_WEIGHTS.get(stat, 0) * (SUBSTATS.get(stat, 0) / 100)  # Expected value based on average upgrade
            for stat in self.substats
        )

        # Base remaining rolls calculation (same as before)
        remaining_rolls = max(0, 5 - self.level)  # Base remaining rolls

        # If there are 3 initial substats, one of the upgrades will be used to add a new substat
        if self.initial_substat_number == 3 and len(self.substats) < 4:
            remaining_rolls -= 1  # Deduct one roll for adding the 4th substat

        # Adjusted potential score calculation, factoring in remaining rolls
        adjusted_potential_score = sum(
            (SUBSTAT_WEIGHTS.get(stat, 0) * (remaining_rolls / 5))  # Adjusted based on remaining rolls
            for stat in self.substats
        )

        # Now we calculate the potential by blending the riskier and more valuable substats
        max_potential_score = expected_value_score + adjusted_potential_score

        return current_score, max_potential_score

    def evaluate(self):
        """
        Evaluate the disk, calculating scores for the main stat, substats, and potential.
        """
        main_stat_score = self.calculate_main_stat_score()
        current_score, potential_score = self.calculate_substat_potential()
        total_score = main_stat_score + current_score + potential_score
        return {
            "Main Stat Score": main_stat_score,
            "Current Substat Score": current_score,
            "Potential Substat Score": potential_score,
            "Total Score": total_score,
        }

    def display(self):
        """
        Display the details of the disk, including substats and evaluation scores.
        """
        print(
            f"Slot: {self.slot}, Main Stat: {self.main_stat}, Level: {self.level}, Initial Substats: {self.initial_substat_number}")
        for substat, upgrade in self.substats.items():
            print(f"  {substat}: +{upgrade if upgrade > 0 else 0}")
        print()

        evaluation = self.evaluate()
        print("Evaluation:")
        print(f"  Main Stat Score: {evaluation['Main Stat Score']}")
        print(f"  Current Substat Score: {evaluation['Current Substat Score']}")
        print(f"  Potential Substat Score: {evaluation['Potential Substat Score']}")
        print(f"  Total Score: {evaluation['Total Score']}")
