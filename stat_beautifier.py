def parse_stat_value(stat_text):
    """
    Parse a stat value, handling both percentage and flat values.
    Returns a tuple of (value, is_percentage)
    """
    stat_text = stat_text.strip()
    if '%' in stat_text:
        try:
            return float(stat_text.replace('%', '')), True
        except ValueError:
            return 0, False
    try:
        return float(stat_text), False
    except ValueError:
        return 0, False


def format_stat_value(value, is_percentage):
    """
    Format a stat value for display
    """
    if is_percentage:
        return f"{value}%"
    return str(value)


def process_stat_line(line):
    """
    Process a single stat line, separating the stat type and value.
    Returns a tuple of (stat_type, value, is_percentage)
    """
    line = line.strip()
    if not line:
        return None, 0, False

    # Handle cases where the value might be on a separate line
    if line.endswith('%'):
        try:
            value = float(line.replace('%', ''))
            return None, value, True
        except ValueError:
            pass
    elif line.replace('.', '').isdigit():
        try:
            value = float(line)
            return None, value, False
        except ValueError:
            pass

    # Try to find "+N" suffix and remove it from the line
    plus_n_suffix = ""
    parts = line.split()
    if parts and parts[-1].startswith('+') and parts[-1][1:].isdigit():
        plus_n_suffix = parts[-1]
        line = ' '.join(parts[:-1])

    # Check if the line ends with a number or percentage
    if '%' in line:
        try:
            value_start = line.rindex(' ')
            value_text = line[value_start:].strip()
            stat_type = line[:value_start].strip()
            value = float(value_text.replace('%', ''))
            if plus_n_suffix:
                stat_type = f"{stat_type} {plus_n_suffix}"
            return stat_type, value, True
        except (ValueError, IndexError):
            return line + (" " + plus_n_suffix if plus_n_suffix else ""), 0, False
    else:
        try:
            value_start = line.rindex(' ')
            value_text = line[value_start:].strip()
            stat_type = line[:value_start].strip()
            value = float(value_text)
            if plus_n_suffix:
                stat_type = f"{stat_type} {plus_n_suffix}"
            return stat_type, value, False
        except (ValueError, IndexError):
            return line + (" " + plus_n_suffix if plus_n_suffix else ""), 0, False


def beautify_stats(text):
    """
    Process the OCR extracted text and return a structured dictionary of stats.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    stats = {
        'main_stat': None,
        'sub_stats': []
    }

    # Process the first line as main stat
    if lines:
        stat_type, value, is_percentage = process_stat_line(lines[0])
        if stat_type and value:
            stats['main_stat'] = {
                'type': stat_type,
                'value': value,
                'is_percentage': is_percentage
            }

    # Process remaining lines as sub stats
    current_stat = None
    for line in lines[1:]:
        stat_type, value, is_percentage = process_stat_line(line)

        # If we got a stat type without value
        if stat_type and value == 0:
            current_stat = stat_type
            continue

        # If we got a value without type, and we have a current_stat
        if not stat_type and value != 0 and current_stat:
            stats['sub_stats'].append({
                'type': current_stat,
                'value': value,
                'is_percentage': is_percentage
            })
            current_stat = None
            continue

        # If we got both type and value
        if stat_type and value != 0:
            stats['sub_stats'].append({
                'type': stat_type,
                'value': value,
                'is_percentage': is_percentage
            })
            current_stat = None

    return stats


def display_beautified_stats(stats):
    """
    Display the beautified stats in a clean format
    """
    if stats['main_stat']:
        print(f"Main Stat: {stats['main_stat']['type']} - "
              f"{format_stat_value(stats['main_stat']['value'], stats['main_stat']['is_percentage'])}")

    if stats['sub_stats']:
        print("\nSub Stats:")
        for stat in stats['sub_stats']:
            print(f"  {stat['type']}: "
                  f"{format_stat_value(stat['value'], stat['is_percentage'])}")
    print()