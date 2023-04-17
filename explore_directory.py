import os
import argparse
from datetime import datetime

def is_excluded(file_path, exclude_str):
    if file_path.endswith("go.mod") or file_path.endswith("go.sum") or "_test" in file_path or file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return True
    if exclude_str and exclude_str in file_path:
        return True
    if ".git" in file_path.split(os.path.sep):
        return True
    return False

def explore_directory(directory, output_file, exclude_str, contain_str):
    explored_files = []  # List of explored files
    contain_list = [] if not contain_str else contain_str.split(",")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')] # Ignore hidden directories (starting with a dot)
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if is_excluded(file_path, exclude_str):
                    continue
                if contain_list and not any(contain in file for contain in contain_list):
                    continue

                with open(output_file, "a") as output:
                    with open(file_path, "r") as file_content:
                        content = file_content.read()
                        output.write(f"{os.path.basename(root)}/{os.path.basename(file)}\n")
                        output.write(content + "\n\n")
                    output.write("--------------------\n\n")

                explored_files.append(file_path)  # Add the explored file to the list
            except Exception as e:
                print(f"Error while processing file {file_path}: {e}")
                continue

    # Print the list of explored files
    print("Explored files:")
    for file_path in explored_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explore a directory and generate a .txt file with the directory's structure and the contents of its files.")
    parser.add_argument("-n", "--directory_name", type=str, required=True, help="The name of the directory to explore")
    parser.add_argument("-e", "--exclude", type=str, required=False, help="String to exclude from file names")
    parser.add_argument("-c", "--contain", type=str, required=False, help="Comma-separated list of strings to search in file names")

    args = parser.parse_args()
    directory_to_explore = args.directory_name
    exclude_str = args.exclude
    contain_str = args.contain

    # Create the "z_exploration" directory if it doesn't exist
    os.makedirs("z_exploration", exist_ok=True)

    # Generate the output file name with the specified format
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"z_exploration/{os.path.basename(directory_to_explore)}_{current_time}.txt"

    with open(output_file, "w") as f:
        f.write("")

    explore_directory(directory_to_explore, output_file, exclude_str, contain_str)




