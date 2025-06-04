import subprocess
import re
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# TODO Make improvments
def get_custom_nc_file(satellite: str, cycle_num: str, pass_num: str = "", save_dir: Path = Path("./rads_data")) -> bool:
    remote_base = os.getenv("RADS_REMOTE_BASE")
    save_dir.mkdir(parents=True, exist_ok=True)
    cycle_num = "".join(["c", cycle_num])
    pass_num = "".join(["p", pass_num])
    
    if not satellite:
        raise ValueError("Satellite not specified")
    
    if not cycle_num:
        raise ValueError("Cycle not specified")
    
    file_cmd = ['rsync', f'{remote_base}/{satellite}/a/{cycle_num}/']
    try:
        files_in_cycle = subprocess.check_output(file_cmd, env=os.environ, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to list files in {satellite}/{cycle_num}.") from e
    
    # TODO Is this nessesary? maybe combine it with pass_num?
    nc_files = re.findall(r'(\S+\.nc)', files_in_cycle)
    if not nc_files:
        raise RuntimeError(f"No .nc files found in {satellite}/{cycle_num}.")
    
    if pass_num != "p":
        try:
            custom_file_name = next((line for line in files_in_cycle.splitlines() if pass_num in line and line.endswith(".nc")), None)
            filename = custom_file_name.split()[-1] if custom_file_name else None
            remote_file_path = f'{remote_base}/{satellite}/a/{cycle_num}/{filename}'
        except StopIteration:
            raise RuntimeError(f"No file found for pass number {pass_num} in {satellite}/{cycle_num}.")
    else:
        remote_file_path = f'{remote_base}/{satellite}/a/{cycle_num}/'
        
    local_target = save_dir / satellite / cycle_num # FIXME Files get downloaded in wrong folder
    local_target.mkdir(parents=True, exist_ok=True)

    
    download_cmd = ['rsync', '-avz', '--del', remote_file_path, str(local_target)]
    subprocess.run(download_cmd, env=os.environ, check=True)
    
    return True
