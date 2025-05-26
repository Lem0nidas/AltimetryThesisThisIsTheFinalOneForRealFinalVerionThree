import subprocess
import re

def get_latest_ers1_nc(remote_base='radsuser@rads.tudelft.nl::rads/data/e1'):
    # List all available cycles for ERS-1 in phase "a"
    phase = 'a'
    rsync_cmd_list_cycles = ['rsync', '--list-only', f'{remote_base}/{phase}/']
    cycles_output = subprocess.check_output(rsync_cmd_list_cycles, text=True)
    cycle_dirs = re.findall(r'c\d{3}/', cycles_output)
    
    if not cycle_dirs:
        raise Exception("No cycle directories found.")

    # Sort cycle directories to find the latest one
    last_cycle = sorted(cycle_dirs)[-1].strip('/')

    # List files in the latest cycle directory
    rsync_cmd_list_files = ['rsync', '--list-only', f'{remote_base}/{phase}/{last_cycle}/']
    files_output = subprocess.check_output(rsync_cmd_list_files, text=True)
    nc_files = re.findall(r'(\S+\.nc)', files_output)

    if not nc_files:
        raise Exception(f"No .nc files found in {last_cycle}.")

    # Sort by pass number assuming format e1pPPPPcCCC.nc
    latest_file = sorted(nc_files)[-1]
    print(f"Latest file: {latest_file}")

    # Download the file
    remote_file_path = f'{remote_base}/{phase}/{last_cycle}/{latest_file}'
    local_target = f'./{latest_file}'
    rsync_cmd_download = ['rsync', '-avz', remote_file_path, local_target]
    subprocess.run(rsync_cmd_download)

    return latest_file

# Run the function
latest = get_latest_ers1_nc()
print(f"Downloaded: {latest}")
