import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

def get_cycles(satellite: str):
    load_dotenv()
    cycles_path = Path(os.getenv("RADS_CYCLES", "/"))
    sat_phases = sorted([f.name for f in cycles_path.iterdir() if f.is_file() and f.name.startswith(satellite)])

    cycles = []
    
    for file in sat_phases:
        file_path = cycles_path / file
        with open(file_path) as f:
            for line in f:
                parts = line.split()
                cycle_number = parts[1]
                start_date = parse_date(parts[4])
                end_date = parse_date(parts[5])
    
                cycles.append({
                    "cycle": cycle_number,
                    "start": start_date,
                    "end": end_date
                })
    return cycles

def parse_date(date_str):
    return datetime.strptime(date_str.split('.')[0], "%y%m%d%H%M%S").date().isoformat()