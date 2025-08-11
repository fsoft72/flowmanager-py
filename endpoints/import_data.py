import os
import gzip
from fastapi import FastAPI
from fastapi.responses import JSONResponse


def init(app: FastAPI, cfg: dict):
    @app.get("/import")
    async def import_endpoint():
        """Import the latest backup file"""
        try:
            # Scan backup directory for .gz files
            backup_path = cfg["backup"]["path"]
            files = os.listdir(backup_path)
            gz_files = [
                f
                for f in files
                if f.endswith(".json.gz") and not f.startswith("latest")
            ]

            # Sort files by filename
            gz_files.sort()

            # Get the latest file
            if not gz_files:
                return JSONResponse(
                    status_code=404, content={"error": "No backup files found"}
                )

            latest_file = gz_files[-1]
            latest_path = os.path.join(backup_path, latest_file)

            # Read and decompress the gzip file
            with gzip.open(latest_path, "rt", encoding="utf-8") as f:
                json_content = f.read()

            return json_content

        except Exception as e:
            return JSONResponse(
                status_code=500, content={"error": f"Failed to import: {str(e)}"}
            )
