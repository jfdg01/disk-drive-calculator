import json
from dataclasses import dataclass, field
from typing import List, Dict, Any

from source.constants import SUBSTAT_WEIGHTS


@dataclass
class Stat:
    """Represents a single stat (main or substat)."""
    name: str
    value: float
    level: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert Stat object to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "level": self.level
        }


@dataclass
class Disk:
    """Represents a disk containing main and sub stats."""
    id: str
    main_stat: Stat
    sub_stats: List[Stat] = field(default_factory=list)

    def total_substat_score(self, weights: Dict[str, float]) -> float:
        """Calculate the total score based on substats and their weights."""
        return sum(weights.get(stat.name, 0) * stat.value for stat in self.sub_stats)

    def potential_score(self, weights: Dict[str, float], max_rolls: int = 5) -> float:
        """Estimate the potential score based on remaining rolls."""
        remaining_rolls = max_rolls - sum(stat.level for stat in self.sub_stats)
        return sum(weights.get(stat.name, 0) * (remaining_rolls / max_rolls) for stat in self.sub_stats)

    def to_dict(self) -> Dict[str, Any]:
        """Export disk data to a dictionary."""
        return {
            "id": self.id,
            "main_stat": self.main_stat.to_dict(),
            "sub_stats": [stat.to_dict() for stat in self.sub_stats]
        }

    def to_json(self) -> str:
        """Export disk data to a JSON string."""
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def __str__(self) -> str:
        """String representation of the disk."""
        sub_stats_str = "\n".join(
            f"  - {stat.name}: {stat.value} (Level {stat.level})" for stat in self.sub_stats
        )
        return (
            f"Disk ID: {self.id}\n"
            f"Main Stat: {self.main_stat.name} - {self.main_stat.value} (Level {self.main_stat.level})\n"
            f"Sub Stats:\n{sub_stats_str}"
        )

    # Comparator methods for sorting and ranking
    def __lt__(self, other: "Disk") -> bool:
        """Compare disks by total substat score."""
        return self.total_substat_score(SUBSTAT_WEIGHTS) < other.total_substat_score(SUBSTAT_WEIGHTS)

    def __eq__(self, other: "Disk") -> bool:
        """Check equality based on main and sub stats."""
        return self.to_dict() == other.to_dict()
