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


def generate_manifest(author, type_pack, mainfest_uuid, dependencies=None, min_engine_version=[1, 20, 50]):
    manifest = {
        "format_version": 2,
        "metadata": {
            "authors": [author]
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
    if author:
        manifest["metadata"] = {"authors": [author]}
    if dependencies:
        manifest["dependencies"] = dependencies
    if isinstance(min_engine_version, str):
        min_engine_version = [int(x) for x in min_engine_version.split(".")]
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
    folder_structure = {
        "BP": {
            "animations": {},
            "animation_controllers": {},
            "entities": {},
            "functions": {},
            "items": {},
            "loot_tables": {},
            "recipes": {},
            "texts": {}
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
            "ui": {}
        }
    }
    create_folder_structure(folder_structure, Path(destination_folder))

    BP_en_US_lang = f"pack.name={project_name} BP\npack.description=Behavior Pack for {project_name}"
    RP_en_US_lang = f"pack.name={project_name} RP\npack.description=Resource Pack for {project_name}"

    file_structure = {
        "BP": {
            "entities": {},
            "functions": {"tick.json": json.dumps({"values": []})},
            "loot_tables": {"empty.json": "{}"},
            "manifest.json": generate_manifest(author, "data", bp_uuid,
                                               [{"uuid": rp_uuid, "version": [1, 0, 0]}], min_engine_version),
            "texts": {
                "en_US.lang": BP_en_US_lang,
                "languages.json": '["en_US"]'
            }
        },
        "RP": {
            "biomes_client.json": "{}",
            "blocks.json": "{}",
            "font": {},
            "manifest.json": generate_manifest(author, "resources", rp_uuid,
                                               [{"uuid": bp_uuid, "version": [1, 0, 0]}], min_engine_version),
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
            }
        }
    }

    create_file_structure(file_structure, Path(destination_folder))


if __name__ == "__main__":
    main()
