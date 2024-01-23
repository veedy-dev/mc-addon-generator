import os
import json
import uuid
from pathlib import Path


def create_folder_structure(folder_structure, base_path):
    for key, value in folder_structure.items():
        path = base_path / key
        path.mkdir(parents=True, exist_ok=True)
        if isinstance(value, dict):
            create_folder_structure(value, path)


def create_file_structure(file_structure, root_path):
    for key, value in file_structure.items():
        path = root_path / key
        if isinstance(value, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_file_structure(value, path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as file:
                file.write(value)


def generate_manifest(author, type_pack, mainfest_uuid, use_scripting_api=False, bp_uuid=None, rp_uuid=None, min_engine_version=[1, 20, 50]):
    if isinstance(min_engine_version, str):
        min_engine_version = [int(x) for x in min_engine_version.split(".")]

    # Construct the base manifest structure
    manifest = {
        "format_version": 2,
        "metadata": {
            "authors": [author] if author else []
        },
        "header": {
            "name": "pack.name",
            "description": "pack.description",
            "uuid": mainfest_uuid,
            "version": [1, 0, 0],
            "min_engine_version": min_engine_version
        },
        "modules": [
            {
                "type": type_pack,
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0]
            }
        ]
    }

    # Add scripting capabilities, modules, and dependencies for BP
    if type_pack == "data" and use_scripting_api:
        manifest["capabilities"] = ["script_eval"]
        manifest["modules"].append({
            "description": "Scripting Module",
            "type": "script",
            "uuid": str(uuid.uuid4()),
            "version": [1, 0, 0],
            "language": "javascript",
            "entry": "scripts/main.js"
        })
        server_version = input(
            "Enter the @minecraft/server version (default 1.7.0): ") or "1.7.0"
        server_ui_version = input(
            "Enter the @minecraft/server-ui version (default 1.1.0): ") or "1.1.0"
        manifest["dependencies"] = [
            {"uuid": rp_uuid, "version": [1, 0, 0]},
            {"module_name": "@minecraft/server", "version": server_version},
            {"module_name": "@minecraft/server-ui", "version": server_ui_version}
        ]
    elif type_pack == "resources":
        # Set dependencies for RP
        manifest["dependencies"] = [
            {"uuid": bp_uuid, "version": [1, 0, 0]}] if bp_uuid else []

    return json.dumps(manifest, indent=4)


def main():
    project_name = input("Enter the project name: ")
    min_engine_version = input(
        "Enter the minimum engine version (e.g., 1.20.50): ")
    if not min_engine_version:
        min_engine_version = "1.20.50"
    author = input("Enter the author name (leave empty if none): ")
    bp_uuid = str(uuid.uuid4())
    rp_uuid = str(uuid.uuid4())

    destination_folder = input(
        "Enter the destination folder for the generated project (leave empty for the current folder): ")
    if not destination_folder:
        destination_folder = "."

    use_scripting_api = input("Use Scripting API? (y/n): ").lower() == 'y'
    folder_structure = {
        "BP": {
            "animations": {},
            "animation_controllers": {},
            "entities": {},
            "functions": {},
            "items": {},
            "loot_tables": {},
            "recipes": {},
            "texts": {},
            "loot_tables": {},
            "functions": {},
            "spawn_rules": {},
        },
        "RP": {
            "animations": {},
            "animation_controllers": {},
            "entity": {},
            "items": {},
            "font": {},
            "models": {"entity": {}},
            "particles": {},
            "render_controllers": {},
            "sounds": {},
            "textures": {},
            "ui": {},
        }
    }
    create_folder_structure(folder_structure, Path(destination_folder))

    BP_en_US_lang = f"pack.name={project_name} BP\npack.description=Behavior Pack for {project_name}"
    RP_en_US_lang = f"pack.name={project_name} RP\npack.description=Resource Pack for {project_name}"

    main_js_template = """import { system, world } from '@minecraft/server'
world.afterEvents.entitySpawn.subscribe((event) => {
    console.warn(event.entity.typeId + ' spawned!');
});

system.run(() => {
    // Code in here will be run every tick
});
// See more at https://wiki.bedrock.dev/scripting/script-server.html
"""
    # Generate BP manifest
    bp_manifest = generate_manifest(
        author, "data", bp_uuid, use_scripting_api, rp_uuid=rp_uuid, min_engine_version=min_engine_version)

    # Generate RP manifest
    rp_manifest = generate_manifest(
        author, "resources", rp_uuid, False, bp_uuid=bp_uuid, min_engine_version=min_engine_version)

    file_structure = {
        "BP": {
            "entities": {},
            "functions": {"tick.json": json.dumps({"values": []})},
            "loot_tables": {"empty.json": "{}"},
            "manifest.json": bp_manifest,
            "texts": {
                "en_US.lang": BP_en_US_lang,
                "languages.json": '["en_US"]'
            }
        },
        "RP": {
            "biomes_client.json": "{}",
            "blocks.json": "{}",
            "font": {},
            "manifest.json": rp_manifest,
            "sounds": {
                "sound_definitions.json": json.dumps({
                    "format_version": "1.14.0",
                    "sound_definitions": {}
                }, indent=4)
            },
            "texts": {
                "en_US.lang": RP_en_US_lang,
                "languages.json": '["en_US"]'
            },
            "textures": {
                "flipbook_textures.json": "{}",
                "item_texture.json": json.dumps({
                    "resource_pack_name": project_name,
                    "texture_name": "atlas.items",
                    "texture_data": {}
                }, indent=4),
                "terrain_texture.json": "{}",
            },
            "sounds.json": json.dumps({"entity_sounds": {"entities": {}}}, indent=4)
        }
    }
    if use_scripting_api:
        file_structure["BP"]["scripts"] = {"main.js": main_js_template}

    create_file_structure(file_structure, Path(destination_folder))


if __name__ == "__main__":
    main()
