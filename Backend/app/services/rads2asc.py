import os
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from utils.arg_mapping import arg_map #When runnig from main.py
# from temp import arg_map #When executing only this file



load_dotenv()

# TODO DO it
def get_asc( #TODO change this name
        satellite: str,
        options: dict[str, str],
        save_dir: Path = Path("./rads_proccessed_data"),
        check_path: Path = Path("./rads_data"),
        ):

    if not satellite:
        raise ValueError("Satellite not specified!")
    elif not options:
        raise ValueError("Options not specified!")
    elif not ('cycle' in options):
        raise ValueError("Cycle not specified!")
    
    save_dir.mkdir(parents=True, exist_ok=True)

    cycle = options['cycle']
    cycle = "".join(["c", cycle])
    file_path = check_path

    if cycle_files_exist(file_path, satellite=satellite, cycle=cycle):
        process_cmd = command_list(satellite, options)
        subprocess.run(process_cmd, env=os.environ, check=True)
    else:
        print("First you must download the files localy.")

    return

def command_list(satellite: str, options: dict[str, str]) -> list[str]:
    command = ['rads2asc', '-S', satellite]
    for key, val in options.items():
        if key in arg_map and val is not (None or ''):
            command += [arg_map[key], str(val)]

    # command += ['--output', '/home/leon/Desktop/Altimetry Project/Backend/rads_proccessed_data/aa']
    # final = command + ['-O /rads_proccessed_data'] #TODO save to different location
    return command


def cycle_files_exist(path: Path, satellite: str, cycle: str) -> bool:
    for root, dirs, files in os.walk(path):
        if satellite in dirs:
            satellite_dir = os.path.join(root, satellite)
            
            if cycle in os.listdir(satellite_dir):
                return True
    return False


if __name__ == "__main__":
    command_list(
        '3a',
        {
        'sat': 'j2',
        'cycle': '10,20',
        'pass': '',
        'region': '-8,42,28,48',
        'vars': 'time,lat,lon,sla,swh,wind_speed',
        'output': 'output.asc',
        },)

    get_asc(
                '3a',
        {
        'sat': 'j2',
        'cycle': '10,20',
        'pass': '',
        'region': '-8,42,28,48',
        'vars': 'time,lat,lon,sla,swh,wind_speed',
        'output': 'output.asc',
        },
    )
    # print(files_exist(Path("./Backend/rads_data/3a/127")))

