import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any

from source.constants import SUBSTAT_WEIGHTS, SUBSTATS


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


def disk_potential(level, substats, starting_substats=4):
    # Constants
    max_level = 15
    levels_per_upgrade = 3
    alpha = 0.15  # Exponential decay rate

    # Calculate current value of the substats
    current_value = sum(SUBSTAT_WEIGHTS[stat] * value for stat, value in substats.items())

    # Calculate remaining upgrades
    total_upgrades = max(0, (max_level - level) // levels_per_upgrade)
    meaningful_upgrades = total_upgrades - (1 if starting_substats == 3 else 0)

    # Average potential gain per upgrade
    average_gain = sum(SUBSTAT_WEIGHTS.values()) / len(SUBSTAT_WEIGHTS)

    # Expected value of the 4th substat (only applies for 3-starting substat disks)
    fourth_substat_value = 0
    if starting_substats == 3 and level < max_level:
        # Expectation: average weight multiplied by average base value
        average_weight = sum(SUBSTAT_WEIGHTS.values()) / len(SUBSTAT_WEIGHTS)
        average_base_value = sum(SUBSTATS.values()) / len(SUBSTATS)
        fourth_substat_value = average_weight * average_base_value

    # Potential from future upgrades
    future_potential = meaningful_upgrades * average_gain

    # Add the 4th substat value to potential if applicable
    if starting_substats == 3:
        future_potential += fourth_substat_value

    # Apply exponential decay for higher levels
    level_penalty = math.exp(-alpha * level)

    # Combine current value and future potential
    total_potential = (current_value + future_potential) * level_penalty

    return total_potential


@dataclass
class Disk:
    """Represents a disk containing main and sub stats."""
    id: str
    main_stat: Stat
    sub_stats: List[Stat] = field(default_factory=list)

    def total_substat_score(self, weights: Dict[str, float]) -> float:
        """Calculate the total score based on substats and their weights."""
        return sum(weights.get(stat.name, 0) * stat.value for stat in self.sub_stats)

    # Inside the Disk class
    def calculate_potential(self, weights: Dict[str, float]) -> float:
        """
        Calculate the potential of the disk using the `disk_potential` function.
        :param weights: Dictionary of substat weights.
        :return: Disk potential score.
        """
        level = self.main_stat.level
        substats = {stat.name: stat.value for stat in self.sub_stats}
        starting_substats = len(self.sub_stats)

        # Pass the required arguments to the disk_potential function
        return disk_potential(level, substats, starting_substats)

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
