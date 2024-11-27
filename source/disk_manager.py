import os
from operator import itemgetter
from typing import List

from constants import SUBSTAT_WEIGHTS
from source.disk import Disk, Stat
from source.disk_database import DiskDatabase


class DiskManager:

    def __init__(self, database: DiskDatabase):
        self.database = database

    def add_disk(self, disk: Disk):
        """Add a new disk to the database."""
        with self.database.connection as conn:
            # Insert into disks table without specifying an ID
            cursor = conn.execute("""
                INSERT INTO disks (main_stat_name, main_stat_value, main_stat_level)
                VALUES (?, ?, ?)
            """, (disk.main_stat.name, disk.main_stat.value, disk.main_stat.level))

            # Retrieve the auto-generated ID for the disk
            disk_id = cursor.lastrowid

            # Insert sub_stats linked to the new disk
            for sub_stat in disk.sub_stats:
                conn.execute("""
                    INSERT INTO sub_stats (disk_id, name, value, level)
                    VALUES (?, ?, ?, ?)
                """, (disk_id, sub_stat.name, sub_stat.value, sub_stat.level))

    def get_disks(self) -> List[Disk]:
        """Retrieve all disks from the database."""
        disks = []
        with self.database.connection as conn:
            cursor = conn.execute("SELECT id, main_stat_name, main_stat_value, main_stat_level FROM disks")
            for row in cursor.fetchall():
                disk_id, main_name, main_value, main_level = row
                main_stat = Stat(name=main_name, value=main_value, level=main_level)

                sub_cursor = conn.execute("SELECT name, value, level FROM sub_stats WHERE disk_id = ?", (disk_id,))
                sub_stats = [Stat(name=sub_row[0], value=sub_row[1], level=sub_row[2]) for sub_row in sub_cursor]

                disks.append(
                    Disk(id=str(disk_id), main_stat=main_stat, sub_stats=sub_stats))  # Cast ID to str if needed
        return disks

    def remove_disk(self, disk_id: str):
        """Remove a disk and its sub-stats from the database."""
        with self.database.connection as conn:
            conn.execute("DELETE FROM sub_stats WHERE disk_id = ?", (disk_id,))
            conn.execute("DELETE FROM disks WHERE id = ?", (disk_id,))

    def update_disk(self, disk: Disk):
        """Update an existing disk."""
        with self.database.connection as conn:
            conn.execute("""
                UPDATE disks SET main_stat_name = ?, main_stat_value = ?, main_stat_level = ?
                WHERE id = ?
            """, (disk.main_stat.name, disk.main_stat.value, disk.main_stat.level, disk.id))

            # Delete and re-insert sub_stats to simplify updates
            conn.execute("DELETE FROM sub_stats WHERE disk_id = ?", (disk.id,))
            for sub_stat in disk.sub_stats:
                conn.execute("""
                    INSERT INTO sub_stats (disk_id, name, value, level)
                    VALUES (?, ?, ?, ?)
                """, (disk.id, sub_stat.name, sub_stat.value, sub_stat.level))

    def disk_exists(self, disk: Disk) -> bool:
        """Check if a disk with the same stats (main + ordered sub-stats) already exists in the database."""
        with self.database.connection as conn:
            # Step 1: Retrieve all disk IDs with matching main stats
            cursor = conn.execute("""
                SELECT id FROM disks
                WHERE main_stat_name = ? 
                AND ABS(main_stat_value - ?) < 0.0001
                AND main_stat_level = ?
            """, (disk.main_stat.name, disk.main_stat.value, disk.main_stat.level))

            matching_main_stat_ids = [row[0] for row in cursor.fetchall()]
            if not matching_main_stat_ids:
                return False  # No disks with matching main stats

            # Step 2: Check sub-stats for each matching disk ID
            for disk_id in matching_main_stat_ids:
                # Retrieve sub-stats for this disk ID, ordered by insertion (ID)
                db_sub_stats = conn.execute("""
                    SELECT name, value, level 
                    FROM sub_stats
                    WHERE disk_id = ?
                    ORDER BY id ASC
                """, (disk_id,)).fetchall()

                # Convert database sub-stats to a list of Stat objects
                db_sub_stats = [
                    Stat(name=row[0], value=row[1], level=row[2])
                    for row in db_sub_stats
                ]

                # Step 3: Compare sub-stats (length, order, and values)
                if len(db_sub_stats) != len(disk.sub_stats):
                    continue  # Skip this disk ID; sub-stat count doesn't match

                match = all(
                    db_stat.name == disk_stat.name and
                    abs(db_stat.value - disk_stat.value) < 0.0001 and
                    db_stat.level == disk_stat.level
                    for db_stat, disk_stat in zip(db_sub_stats, disk.sub_stats)
                )

                if match:
                    return True  # Found a matching disk

            # No matching disk found
            return False

    def evaluate_disk(self, disk: Disk) -> dict:
        """
        Evaluate a single disk using its methods.
        :param disk: A Disk object.
        :return: Evaluation scores and total score as a dictionary.
        """
        # Fixed main stat score
        main_stat_score = 0 if disk.main_stat.level >= 15 else 10  # Example score for non-maxed main stat

        # Calculate scores using Disk methods
        current_score = disk.total_substat_score(SUBSTAT_WEIGHTS)
        potential_score = disk.potential_score(SUBSTAT_WEIGHTS)

        # Total score combines main stat and substat scores
        total_score = main_stat_score + current_score + potential_score

        return {
            "Disk ID": disk.id,
            "Main Stat Score": main_stat_score,
            "Current Substat Score": current_score,
            "Potential Substat Score": potential_score,
            "Total Score": total_score,
        }

    def rank_disks(self) -> List[dict]:
        """
        Rank all disks based on their total scores.
        :return: Sorted list of disk evaluations.
        """
        disks = self.get_disks()  # Fetch disks from the database
        evaluations = [self.evaluate_disk(disk) for disk in disks]
        # Sort by total score in descending order
        return sorted(evaluations, key=itemgetter("Total Score"), reverse=True)

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


# Example usage with database
if __name__ == "__main__":
    # Initialize DiskDatabase (assumes implementation exists)
    db = DiskDatabase("../db/disk_database.db")
    disk_manager = DiskManager(db)

    # Example: Add, rank, and display disks
    ranked_disks = disk_manager.rank_disks()
    disk_manager.display_ranking(ranked_disks)
