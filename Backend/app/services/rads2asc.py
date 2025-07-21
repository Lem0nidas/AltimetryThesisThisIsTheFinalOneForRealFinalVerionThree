import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from utils.arg_mapping import arg_map


load_dotenv()

# TODO DO it
def get_asc(
        satellite: str,
        # cycle: str, #FIXME I can get this from the options/kwargs argument! Figure out how to extract it
        options: dict[str, str],
        cycle: str = "127",
        save_dir: Path = Path("./rads_data")
        ):

    if not satellite:
        raise ValueError("Satellite not specified")

    # if options['cycle_num']:
    #     file_path = save_dir / satellite / options['cycle_num']
    # else: file_path = save_dir / satellite

    file_path: Path = save_dir / satellite / cycle

    if files_exist(file_path):
        process_cmd = command_list(options)
        subprocess.run(process_cmd, env=os.environ, check=True)
    else:
        print("First you must download the files localy.") #TODO Prompt the user to download the files if they are not found

    return

def command_list(args, **kwargs) -> list[str]:
    command = ['rads2asc', '-S', '3a']
    for key, val in args.items():
        if key in arg_map and val is not None:
            command += [arg_map[key], str(val)]

    print(args)
    print(command)
    
    return command

def files_exist(path: Path) -> bool:
    satellite: str = path.parts[-2]
    cycle: str = path.parts[-1]

    for root, dirs, files in os.walk(path):
        for file in files:
            if (f'{satellite}' and f'c{cycle}') in file:
                return True
    return False


if __name__ == "__main__":
    # command_list({
    #     'sat': 'j2',
    #     'cycle': '10,20',
    #     'pass': '101,110',
    #     'region': '-8,42,28,48',
    #     'vars': 'time,lat,lon,sla,swh,wind_speed',
    #     'output': 'output.asc',
    # }, sat='j2', cycle='10,20', satellite='j3', format='')

    print(files_exist(Path("./Backend/rads_data/3a/127")))

