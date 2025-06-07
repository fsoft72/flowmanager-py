from fastapi import FastAPI
from fastapi.responses import JSONResponse

def init(app: FastAPI, cfg: dict):
    @app.get("/projects")
    async def list_projects():
        """List all project keys"""
        projects = list(cfg['projects'].keys())
        return {"projects": projects}
    
    @app.get("/targets")
    async def list_targets():
        """List all projects with their names"""
        projects = {}
        for project_key, project_data in cfg['projects'].items():
            projects[project_key] = project_data['name']
        
        return {"projects": projects}
