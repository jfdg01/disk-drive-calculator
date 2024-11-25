import unittest

def parse_sub_stat(stat_text):
    if not stat_text:
        return None

    parts = stat_text.strip().split()
    stat_data = {
        "name": None,
        "level": 0,
        "value": None
    }

    # Handle special stat names (CRIT Rate, CRIT DMG, Anomaly Proficiency)
    if parts[0] == "CRIT" or parts[0] == "Anomaly":
        stat_data["name"] = f"{parts[0]} {parts[1]}"
        remaining_parts = parts[2:]
    else:
        stat_data["name"] = parts[0]
        remaining_parts = parts[1:]

    # Process remaining parts for level and value
    for part in remaining_parts:
        if part.startswith("+"):
            # Extract level number
            stat_data["level"] = int(part.replace("+", ""))
        else:
            # Extract numeric value
            stat_data["value"] = float(part.replace("%", ""))

    return stat_data


class TestStatParser(unittest.TestCase):
    def test_def_with_level_and_percentage(self):
        result = parse_sub_stat("DEF +1 9.6%")
        self.assertEqual(result, {
            "name": "DEF",
            "level": 1,
            "value": 9.6
        })

    def test_hp_with_value_only(self):
        result = parse_sub_stat("HP 212")
        self.assertEqual(result, {
            "name": "HP",
            "level": 0,
            "value": 212
        })

    def test_crit_rate_with_percentage(self):
        result = parse_sub_stat("CRIT Rate 2.4%")
        self.assertEqual(result, {
            "name": "CRIT Rate",
            "level": 0,
            "value": 2.4
        })

    def test_crit_dmg_with_level_and_percentage(self):
        result = parse_sub_stat("CRIT DMG +3 21.3%")
        self.assertEqual(result, {
            "name": "CRIT DMG",
            "level": 3,
            "value": 21.3
        })

    def test_empty_input(self):
        result = parse_sub_stat("")
        self.assertIsNone(result)

    def test_none_input(self):
        result = parse_sub_stat(None)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)