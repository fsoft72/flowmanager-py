import json
import gzip
import os
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def init(app: FastAPI, cfg: dict):
    @app.post("/backup")
    async def backup_endpoint(request: Request):
        """Save backup file with gzip compression"""
        try:
            body = await request.json()
            
            # Create filename with YYYYMMDD-HHMMSS
            now = datetime.now()
            date = now.strftime('%Y%m%d')
            time = now.strftime('%H%M%S')
            filename = f"{date}-{time}.json"
            unique_filename = f"{cfg['backup']['path']}/{filename}.gz"
            
            # Convert to JSON string
            json_data = json.dumps(body, indent=4)
            
            # Compress and save
            with gzip.open(unique_filename, 'wt', encoding='utf-8') as f:
                f.write(json_data)
            
            # Handle latest symlink
            latest = f"{cfg['backup']['path']}/latest.json.gz"
            if os.path.exists(latest):
                os.unlink(latest)
            
            # Create symlink to latest file
            os.symlink(unique_filename, latest)
            
            print(f"Backup saved to {unique_filename}")
            return {"ok": 1}
            
        except Exception as e:
            print(f"Pipeline failed: {e}")
            return JSONResponse(
                status_code=500, 
                content={"code": 500, "message": "Pipeline failed."}
            )
