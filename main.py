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


def generate_manifest(name, description, author, type_pack, uuid, dependencies=None):
    manifest = {
        "format_version": 2,
        "header": {
            "description": description,
            "name": name,
            "uuid": uuid,
            "version": [1, 0, 0],
            "min_engine_version": [1, 19, 50]
        },
        "modules": [
            {
                "type": type_pack,
                "uuid": uuid,
                "version": [1, 0, 0]
            }
        ]
    }
    if author:
        manifest["metadata"] = {"authors": [author]}
    if dependencies:
        manifest["dependencies"] = dependencies
    return json.dumps(manifest, indent=4)


def main():
    project_name = input("Enter the project name: ")
    bp_description = f"Behavior Pack for {project_name}"
    rp_description = f"Resource Pack for {project_name}"
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
            "font": {},
            "models": {"entity": {}},
            "particles": {},
            "render_controllers": {},
            "sounds": {},
            "textures": {},
            "ui": {}
        }
    }
    create_folder_structure(
        folder_structure, Path(destination_folder))

    BP_en_US_lang = "pack.name={} BP\npack.description={}".format(
        project_name, bp_description)
    RP_en_US_lang = "pack.name={} RP\npack.description={}".format(
        project_name, rp_description)

    file_structure = {
        "BP": {
            "entities": {},
            "functions": {"tick.json": "{}"},
            "loot_tables": {"empty.json": "{}"},
            "manifest.json": generate_manifest(project_name, BP_en_US_lang, author, "data", bp_uuid,
                                               [{"uuid": rp_uuid, "version": [1, 0, 0]}]),
            "texts": {
                "en_US.lang": BP_en_US_lang,
                "languages.json": '["en_US"]'
            }
        },
        "RP": {
            "biomes_client.json": "{}",
            "blocks.json": "{}",
            "font": {},
            "manifest.json": generate_manifest(project_name, RP_en_US_lang, author, "resources", rp_uuid,
                                               [{"uuid": bp_uuid, "version": [1, 0, 0]}]),
            "texts": {
                "en_US.lang": RP_en_US_lang,
                "languages.json": '["en_US"]'
            },
            "textures": {
                "flipbook_textures.json": "{}",
                "item_texture.json": "{}",
                "terrain_texture.json": "{}"
            }
        }
    }
    create_file_structure(file_structure, Path(destination_folder))


if __name__ == "__main__":
    main()
