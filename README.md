# Minecraft Bedrock Addon Generator

This Python script automates the creation of a Minecraft addon project structure, including both Behavior Pack (BP) and Resource Pack (RP). It allows customization of the project name, author, and version, and optionally includes support for the Minecraft Scripting API.

## Features

- Generates folder structures for both BP and RP.
- Creates essential files like `manifest.json`, language files, and optionally `main.js` for scripting.
- Customizable project name, author, and minimum engine version.
- Option to include Scripting API support with user-defined versions for `@minecraft/server` and `@minecraft/server-ui`.

## Prerequisites

- Python 3.x
- Basic knowledge of terminal or command prompt usage.

## Usage

1. **Run the Script**: Execute the script by running `python main.py` in your terminal or command prompt.
   
2. **Input Project Details**: You'll be prompted to enter:
   - The project name.
   - The minimum engine version (default: 1.20.50).
   - The author's name (optional).
   - The destination folder for the generated project (default: current folder).

3. **Scripting API Option**: If asked whether to use the Scripting API, enter `y` for yes or `n` for no. If yes:
   - Enter the desired versions for `@minecraft/server` and `@minecraft/server-ui`.
   - The script will generate a `scripts` folder with a `main.js` file in the BP directory.

4. **Check the Output**: After completion, check the specified destination folder for the generated BP and RP structures.

## Output Structure

- **Behavior Pack (BP)**
  - `animations`, `animation_controllers`, `entities`, `functions`, `items`, `loot_tables`, `recipes`, `texts`, `spawn_rules`.
  - `scripts` folder with `main.js` (if Scripting API is used).
  - `manifest.json` and language files.
  
- **Resource Pack (RP)**
  - `animations`, `animation_controllers`, `entity`, `items`, `font`, `models`, `particles`, `render_controllers`, `sounds`, `textures`, `ui`.
  - `sound_definitions.json` and `sounds.json`.
  - `manifest.json` and language files.

## Running with Batch or Shell Scripts

- **Windows**: Use `run.bat` to execute the script.
- **Unix/Linux**: Use `run.sh` for script execution.

## Notes

- Ensure you have the necessary permissions in the destination directory.
- Test the generated packs in a controlled environment before deploying.
