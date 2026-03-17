import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv
from utils.phase_mapping import locate_phase
from pydantic import ValidationError

load_dotenv()

# TODO Make improvments
def get_custom_nc_file(
        satellite: str, 
        cycle_num: str, 
        pass_num: str = "",
        ) -> None:
    
    if not satellite:
        raise ValueError("Satellite not specified")
    if not cycle_num:
        raise ValueError("Cycle not specified")
    
    remote_base = os.getenv("RADS_REMOTE_BASE")
    rads_dir = Path(os.getenv("RADSDATAROOT", "/"))
    cycle_num = "".join(["c", cycle_num.zfill(3)])
    phase_code = locate_phase(satellite, cycle_num[1:])

    file_cmd = ['rsync', f'{remote_base}/{satellite}/{phase_code}/{cycle_num}/']
    try:
        files_in_cycle = subprocess.check_output(file_cmd, env=os.environ, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to list files in {satellite}/{cycle_num}.") from e
    
    if pass_num != "":
        pass_num = "".join(["p", pass_num.zfill(4)])
        try:
            custom_file_name = next((line for line in files_in_cycle.splitlines() if pass_num in line and line.endswith(".nc")), None)
            filename = custom_file_name.split()[-1] if custom_file_name else None
            remote_file_path = f'{remote_base}/{satellite}/{phase_code}/{cycle_num}/{filename}'
        except StopIteration:
            raise RuntimeError(f"No file found for pass number {pass_num} in {satellite}/{cycle_num}.")
        except ValidationError:
            print('Must be integer')
            raise ValidationError

    else:
        remote_file_path = f'{remote_base}/{satellite}/{phase_code}/{cycle_num}/'
        
    local_target = rads_dir / satellite / phase_code / cycle_num
    local_target.mkdir(parents=True, exist_ok=True)

    
    download_cmd = ['rsync', '-avz', '--del', remote_file_path, str(local_target)]
    subprocess.run(download_cmd, env=os.environ, check=True)
    
    return None
