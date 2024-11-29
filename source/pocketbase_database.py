import requests
from typing import List

class PocketBaseDatabase:
    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url
        self.auth_token = auth_token

    def _headers(self):
        """Generate headers for the requests."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def create_disk(self, disk_data: dict):
        """Create a new disk in PocketBase."""
        response = requests.post(f"{self.base_url}/collections/disks/records", json=disk_data, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_disks(self) -> List[dict]:
        """Retrieve all disks from PocketBase."""
        response = requests.get(f"{self.base_url}/collections/disks/records", headers=self._headers())
        response.raise_for_status()
        return response.json().get("items", [])

    def update_disk(self, disk_id: str, disk_data: dict):
        """Update a disk in PocketBase."""
        response = requests.patch(f"{self.base_url}/collections/disks/records/{disk_id}", json=disk_data, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def delete_disk(self, disk_id: str):
        """Delete a disk from PocketBase."""
        response = requests.delete(f"{self.base_url}/collections/disks/records/{disk_id}", headers=self._headers())
        response.raise_for_status()
        return response.status_code == 204