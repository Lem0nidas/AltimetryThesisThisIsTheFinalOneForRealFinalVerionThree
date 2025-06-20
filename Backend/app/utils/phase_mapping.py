import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()


def locate_phase(satellite: str, cyc_num: str) -> str:
    cyc_path = Path(str(os.getenv("RADS_CYCLES")))
    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]
    for file in sat_phases:
        phase_code, first_cycle, last_cycle = read_first_last_cycle(f"{cyc_path}/{file}")
        if (int(first_cycle) < int(cyc_num)) and (int(last_cycle) > int(cyc_num)):
            return phase_code
        else:
            continue
    return "Couldn't find the requested cycle!"


def read_first_last_cycle(file_path) -> tuple[str, str, str]:
    with open(file_path, 'r') as f:
        first_line = f.readline().split()
        first_cycle = first_line[1]

    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Go to second-last byte (avoid EOF)
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move backward until a newline
        last_line = f.readline().decode().split()
        last_cycle = last_line[1]

    return first_line[0], first_cycle, last_cycle


def read_first_last_pass(file_path) -> tuple[datetime, datetime]:
    with open(file_path, 'r') as f:
        first = f.readline().split(" ")[4]

    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Go to second-last byte (avoid EOF)
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move backward until a newline
        last = f.readline().decode().split(" ")[5]

    return parse_rads_datetime(first), parse_rads_datetime(last)


def parse_rads_datetime(date_str: str) -> datetime:
    if len(date_str) >= 12 and date_str[:12].isdigit():
        date_str = date_str.split('.')[0]
        yy = int(date_str[:2])
        year = 1900 + yy if yy >= 80 else 2000 + yy
        dt = datetime.strptime(f"{year}{date_str[2:]}", "%Y%m%d%H%M%S")
        return dt.replace(tzinfo=timezone.utc)
    else:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)

