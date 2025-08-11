import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.crypt import json_encrypt

from endpoints import (
    backup,
    build,
    projects,
    import_data,
    save_markdown,
    save_to_project,
)

# Load configuration
with open("cfg.json", "r") as f:
    cfg = json.load(f)

app = FastAPI(title="FlowManager", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(cfg["tmpidr"], exist_ok=True)
os.makedirs(cfg["backup"]["path"], exist_ok=True)

# Initialize endpoints
backup.init(app, cfg)
build.init(app, cfg)
projects.init(app, cfg)
import_data.init(app, cfg)
save_markdown.init(app, cfg)
save_to_project.init(app, cfg)


@app.get("/hello")
async def hello():
    """Test endpoint to check if flow is working"""
    return json_encrypt({"hello": "world"})
