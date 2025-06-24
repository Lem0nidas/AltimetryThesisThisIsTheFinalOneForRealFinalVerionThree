from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.download_routes import router

app = FastAPI()

# Allow your Svelte frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
