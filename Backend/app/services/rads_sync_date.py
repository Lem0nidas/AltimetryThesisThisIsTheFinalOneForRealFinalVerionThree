import os
import subprocess
from pathlib import Path
from dotenv import find_dotenv
from datetime import datetime, timedelta, timezone
from services.rads_sync_custom import get_custom_nc_file
from utils.phase_mapping import *


find_dotenv()

# TODO Make improvments
def get_date_nc_file(
        satellite: str, 
        start_date: str, 
        end_date: str, 
        ) -> None:

    if not satellite:
        raise ValueError("Satellite not specified")
    if not start_date:
        raise ValueError("Date not specified")

    cyc_path = Path(os.getenv("RADS_CYCLES", "/"))
    rads_dir = Path(os.getenv("RADSDATAROOT", "/"))
    user_start_date = parse_rads_datetime(start_date)
    user_end_date = parse_rads_datetime(end_date)
    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]
    downloaded = False

#TODO Maybe there is a better way to do this. Maybe not
    for phase_file in sat_phases:
        phase_code, first_cycle, last_cycle, cyc_first_date, cyc_last_date = read_first_last_cycle(f"{cyc_path}/{phase_file}")

        if (cyc_last_date < user_start_date) or (cyc_first_date > user_end_date):
            continue

        if user_start_date > cyc_first_date:
            start_cycle_num = find_cycle_num(f"{cyc_path}/{phase_file}", user_start_date)
        else:
            start_cycle_num = first_cycle

        if user_end_date < cyc_last_date:
            end_cycle_num = find_cycle_num(f"{cyc_path}/{phase_file}", user_end_date)
        else:
            end_cycle_num = last_cycle

        if (start_cycle_num.isdigit() and end_cycle_num.isdigit()):
            for each_cycle in range(int(start_cycle_num), int(end_cycle_num) + 1):
                try:
                    get_custom_nc_file(satellite, str(each_cycle).zfill(3))
                except Exception as e:
                    print(f"Cycle number {str(each_cycle).zfill(3)} was not found. \nException message: {e}")

                zip_name = f"{satellite}_c{str(each_cycle).zfill(3)}.zip"
                zip_dir = rads_dir / satellite
                try:
                    if not (zip_dir / zip_name).exists():
                        subprocess.run(
                            ['zip', '-r', str(zip_dir / zip_name), f'c{str(each_cycle).zfill(3)}'],
                            cwd=zip_dir / phase_code,
                            check=True
                        )
                except subprocess.CalledProcessError as e:
                    print(f"Failed to create zip {zip_name}: {e}")
                    
            downloaded = True

    if (not downloaded):
        print("No matching data found in the selected date range!")

    return None

def find_cycle_num(file_path: str, date: datetime) -> str:
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.split()
            cycle_start_date = parse_rads_datetime(parts[4])
            cycle_end_date = parse_rads_datetime(parts[5])

            if (cycle_start_date < date < cycle_end_date):
                return parts[1]

    return "Date out of range!"

def sec85_to_utc(sec: str) -> datetime:
    sec85 = float(sec)
    base = datetime(1985, 1, 1, tzinfo=timezone.utc)
    return base + timedelta(seconds=sec85)