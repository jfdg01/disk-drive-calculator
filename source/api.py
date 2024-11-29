from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from disk import Disk, Stat
from disk_manager import DiskManager
from pocketbase_database import PocketBaseDatabase
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and disk manager
pocketbase_db = PocketBaseDatabase(base_url="http://localhost:8090/api")
disk_manager = DiskManager(pocketbase_db)


# Pydantic models for request and response validation
class StatModel(BaseModel):
    name: str
    value: float
    level: int


class DiskModel(BaseModel):
    id: str
    main_stat: StatModel
    sub_stats: List[StatModel]


@app.get("/disks", response_model=List[DiskModel])
def get_disks():
    disks = disk_manager.get_disks()
    return [
        DiskModel(
            id=str(disk.id),  # Ensure id is a string
            main_stat=StatModel(
                name=disk.main_stat.name,
                value=disk.main_stat.value,
                level=disk.main_stat.level
            ),
            sub_stats=[
                StatModel(
                    name=stat.name,
                    value=stat.value,
                    level=stat.level
                ) for stat in disk.sub_stats
            ]
        )
        for disk in disks
    ]


@app.post("/disks", response_model=DiskModel)
def create_disk(disk: DiskModel):
    if disk_manager.disk_exists(Disk(
            id=disk.id,
            main_stat=Stat(**disk.main_stat.model_dump()),
            sub_stats=[Stat(**stat.model_dump()) for stat in disk.sub_stats]
    )):
        raise HTTPException(status_code=400, detail="Disk already exists.")
    new_disk = Disk(
        id=disk.id,
        main_stat=Stat(**disk.main_stat.model_dump()),
        sub_stats=[Stat(**stat.model_dump()) for stat in disk.sub_stats]
    )
    disk_manager.add_disk(new_disk)
    return disk


@app.put("/disks/{disk_id}", response_model=DiskModel)
def update_disk(disk_id: str, disk: DiskModel):
    updated_disk = Disk(
        id=disk_id,
        main_stat=Stat(**disk.main_stat.model_dump()),
        sub_stats=[Stat(**stat.model_dump()) for stat in disk.sub_stats]
    )
    disk_manager.update_disk(updated_disk)
    return disk


@app.delete("/disks/{disk_id}")
def delete_disk(disk_id: str):
    disk_manager.remove_disk(disk_id)
    return {"message": "Disk deleted successfully."}

@app.post("/disks/batch")
def create_disks_batch(disks: List[DiskModel]):
    for disk in disks:
        new_disk = Disk(
            id=disk.id,
            main_stat=Stat(**disk.main_stat.model_dump()),
            sub_stats=[Stat(**stat.model_dump()) for stat in disk.sub_stats]
        )
        disk_manager.add_disk(new_disk.to_dict())
    return {"message": f"Successfully added {len(disks)} disks."}
