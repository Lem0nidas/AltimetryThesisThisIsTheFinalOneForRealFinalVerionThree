import subprocess
import os
import re
from pathlib import Path
from dotenv import find_dotenv
from datetime import datetime as dt

find_dotenv()

# TODO Make improvments
# TODO NOT COMPLETED
def get_date_nc_file(satellite: str, date: str, save_dir: Path = Path("./rads_data")) -> None:

    if not satellite:
        raise ValueError("Satellite not specified")

    if not date:
        raise ValueError("Date not specified")

    remote_base = (os.getenv("RADS_REMOTE_BASE"))
    tables = os.getenv("RADS_TABLES")
    cyc_path = Path(str(f"{tables}/cycles/"))
    pass_path = Path(str(f"{tables}/passes/"))
    save_dir.mkdir(parents=True, exist_ok=True)
    cycle_num, pass_num = str, str
    user_date = parse_rads_datetime(date)


    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]

    for file in sat_phases:
        cyc_first_date, cyc_last_date = read_first_last_line(f"{tables}/cycles/{file}")
        # print(cyc_first_date, cyc_last_date)
        print(cyc_first_date, user_date, cyc_last_date)
        if (cyc_first_date < user_date) & (cyc_last_date > user_date):
            print(f"Dates found in file: {file}")
            return None
        else:
            print("Dates were not found")
        
    return None


def parse_rads_datetime(date_str: str) -> dt:
    if len(date_str) >= 12 and date_str[:12].isdigit():
        date_str = date_str.split('.')[0]
        yy = int(date_str[:2])
        year = 1900 + yy if yy >= 80 else 2000 + yy
        return dt.strptime(f"{year}{date_str[2:]}", "%Y%m%d%H%M%S")
    else:
        return dt.strptime(date_str, "%Y-%m-%d")


def read_first_last_line(file_path) -> tuple[dt, dt]:
    with open(file_path, 'r') as f:
        first = f.readline().split(" ")[4]


    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Go to second-last byte (avoid EOF)
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move backward until a newline
        last = f.readline().decode().split(" ")[5]

    return parse_rads_datetime(first), parse_rads_datetime(last)
