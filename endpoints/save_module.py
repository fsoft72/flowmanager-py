import json
import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse

def init(app: FastAPI, cfg: dict):
    @app.post("/save/module")
    async def save_module(request: Request, project: str = Query(...)):
        """Save module data to project directories"""
        try:
            body = await request.json()
            
            # Find project configuration
            proj = cfg['projects'].get(project)
            if not proj:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Project {project} not found"}
                )
            
            # Get all targets that have savemodule === true
            targets = [t for t in proj['targets'] if t.get('savemodule') is True]
            
            # If no targets are found, simply return ok
            if not targets:
                return {"ok": 1}
            
            # Generate everything for all targets
            for target in targets:
                dest_dir = f"{target['path']}/work/modules"
                
                # Create dest_dir if it does not exist
                os.makedirs(dest_dir, exist_ok=True)
                
                try:
                    orig = json.loads(body.get('module', '{}'))
                except (json.JSONDecodeError, TypeError):
                    orig = body.get('module', {})
                
                module_data = json.dumps(orig, indent=2)
                name = (body.get('name', '')).lower().replace(' ', '_')
                dest_filename = f"{dest_dir}/{name}.json"
                
                # Save module content to file
                with open(dest_filename, 'w', encoding='utf-8') as f:
                    f.write(module_data)
            
            return {"ok": 1}
            
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to save module: {str(e)}"}
            )
