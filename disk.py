import random
from constants import MAIN_STATS, MAIN_STAT_WEIGHTS, SUBSTATS, SUBSTAT_WEIGHTS, ELEMENTAL_TYPES

class Disk:
    def __init__(self, slot=None, main_stat=None, substats=None):
        self.slot = slot or random.randint(1, 6)
        self.main_stat = main_stat or self._generate_main_stat()
        self.level = 0
        self.substats = substats or self._generate_substats()

    def _generate_main_stat(self):
        main_stat = random.choices(MAIN_STATS[self.slot], weights=list(MAIN_STAT_WEIGHTS[self.slot].values()))[0]
        if self.slot == 5 and main_stat == "Element DMG Bonus":
            main_stat = random.choice(ELEMENTAL_TYPES) + " DMG Bonus"
        return main_stat

    def _generate_substats(self):
        initial_substat_count = random.randint(3, 4)
        available_substats = [s for s in SUBSTATS if s != self.main_stat]
        selected_substats = random.sample(available_substats, initial_substat_count)
        return {stat: 0 for stat in selected_substats}

    def calculate_main_stat_score(self):
        return MAIN_STAT_WEIGHTS.get(self.slot, {}).get(self.main_stat, 0)

    def calculate_substat_potential(self):
        current_score = sum(SUBSTAT_WEIGHTS.get(stat, 0) for stat in self.substats)
        remaining_rolls = 5
        max_potential_score = sum(
            SUBSTAT_WEIGHTS.get(stat, 0) * remaining_rolls
            for stat in self.substats
        )
        return current_score, max_potential_score

    def evaluate(self):
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
        print(f"Slot: {self.slot}, Main Stat: {self.main_stat}, Level: {self.level}")
        for substat, upgrade in self.substats.items():
            print(f"  {substat}: {'+' + str(upgrade) if upgrade > 0 else ''}")
        print()

        evaluation = self.evaluate()
        print("Evaluation:")
        print(f"  Main Stat Score: {evaluation['Main Stat Score']}")
        print(f"  Current Substat Score: {evaluation['Current Substat Score']}")
        print(f"  Potential Substat Score: {evaluation['Potential Substat Score']}")
        print(f"  Total Score: {evaluation['Total Score']}")