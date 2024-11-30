import json

import requests
from typing import List, Dict, Optional


class PocketBaseDatabase:
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        self.base_url = base_url
        self.auth_token = auth_token

    def create_disks_and_get_ids(self, disks: List[dict]) -> List[dict]:

        # Construct batch requests
        batch_requests = [
            {
                "method": "POST",
                "url": "/api/collections/disks/records?fields=id",
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "main_stat_name": disk["main_stat"]["name"],
                    "main_stat_value": disk["main_stat"]["value"],
                    "main_stat_level": disk["main_stat"]["level"],
                }
            }
            for disk in disks
        ]

        # Prepare payload
        payload = {"requests": batch_requests}

        # Log payload for debugging
        # print("Payload being sent:", json.dumps(payload, indent=4))

        # Make the POST request
        response = requests.post(
            f"{self.base_url}/batch",
            json=payload,
            headers=self._headers(),
        )

        # Log response
        if not response.ok:
            print("Response status code:", response.status_code)
            print("Error response body:", response.text)

        # Raise error for bad status codes
        response.raise_for_status()

        # Parse and get the ids
        ids = [item['body']['id'] for item in response.json()]

        # Match the ids to the substats of each disk
        for disk, disk_id in zip(disks, ids):
            for sub_stat in disk["sub_stats"]:
                sub_stat["disk_id"] = disk_id

        return disks

    def get_disks_and_substats(self) -> List[dict]:

        batch_requests = [
            {
                "method": "GET",
                "url": "/api/collections/disks/records",
                "headers": {"Content-Type": "application/json"},
                "body": {}
            },
            {
                "method": "GET",
                "url": "/api/collections/sub_stats/records",
                "headers": {"Content-Type": "application/json"},
                "body": {}
            }

        ]

        payload = {"requests": batch_requests}

        # Log payload for debugging
        print("Payload being sent:", json.dumps(payload, indent=4))

        response = requests.post(
            f"{self.base_url}/batch",
            json=payload,
            headers=self._headers(),
        )

        # Log response
        if not response.ok:
            print("Response status code:", response.status_code)
            print("Error response body:", response.text)

        # Raise error for bad status codes
        response.raise_for_status()

        disks = None
        sub_stats = None

        # Group sub_stats by disk_id for easier lookup
        sub_stats_by_disk = {}
        for sub_stat in sub_stats:
            disk_id = sub_stat["disk_id"]
            if disk_id not in sub_stats_by_disk:
                sub_stats_by_disk[disk_id] = []
            sub_stats_by_disk[disk_id].append(sub_stat)

        # Build the result structure
        result = []
        for disk in disks:
            disk_id = disk["id"]
            result.append({
                "id": disk_id,
                "main_stat": {
                    "name": disk["main_stat_name"],
                    "value": disk["main_stat_value"],
                    "level": disk["main_stat_level"]
                },
                "sub_stats": [
                    {
                        "name": sub_stat["name"],
                        "value": sub_stat["value"],
                        "level": sub_stat["level"]
                    }
                    for sub_stat in sub_stats_by_disk.get(disk_id, [])
                ]
            })

        return result

    def create_sub_stats_batch(self, disks_with_ids: List[dict]) -> dict:
        # Construct batch requests
        batch_requests = [
            {
                "method": "POST",
                "url": "/api/collections/sub_stats/records",  # Relative URL
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "disk_id": sub_stat["disk_id"],  # Use the disk_id from the sub_stat
                    "name": sub_stat["name"],
                    "value": sub_stat["value"],
                    "level": sub_stat["level"],
                },
            }
            for disk in disks_with_ids
            for sub_stat in disk["sub_stats"]  # Iterate over sub_stats in each disk
        ]

        # Prepare payload
        payload = {"requests": batch_requests}

        # Log payload for debugging
        # print("Payload being sent for sub_stats:", json.dumps(payload, indent=4))

        # Make the POST request
        response = requests.post(
            f"{self.base_url}/batch",
            json=payload,
            headers=self._headers(),
        )

        # Log response
        if not response.ok:
            print("Response status code:", response.status_code)
            print("Error response body:", response.text)

        # Raise error for bad status codes
        response.raise_for_status()

        # Return parsed response
        return response.json()

    def _headers(self) -> Dict[str, str]:
        """Generate headers for the requests."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    # Disk methods
    def create_disk(self, disk_data: dict) -> dict:
        response = requests.post(
            f"{self.base_url}/collections/disks/records",
            json=disk_data,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_substats(self) -> List[dict]:
        response = requests.get(
            f"{self.base_url}/collections/sub_stats/records",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get("items", [])

    def get_disks(self) -> List[dict]:
        response = requests.get(
            f"{self.base_url}/collections/disks/records",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get("items", [])

    def update_disk(self, disk_id: str, disk_data: dict) -> dict:
        response = requests.patch(
            f"{self.base_url}/collections/disks/records/{disk_id}",
            json=disk_data,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def delete_disk(self, disk_id: str) -> bool:
        response = requests.delete(
            f"{self.base_url}/collections/disks/records/{disk_id}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.status_code == 204

    # Sub-Stat methods
    def create_sub_stat(self, sub_stat_data: dict) -> dict:
        response = requests.post(
            f"{self.base_url}/collections/sub_stats/records",
            json=sub_stat_data,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_sub_stats_by_disk(self, disk_id: str) -> List[dict]:
        response = requests.get(
            f"{self.base_url}/collections/sub_stats/records?filter=disk_id='{disk_id}'",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get("items", [])

    def delete_sub_stats_by_disk(self, disk_id: str) -> bool:
        """Delete all sub-stats for a given disk."""
        sub_stats = self.get_sub_stats_by_disk(disk_id)
        for sub_stat in sub_stats:
            self.delete_sub_stat(sub_stat["id"])
        return True

    def delete_sub_stat(self, sub_stat_id: str) -> bool:
        response = requests.delete(
            f"{self.base_url}/collections/sub_stats/records/{sub_stat_id}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.status_code == 204
