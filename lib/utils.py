import json
import os


def targets_save_module(proj, module):
    """Save module data to project targets"""
    # Get all targets that have savemodule === true
    targets = [t for t in proj["targets"] if t.get("savemodule") is True]

    # If no targets are found, simply return ok
    if not targets:
        return {"ok": 1}

    # Generate everything for all targets
    for target in targets:
        json_dir = proj.get("json_dir") or target.get("json_dir")
        savemodule(target["path"], module, json_dir=json_dir)

    return {"ok": 1}


def savemodule(path, module, json_dir=None):
    if json_dir:
        dest_dir = json_dir
    else:
        dest_dir = f"{path}/work/modules"

    # Create dest_dir if it does not exist
    os.makedirs(dest_dir, exist_ok=True)

    module_data = json.dumps(module, indent=2, default=str)
    name = module.get("name", "").lower().replace(" ", "_")
    dest_filename = f"{dest_dir}/{name}.json"

    # Save module content to file
    with open(dest_filename, "w", encoding="utf-8") as f:
        f.write(module_data)
