import subprocess
import re
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# TODO Make the /rads_data directory accesable. I still get the error Permission denied.
# FIXME Download only from "a" phase.
def get_latest_nc_file(
        satellite: str, 
        local_dir: Path = Path("./rads_data")
        ) -> Path:

    remote_base = os.getenv("RADS_REMOTE_BASE")

    if not satellite:
        raise ValueError("Satellite not specified.")

    local_dir.mkdir(parents=True, exist_ok=True)

    cycle_cmd = ['rsync', f'{remote_base}/{satellite}/a/']
    try:
        cycles_output = subprocess.check_output(cycle_cmd, env=os.environ, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to list remote cycles.") from e

    cycle_dirs = re.findall(r'c\d{3}', cycles_output)
    if not cycle_dirs:
        raise RuntimeError("No cycle directories found.")

    last_cycle = sorted(cycle_dirs)[-1].strip('/')

    file_cmd = ['rsync', f'{remote_base}/{satellite}/a/{last_cycle}/']
    try:
        files_output = subprocess.check_output(file_cmd, env=os.environ, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to list files in {last_cycle}.") from e

    nc_files = re.findall(r'(\S+\.nc)', files_output)
    if not nc_files:
        raise RuntimeError(f"No .nc files found in {last_cycle}.")

    latest_file = sorted(nc_files)[-1]

    remote_file_path = f'{remote_base}/{satellite}/a/{last_cycle}/{latest_file}'
    local_target = local_dir / latest_file

    download_cmd = ['rsync', '-avz', remote_file_path, str(local_target)]
    subprocess.run(download_cmd, env=os.environ, check=True)

    return local_target
