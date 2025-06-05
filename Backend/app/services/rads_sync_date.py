import subprocess
import os
import re
from pathlib import Path
from dotenv import find_dotenv
from datetime import datetime as dt

find_dotenv()

# TODO Make improvments
# TODO NOT COMPLETED
def get_date_nc_file(satellite: str, date: str, save_dir: Path = Path("./rads_data")) -> bool:
    remote_base = (os.getenv("RADS_REMOTE_BASE"))
    tables = os.getenv("RADS_TABLES")
    cyc_path = Path(str(f"{tables}/cycles/"))
    pass_path = Path(str(f"{tables}/passes/"))
    save_dir.mkdir(parents=True, exist_ok=True)
    cycle_num, pass_num = str, str
    
    if not satellite:
        raise ValueError("Satellite not specified")

    if not date:
        raise ValueError("Date not specified")

    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]
    rads_cyc_date_format = dt.strptime(date, "%Y-%m-%d").strftime("%y%m%d%H%M%S")
    # print(rads_cyc_date_format)
    # print(type(rads_cyc_date_format))
    print(sat_phases)
    print(cyc_path)

    for file in sat_phases:
        cyc_first_date, cyc_last_date = read_first_last_line(f"{tables}/cycles/{file}")
        print(cyc_first_date, cyc_last_date)
        # print(cyc_first_date, cyc_last_date, rads_cyc_date_format)
        if (int(float(cyc_first_date)) < int(rads_cyc_date_format)) & (int(float(cyc_last_date)) > int(rads_cyc_date_format)):
            print(f"Dates found in file: {file}")
            return True
        else:
            print("Dates were not found")
        
    return True


def read_first_last_line(file_path):
    with open(file_path, 'r') as f:
        first = f.readline().split(" ")[4]


    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Go to second-last byte (avoid EOF)
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move backward until a newline
        last = f.readline().decode().split(" ")[5]

    return first, last
