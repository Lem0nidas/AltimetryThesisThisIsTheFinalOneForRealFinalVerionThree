from fastapi import HTTPException, UploadFile, File
from typing import Dict, Any
from pathlib import Path
import numpy as np
import netCDF4


BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR: Path = BASE_DIR / "tools" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 1024*1024

async def storeNetcdf(file: UploadFile = File(...)) -> dict[str, Any]:
    if file.content_type not in ["application/x-netcdf", "application/netcdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    if not file.filename:
        raise HTTPException(400, "No filename provided") 
    else:
        safe_name = Path(file.filename).name

    contents: bytes = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "File too large")
    
    file_path: Path = UPLOAD_DIR / safe_name
    file_path.write_bytes(contents)

    data: Dict[str, Any] = {}

    def to_json_safe(val):
        if isinstance(val, np.ndarray):
            return val.tolist()
        if isinstance(val, np.generic):
            return val.item()
        return val
    
    try:
        dataset = netCDF4.Dataset(file_path, 'r')
        for var_name, var in dataset.variables.items():
            attrs = {attr: to_json_safe(getattr(var, attr)) for attr in var.ncattrs()}

            data[var_name] = {
                "dimension": list(var.dimensions),
                "attributes": attrs,
                "values": var[:].tolist()
            }

        return data
    except Exception:
        file_path.unlink(missing_ok=True)
        raise HTTPException(400, "Invalid NetCDF file")
    finally:
        dataset.close() # type: ignore

