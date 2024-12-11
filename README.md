# README

## Overview

This script explores a given directory, filters files based on specified criteria, and consolidates their contents into a timestamped text file inside the `z_exploration` directory. Each run creates a unique output file that lists and includes the contents of all matching files.

After generating the result file, the make targets allow copying its contents directly to the clipboard, depending on the operating system (macOS or Ubuntu).

## How It Works

1. The main script is `explore_directory.py`. It:
   - Recursively traverses the specified directory.
   - Applies optional exclusion patterns (`-e`) and optional name-containment filters (`-c`).
   - Produces a timestamped text file in `z_exploration` with the paths and contents of the matched files.
   - Inserts a separator (`--------------------`) between each listed file.

2. The provided `Makefile` simplifies running the script and copying the results. There are two primary targets:
   - `make cp`: For macOS.
   - `make cpy`: For Ubuntu.

   These targets:
   - Prompt the user for the directory path, exclude patterns, and contain patterns.
   - Execute the Python script with the provided parameters.
   - Find the most recently generated file in `z_exploration` and copy its contents to the clipboard.

3. The `make clean` target removes all files in `z_exploration`.

## Parameters

- `-n, --directory_name`: Required. The path of the directory to explore.
- `-e, --exclude`: Optional. A comma-separated list of patterns. Any file whose path includes one of these patterns is ignored.
- `-c, --contain`: Optional. A comma-separated list of patterns. Only files whose names contain at least one of these patterns will be included.
