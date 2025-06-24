from fastapi import APIRouter, HTTPException
from models.request_models import *
from services.rads_sync_latest import get_latest_nc_file
from services.rads_sync_custom import get_custom_nc_file
from services.rads_sync_date import get_date_nc_file

router = APIRouter()


@router.post("/api/download")
async def download_data(request: CustomRequest):
    return {
        "message": f"Received request for satellite: {request.satellite} for cycle: {request.cycle_num} and pass: {request.pass_num}"
        }


@router.post("/api/download_latest")
def download_raw_data(request: DownloadRequest):
    if not request.satellite:
        raise HTTPException(status_code=400, detail="Missing 'satellite' key")

    try:
        get_latest_nc_file(request.satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Download for satellite {request.satellite} triggered"}

@router.post("/api/download_custom")
def download_custom_data(req: CustomRequest):
    if not req.satellite:
        raise HTTPException(status_code=400, detail="Missing 'satellite' key")
    
    try: 
        get_custom_nc_file(req.satellite, req.cycle_num, req.pass_num)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Received request for {req.satellite}/{req.cycle_num} data"}

@router.post("/api/download_date")
def download_by_date(req: DateRequest):
    if not req.satellite:
        raise HTTPException(status_code=400, detail="Missing 'satellite' key")
    
    try:
        get_date_nc_file(req.satellite, req.start_date, req.end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": f"Reicived request for {req.satellite} with start date {req.start_date}"}
