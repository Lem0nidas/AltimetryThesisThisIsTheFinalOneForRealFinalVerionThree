from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.rads_sync_latest import get_latest_nc_file
from services.rads_sync_custom import get_custom_nc_file


app = FastAPI()

# Allow your Svelte frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    satellite: str

class CustomRequest(BaseModel):
    satellite: str
    cycle_num: str
    pass_num: str

@app.post("/api/download")
async def download_data(request: DownloadRequest):
    print(f"Received satellite request: {request.satellite}")
    # Placeholder: you can later trigger a file fetch, job queue, etc.
    return {"message": f"Received request for satellite: {request.satellite}"}


@app.post("/api/download_latest")
def download_raw_data(request: DownloadRequest):
    if not request.satellite:
        raise HTTPException(status_code=400, detail="Missing 'satellite' key")

    try:
        get_latest_nc_file(request.satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Download for satellite {request.satellite} triggered"}

@app.post("/api/download_custom")
def download_custom_data(req: CustomRequest):
    if not req.satellite:
        raise HTTPException(status_code=400, detail="Missing 'satellite' key")
    
    try: 
        get_custom_nc_file(req.satellite, req.cycle_num, req.pass_num)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Received request for {req.satellite}/{req.cycle_num} data"}