import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from utils.arg_mapping import arg_map
from utils.reg_mapping import reg_map
# from temp import arg_map




load_dotenv()

def get_processed(
        satellite: str,
        options: dict[str, str | list[str]],
        file_type: bool,
        ):

    if not satellite:
        raise ValueError("Satellite not specified")
    
    existing_cycles = files_exist(satellite, options['cycle'])

    if existing_cycles:
        options['cycle'] = sorted([p.name[1:] for p in existing_cycles], key=int)
        process_cmd = command_list(satellite, options, file_type)
        subprocess.run(process_cmd, env=os.environ, check=True)
    else:
        print("First you must download the files localy.")
    return

def command_list(satellite: str, options: dict[str, str | list[str]], file: bool) -> list[str]:
    if (not file):
        programm = 'rads2asc'
    else:
        programm = 'rads2nc'

    command = [programm, '-S', satellite]
    if not options.get('region'):
        del options['region']
    elif options['region'] in reg_map:
        options['region'] = reg_map[options['region']]

    if not options.get('cycle'):
        del options['cycle']

    for key, val in options.items():
        if (key in arg_map) and (val is not None and val != ''):
            if isinstance(val, list):
                command += [arg_map[key], ",".join(val)]
            else:
                command += [arg_map[key], str(val)]

    command += ['-o', "".join([satellite, ".", programm[:3]])]
    return command

def files_exist(satellite: str, cycles: str | list[str]) -> list:
    root = Path(os.getenv("RADSDATAROOT", "/"))
    satellite_path = root / satellite
    existing: list[Path] = []

    for p in satellite_path.iterdir():
        if not p.is_dir():
            continue
        for cycle in cycles:
            cycle_path = p / "".join(['c', cycle])
            if cycle_path.is_dir():
                existing.append(cycle_path)

    return existing

if __name__ == "__main__":
    print(files_exist("3a", ["c001"]))
