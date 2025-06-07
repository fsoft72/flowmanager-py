import json
import gzip
import os
from io import StringIO
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse

def init(app: FastAPI, cfg: dict):
    @app.post("/save/to/project")
    async def save_to_project(request: Request, project: str = Query(...)):
        """Save flow data to project directory"""
        try:
            body = await request.json()
            
            # Find project configuration
            proj = cfg['projects'].get(project)
            if not proj:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Project {project} not found"}
                )
            
            # Get the target called 'liwe3' from proj.targets
            target = None
            for t in proj['targets']:
                if t['template'] == 'liwe3':
                    target = t
                    break
            
            # If no 'liwe3' target found, use the first target
            if not target and proj['targets']:
                target = proj['targets'][0]
            
            if not target:
                return JSONResponse(
                    status_code=400,
                    content={"error": "No valid target found"}
                )
            
            # Create destination path
            dest_filename = f"{target['path']}/work/liweflow.json.gz"
            os.makedirs(os.path.dirname(dest_filename), exist_ok=True)
            
            # Convert to JSON and compress
            json_data = json.dumps(body)
            
            with gzip.open(dest_filename, 'wt', encoding='utf-8') as f:
                f.write(json_data)
            
            return {"ok": 1}
            
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to save: {str(e)}"}
            )
