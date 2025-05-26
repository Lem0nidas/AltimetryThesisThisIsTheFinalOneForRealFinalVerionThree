from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.post("/api/download")
async def download_data(request: DownloadRequest):
    print(f"Received satellite request: {request.satellite}")
    # Placeholder: you can later trigger a file fetch, job queue, etc.
    return {"message": f"Received request for satellite: {request.satellite}"}
