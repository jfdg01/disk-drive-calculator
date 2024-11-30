import json
import os
from disk import Stat, Disk
from pocketbase_database import PocketBaseDatabase
from constants import DATABASE_URL


def batch_upload_all_disks(disks, number_of_disks, database):
    for i in range(0, len(disks), number_of_disks):
        batch = disks[i:i + number_of_disks]

        # Step 1: Create disks and get their IDs
        created_disks = database.create_disks_and_get_ids(batch)

        # Step 2: Create sub-stats using the retrieved IDs
        database.create_sub_stats_batch(created_disks)

        print(f"Uploaded batch {i // number_of_disks + 1} successfully.")


def batch_upload_fist_n_disks(disks, number_of_disks, database):
    batch = disks[:number_of_disks]

    # Step 1: Create disks and get their IDs
    created_disks = database.create_disks_and_get_ids(batch)

    # Step 2: Create sub-stats using the retrieved IDs
    database.create_sub_stats_batch(created_disks)

    print(f"Uploaded batch of size {number_of_disks} successfully.")


def convert_json_to_db(json_file, batch_size, database):
    """Migrate data from JSON to SQLite database."""
    if not os.path.exists(json_file):
        print(f"File {json_file} does not exist.")
        return

    with open(json_file, "r") as file:
        raw_disks = json.load(file)

    disks = []

    for disk_id, disk_data in raw_disks.items():
        main_stat_data = disk_data.get("main_stat")
        if not main_stat_data:
            # print(f"Disk {disk_id} is missing 'main_stat' data. Using default value.")
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

            # Add the disk to the list for batch upload
            disks.append(disk.to_dict())
        except KeyError as e:
            print(f"Missing key {e} in 'main_stat' or 'sub_stats' for disk {disk_id}. Skipping this entry.")

    # Batch upload the disks
    batch_upload_fist_n_disks(disks, 5, database)
    # batch_upload_all_disks(disks, batch_size, database)

    print("Migration complete!")


if __name__ == "__main__":
    db = PocketBaseDatabase(DATABASE_URL)
    convert_json_to_db("../output/disk_data.json", 3000, db)
