import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse


def init(app: FastAPI, cfg: dict):
    @app.post("/save/markdown")
    async def save_markdown(request: Request, project: str = Query(...)):
        """Save markdown documentation to project directories"""
        try:
            body = await request.json()

            # Find project configuration
            proj = cfg["projects"].get(project)
            if not proj:
                return JSONResponse(
                    status_code=400, content={"error": f"Project {project} not found"}
                )

            # Get all targets that have savedocs === true
            targets = [t for t in proj["targets"] if t.get("savedocs") is True]

            # If no targets are found, simply return ok
            if not targets:
                return {"ok": 1}

            module = body.get("module")
            markdown = body.get("markdown", "")

            for target in targets:
                print(f"=== SAVE MARKDOWN: targets={targets}, proj={proj}")

                dest_dir = f"{target['path']}/work/docs/modules"

                if target.get("docs_path"):
                    dest_dir = target["docs_path"]

                # Create dest_dir if it does not exist
                os.makedirs(dest_dir, exist_ok=True)

                dest_filename = f"{dest_dir}/{module}.md"

                # Save markdown content to file
                with open(dest_filename, "w", encoding="utf-8") as f:
                    f.write(markdown)

            return {"ok": 1}

        except Exception as e:
            return JSONResponse(
                status_code=500, content={"error": f"Failed to save markdown: {str(e)}"}
            )
