import asyncio
import json
import os
import time
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse

from lib.utils import targets_save_module


async def execute_shell(cmd: str) -> str:
    """Execute shell command asynchronously"""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode()}")

    return stdout.decode()


def init(app: FastAPI, cfg: dict):
    @app.post("/build")
    async def build_endpoint(request: Request, project: str = Query(...)):
        """Build project from flow data"""
        try:
            # Find project configuration
            prj = cfg["projects"].get(project)
            if not prj:
                return JSONResponse(
                    status_code=400, content={"error": "Project not found"}
                )

            module = await request.json()

            # Create temporary file
            unique_filename = f"{cfg['tmpidr']}/{int(time.time() * 1000)}.json"
            os.makedirs(os.path.dirname(unique_filename), exist_ok=True)

            with open(unique_filename, "w") as f:
                json.dump(module, f)

            targets_save_module(prj, module)

            # Build commands for each target
            cmds = []
            for target in prj["targets"]:
                cmd = f"{cfg['system']['python3']} {cfg['system']['flow2code']['path']} -t {target['template']} -o {target['path']} {unique_filename}"
                cmds.append(cmd)

            print("Commands:", cmds)

            # Execute all commands
            for cmd in cmds:
                await execute_shell(cmd)

            return {"ok": 1}

        except Exception as e:
            raise
            return JSONResponse(
                status_code=500, content={"error": f"Build failed: {str(e)}"}
            )
