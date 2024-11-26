import json
import os
from operator import itemgetter

from constants import SUBSTAT_WEIGHTS


class DiskManager:
    def __init__(self, disk_data_file):
        """
        Initialize the DiskManager instance.
        :param disk_data_file: Path to the JSON file containing disk data.
        """
        self.disk_data_file = disk_data_file
        self.disks = {}

    def load_disks(self):
        """
        Load disk data from the JSON file.
        """
        if not os.path.exists(self.disk_data_file):
            raise FileNotFoundError(f"Disk data file '{self.disk_data_file}' not found.")

        with open(self.disk_data_file, "r") as file:
            self.disks = json.load(file)
        print(f"Loaded {len(self.disks)} disks from {self.disk_data_file}.")

    def evaluate_disk(self, disk_id, disk_data):
        """
        Evaluate a single disk based solely on substats.
        Assumes every main stat contributes a fixed score of 10.
        :param disk_id: Identifier for the disk.
        :param disk_data: Data dictionary for the disk.
        :return: Evaluation scores and total score.
        """
        # Fixed main stat score
        main_stat_score = 0

        # Validate and calculate substats
        sub_stats = disk_data.get("sub_stats", [])
        if not isinstance(sub_stats, list) or not all(isinstance(stat, dict) for stat in sub_stats):
            raise ValueError(f"Invalid sub stats for disk ID {disk_id}: {sub_stats}")

        # Calculate current and potential scores
        current_score = sum(SUBSTAT_WEIGHTS.get(stat.get("name"), 0) for stat in sub_stats)
        remaining_rolls = 5  # Assume max rolls
        potential_score = sum(
            SUBSTAT_WEIGHTS.get(stat.get("name"), 0) * (remaining_rolls / 5)
            for stat in sub_stats
        )

        # If main_stat_level is 15 put score at 0
        main_stat = disk_data.get("main_stat") or {}
        if main_stat.get("level") == 15:
            main_stat_score = 0
            current_score = 0
            potential_score = 0

        # Total score combines main stat and substat scores
        total_score = main_stat_score + current_score + potential_score

        return {
            "Disk ID": disk_id,
            "Main Stat Score": main_stat_score,
            "Current Substat Score": current_score,
            "Potential Substat Score": potential_score,
            "Total Score": total_score,
        }

    def rank_disks(self):
        """
        Rank all disks based on their total scores.
        :return: Sorted list of disk evaluations.
        """
        evaluations = []
        for disk_id, disk_data in self.disks.items():
            evaluation = self.evaluate_disk(disk_id, disk_data)
            evaluations.append(evaluation)

        # Sort by total score in descending order
        ranked_disks = sorted(evaluations, key=itemgetter("Total Score"), reverse=True)
        return ranked_disks

    def display_ranking(self, ranked_disks):
        """
        Display the ranked disks in a readable format.
        :param ranked_disks: List of ranked disks.
        """
        print(
            f"{'Rank':<5} {'Disk ID':<10} {'Main Score':<12} {'Current Score':<15} {'Potential Score':<18} {'Total Score':<12}")
        print("=" * 75)
        for rank, disk in enumerate(ranked_disks, start=1):
            print(
                f"{rank:<5} {disk['Disk ID']:<10} {disk['Main Stat Score']:<12.2f} {disk['Current Substat Score']:<15.2f} {disk['Potential Substat Score']:<18.2f} {disk['Total Score']:<12.2f}")


# run the program
if __name__ == "__main__":
    # Example usage
    disk_file = "../output/disk_data.json"
    disk_manager = DiskManager(disk_file)

    # Load, rank, and display disks
    disk_manager.load_disks()
    ranked_disks = disk_manager.rank_disks()
    disk_manager.display_ranking(ranked_disks)
