import os
from pathlib import Path
from dotenv import find_dotenv
from datetime import datetime, timedelta, timezone
from services.rads_sync_custom import get_custom_nc_file


find_dotenv()

# TODO Make improvments
def get_date_nc_file(satellite: str, date: str, save_dir: Path = Path("./rads_data")) -> None:

    if not satellite:
        raise ValueError("Satellite not specified")
    if not date:
        raise ValueError("Date not specified")

    cyc_path = Path(str(os.getenv("RADS_CYCLES")))
    pass_path = Path(str(os.getenv("RADS_PASSES")))
    save_dir.mkdir(parents=True, exist_ok=True)
    user_date = parse_rads_datetime(date)
    sat_phases = [f.name for f in cyc_path.iterdir() if f.is_file() and f.name.startswith(satellite)]

    for file in sat_phases:
        cyc_first_date, cyc_last_date = read_first_last_line(f"{cyc_path}/{file}")
        if (cyc_first_date < user_date) and (cyc_last_date > user_date):
            print(f"Dates found in file: {file}")

            pass_num, cycle_num = read_pass_file(f"{pass_path}/{file[:-4]}.pas", user_date)

            if (pass_num.isdigit() & cycle_num.isdigit()):
                get_custom_nc_file(satellite, cycle_num, pass_num)
            else:
                print(f"{pass_num}\n{cycle_num}")

            return
        else:
            print(f"Dates were not found in {file}")
        
    return None


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


def read_first_last_line(file_path) -> tuple[datetime, datetime]:
    with open(file_path, 'r') as f:
        first = f.readline().split(" ")[4]

    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Go to second-last byte (avoid EOF)
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move backward until a newline
        last = f.readline().decode().split(" ")[5]

    return parse_rads_datetime(first), parse_rads_datetime(last)


def read_pass_file(file_path: str, date: datetime) -> tuple[str, str]:
    with open(file_path, 'r') as f:
        for pas in f:
            if (sec85_to_utc(pas.split()[3]) < date) and (sec85_to_utc(pas.split()[4]) > date):
                pass_num = pas.split()[2]
                cyc_num = pas.split()[1]
                return pass_num, cyc_num
            else:
                continue
    return ("Couldn't find pass number!", "Couldn't find cycle number!")


def sec85_to_utc(sec: str) -> datetime:
    sec85 = float(sec)
    base = datetime(1985, 1, 1, tzinfo=timezone.utc)
    return base + timedelta(seconds=sec85)