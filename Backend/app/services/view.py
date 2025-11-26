# This is temporary
from fastapi import UploadFile, File
import tempfile
import netCDF4

async def viewNetcdf(file: UploadFile = File(...)) -> None:

    suffix = '.nc'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
        nc_file = netCDF4.Dataset(tmp_path, 'r')

    print(nc_file.variables.keys())

    temperature = nc_file.variables['swh_ku'][:]
    print(temperature)

    print(nc_file.dimensions)
    print(nc_file.variables['swh_ku'].dimensions)

    print(nc_file.ncattrs())

    temperature_attrs = nc_file.variables['swh_ku'].ncattrs()
    for attr in temperature_attrs:
        print(f"{attr}: {nc_file.variables['swh_ku'].getncattr(attr)}")


    nc_file.close()
