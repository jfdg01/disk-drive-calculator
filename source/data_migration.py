import json
import os

from source.disk import Stat, Disk
from source.disk_database import DiskDatabase
from source.disk_manager import DiskManager


def migrate_json_to_db(json_file, database: DiskDatabase):
    """Migrate data from JSON to SQLite database."""
    if not os.path.exists(json_file):
        print(f"File {json_file} does not exist.")
        return

    with open(json_file, "r") as file:
        raw_disks = json.load(file)

    disk_manager = DiskManager(database)
    for disk_id, disk_data in raw_disks.items():
        main_stat_data = disk_data.get("main_stat")
        if not main_stat_data:
            print(f"Disk {disk_id} is missing 'main_stat' data. Using default value.")
            main_stat = Stat(
                name="HP",
                value=550.0,
                level=1
            )
        else:
            main_stat = Stat(
                name=main_stat_data["name"],
                value=main_stat_data["value"],
                level=main_stat_data["level"]
            )

        try:
            sub_stats = [Stat(**sub_stat) for sub_stat in disk_data.get("sub_stats", [])]
            disk = Disk(id=disk_id, main_stat=main_stat, sub_stats=sub_stats)

            disk_manager.add_disk(disk)
        except KeyError as e:
            print(f"Missing key {e} in 'main_stat' or 'sub_stats' for disk {disk_id}. Skipping this entry.")

    print("Migration complete!")

def main():
    json_file = "../output/disk_data.json"
    database_file = "../output/disk_database.db"

    # Initialize the database connection
    database = DiskDatabase(database_file)

    # Perform the migration
    migrate_json_to_db(json_file, database)

    # Close the database connection
    database.close()


if __name__ == "__main__":
    main()
