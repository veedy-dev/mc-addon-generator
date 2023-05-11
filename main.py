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


def generate_manifest(name, description, author, type_pack, dependencies=None):
    manifest = {
        "format_version": 2,
        "header": {
            "description": description,
            "name": name,
            "uuid": str(uuid.uuid4()),
            "version": [1, 0, 0],
            "min_engine_version": [1, 16, 0]
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

    en_US_lang = "pack.name={}\npack.description={}".format(
        project_name, bp_description)

    file_structure = {
        "BP": {
            "entities": {},
            "functions": {"tick.json": "{}"},
            "loot_tables": {"empty.json": "{}"},
            "manifest.json": generate_manifest(project_name, bp_description, author, "data", [{"uuid": rp_uuid, "version": [1, 0, 0]}]),
            "texts": {
                "en_US.lang": en_US_lang,
                "languages.json": '{"en_US": "English (US)"}'
            }
        },
        "RP": {
            "biomes_client.json": "{}",
            "blocks.json": "{}",
            "font": {},
            "manifest.json": generate_manifest(project_name, bp_description, author, "resources", [{"uuid": rp_uuid, "version": [1, 0, 0]}]),
            "texts": {
                "en_US.lang": en_US_lang,
                "languages.json": '{"en_US": "English (US)"}'
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
