# Directory Explorer

This script allows you to explore a directory and generate a .txt file with the directory's structure and the contents of its files. It excludes specific files and directories, and searches for specific strings in file names.

## Prerequisites
- Python 3.x

## Usage
To use the script, run the following command in the terminal:

```python explore_directory.py -n <directory_name> -e <exclude_string> -c <contain_string>```

- `directory_name`: The name of the directory to explore (required)
- `exclude_string`: String to exclude from file names (optional)
- `contain_string`: Comma-separated list of strings to search in file names (optional)

The script will generate a timestamped .txt file in the `z_exploration` directory. The file will contain the directory's structure and the contents of its files.

## Makefile
- `clean`: Removes all .txt files in the `z_exploration` directory
- `regen`: Cleans the directory and explores the specified directory with the specified exclude and contain strings
- `copy`: Copies the contents of the most recently generated .txt file to the clipboard

## Notes
- The script excludes specific files and directories by default. You can add additional exclusions in the `is_excluded` function.
- The script ignores hidden directories (starting with a dot).
