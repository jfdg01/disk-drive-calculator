from typing import List

from disk import Disk, Stat
from pocketbase_database import PocketBaseDatabase


class DiskManager:
    def __init__(self, database: PocketBaseDatabase):
        self.database = database

    def add_disk(self, disk: Disk):
        """Add a new disk to the database."""
        disk_data = {
            "main_stat": disk.main_stat.to_dict(),
            "sub_stats": [sub_stat.to_dict() for sub_stat in disk.sub_stats]
        }
        created_disk = self.database.create_disk(disk_data)
        disk.id = created_disk["id"]  # Update the disk ID with the one assigned by PocketBase

    def get_disks(self) -> List[Disk]:
        """Retrieve all disks from the database."""
        disks_data = self.database.get_disks()
        result = []
        for disk_data in disks_data:
            main_stat = Stat(**disk_data["main_stat"])
            sub_stats = [Stat(**sub_stat) for sub_stat in disk_data["sub_stats"]]
            disk = Disk(id=disk_data["id"], main_stat=main_stat, sub_stats=sub_stats)
            result.append(disk)
        return result

    def remove_disk(self, disk_id: str):
        """Remove a disk and its sub-stats from the database."""
        self.database.delete_disk(disk_id)

    def update_disk(self, disk: Disk):
        """Update an existing disk."""
        disk_data = {
            "main_stat": disk.main_stat.to_dict(),
            "sub_stats": [sub_stat.to_dict() for sub_stat in disk.sub_stats]
        }
        self.database.update_disk(disk.id, disk_data)

    def disk_exists(self, disk: Disk) -> bool:
        """Check if a disk with the same stats exists in the database."""
        disks = self.get_disks()
        for existing_disk in disks:
            if existing_disk.main_stat == disk.main_stat and existing_disk.sub_stats == disk.sub_stats:
                return True
        return False
