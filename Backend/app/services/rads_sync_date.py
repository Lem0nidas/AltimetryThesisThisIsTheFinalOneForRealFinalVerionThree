import os
import subprocess
from pathlib import Path
from dotenv import find_dotenv
from datetime import datetime, timedelta, timezone
from services.rads_sync_custom import get_custom_nc_file
from utils.phase_mapping import parse_rads_datetime, read_first_last_pass


find_dotenv()

# TODO Make improvments
# FIXME Somethings are not working properly. Clean up and debug.
def get_date_nc_file(
        satellite: str, 
        start_date: str, 
        end_date: str = "", 
        save_dir: Path = Path("./rads_data")
        ) -> None:

    if not satellite:
        raise ValueError("Satellite not specified")
    if not start_date:
        raise ValueError("Date not specified")

    cyc_path = Path(str(os.getenv("RADS_CYCLES")))
    save_dir.mkdir(parents=True, exist_ok=True)
    user_start_date = parse_rads_datetime(start_date)
    user_end_date = parse_rads_datetime(end_date) if (end_date[:4].isdigit()) else datetime.max.replace(tzinfo=timezone.utc)
    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]
    downloaded = False

    for file in sat_phases:
        cyc_first_date, cyc_last_date = read_first_last_pass(f"{cyc_path}/{file}")

        if (cyc_last_date < user_start_date) or (cyc_first_date > user_end_date):
            continue

        print(f"Dates found in file: {file}")

        phase_code = file[2]
        start_cycle_num = read_cycle_file(f"{cyc_path}/{file}", user_start_date)
        end_cycle_num = read_cycle_file(f"{cyc_path}/{file}", user_end_date)

        if (start_cycle_num.isdigit() and end_cycle_num.isdigit()):
            for each_cycle in range(int(start_cycle_num), int(end_cycle_num) + 1):
                try:
                    get_custom_nc_file(satellite, str(each_cycle).zfill(3), phase_code=phase_code)
                except Exception as e:
                    print(f"Cycle number {str(each_cycle).zfill(3)} was not found. \nException message: {e}")

                zip_name = f"{satellite}_c{str(each_cycle).zfill(3)}.zip"
                zip_cmd = ['zip', '-r', str(zip_name), '.']
                subprocess.run(zip_cmd, cwd=str(save_dir / satellite / f'c{str(each_cycle).zfill(3)}'), check=True)
            
            downloaded = True

# FIXME For now only download one cycle base on date. Is it worth updating to download everything until the latest data??
        elif (start_cycle_num.isdigit()):
            get_custom_nc_file(satellite, start_cycle_num, phase_code=phase_code)
        else:
            print(f"{start_cycle_num}")

    if (not downloaded):
        print("No matching data found in the selected date range!")

    return None

def read_cycle_file(file_path: str, date: datetime) -> str:
    with open(file_path, 'r') as f:
        for cycle in f:
            if (parse_rads_datetime(cycle.split()[4]) < date) and (parse_rads_datetime(cycle.split()[5]) > date):
                return cycle.split()[1]

    return "Couldn't find the requested data!"

def sec85_to_utc(sec: str) -> datetime:
    sec85 = float(sec)
    base = datetime(1985, 1, 1, tzinfo=timezone.utc)
    return base + timedelta(seconds=sec85)