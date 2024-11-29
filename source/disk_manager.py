from typing import List

from pocketbase_database import PocketBaseDatabase


class DiskManager:
    def __init__(self, database: PocketBaseDatabase):
        self.database = database

    def add_disk(self, disk: dict):
        # Create the disk
        created_disk = self.database.create_disk({
            "main_stat_name": disk["main_stat"]["name"],
            "main_stat_value": disk["main_stat"]["value"],
            "main_stat_level": disk["main_stat"]["level"]
        })

        # Add sub-stats
        for sub_stat in disk["sub_stats"]:
            self.database.create_sub_stat({
                "disk_id": created_disk["id"],
                "name": sub_stat["name"],
                "value": sub_stat["value"],
                "level": sub_stat["level"]
            })

    def get_disks(self) -> List[dict]:
        disks = self.database.get_disks()
        return disks

    def remove_disk(self, disk_id: str):
        # Delete sub-stats and the disk
        self.database.delete_sub_stats_by_disk(disk_id)
        self.database.delete_disk(disk_id)

    def update_disk(self, disk: dict):
        # Update the disk
        self.database.update_disk(disk["id"], {
            "main_stat_name": disk["main_stat"]["name"],
            "main_stat_level": disk["main_stat"]["value"]
        })

        # Delete existing sub-stats and add new ones
        self.database.delete_sub_stats_by_disk(disk["id"])
        for sub_stat in disk["sub_stats"]:
            self.database.create_sub_stat({
                "disk_id": disk["id"],
                "name": sub_stat["name"],
                "value": sub_stat["value"],
                "level": sub_stat["level"]
            })