import os
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from utils.arg_mapping import arg_map
from utils.reg_mapping import reg_map
# from temp import arg_map




load_dotenv()

# TODO DO it
def get_asc(
        satellite: str,
        options: dict[str, str],
        ):

    if not satellite:
        raise ValueError("Satellite not specified")
    
    cycle = 'c' + options['cycle']
    phase = 'a'
    if files_exist(satellite, phase, cycle):
        process_cmd = command_list(satellite, options)
        subprocess.run(process_cmd, env=os.environ, check=True)
    else:
        print("First you must download the files localy.") #TODO Prompt the user to download the files if they are not found
    return

def command_list(satellite: str, options: dict[str, str]) -> list[str]:
    command = ['rads2asc', '-S', satellite]
    if not options.get('region'):
        del options['region']

    print(options)
    for key, val in options.items():
        if key in arg_map and (val is not None and val != ''):
            command += [arg_map[key], str(val)]
    
    command += ['-o', "".join([satellite, options['cycle']])]
    return command

def files_exist(satellite: str, phase: str, cycle: str) -> bool:
    home = Path(os.getenv("RADSDATAROOT", "/"))
    expected_path = home / satellite / phase / cycle
    return expected_path.exists()

if __name__ == "__main__":
    # command_list(
    #     '3a',
    #     {
    #     'sat': 'j2',
    #     'cycle': '10,20',
    #     'pass': '',
    #     'region': '-8,42,28,48',
    #     'vars': 'time,lat,lon,sla,swh,wind_speed',
    #     'output': 'output.asc',
    #     },)

    # get_asc(
    #             '3a',
    #     {
    #     'sat': 'j2',
    #     'cycle': '10,20',
    #     'pass': '',
    #     'region': '-8,42,28,48',
    #     'vars': 'time,lat,lon,sla,swh,wind_speed',
    #     'output': 'output.asc',
    #     },
    # )
    print(files_exist("3a", "a", "c001"))
