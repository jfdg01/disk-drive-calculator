from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from disk_manager import DiskManager
from pocketbase_database import PocketBaseDatabase
from fastapi.middleware.cors import CORSMiddleware
import logging

from constants import DATABASE_URL

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's URL for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and DiskManager
disk_manager = DiskManager(PocketBaseDatabase(DATABASE_URL))

# Pydantic models for request and response validation
class StatModel(BaseModel):
    name: str
    value: float
    level: int


class DiskModel(BaseModel):
    id: str = None  # Optional for creation
    main_stat: StatModel
    sub_stats: List[StatModel]


# Routes
@app.post("/disks/", response_model=dict)
def add_disk(disk: DiskModel):
    try:
        # Prepare the data for DiskManager
        disk_data = {
            "main_stat": {
                "name": disk.main_stat.name,
                "value": disk.main_stat.value,
                "level": disk.main_stat.level
            },
            "sub_stats": [
                {"name": stat.name, "value": stat.value, "level": stat.level}
                for stat in disk.sub_stats
            ]
        }
        disk_manager.add_disk(disk_data)
        return {"message": "Disk added successfully"}
    except Exception as e:
        logging.error(f"Error adding disk: {e}")
        raise HTTPException(status_code=500, detail="Failed to add disk")


@app.get("/disks/", response_model=List[DiskModel])
def get_disks():
    try:
        disks = disk_manager.get_disks()
        return disks
    except Exception as e:
        logging.error(f"Error retrieving disks: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve disks")


@app.delete("/disks/{disk_id}", response_model=dict)
def remove_disk(disk_id: str):
    try:
        disk_manager.remove_disk(disk_id)
        return {"message": "Disk removed successfully"}
    except Exception as e:
        logging.error(f"Error removing disk with id {disk_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove disk")


@app.put("/disks/{disk_id}", response_model=dict)
def update_disk(disk_id: str, disk: DiskModel):
    try:
        # Prepare the data for DiskManager
        disk_data = {
            "id": disk_id,
            "main_stat": {
                "name": disk.main_stat.name,
                "value": disk.main_stat.value,
                "level": disk.main_stat.level
            },
            "sub_stats": [
                {"name": stat.name, "value": stat.value, "level": stat.level}
                for stat in disk.sub_stats
            ]
        }
        disk_manager.update_disk(disk_data)
        return {"message": "Disk updated successfully"}
    except Exception as e:
        logging.error(f"Error updating disk with id {disk_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update disk")
