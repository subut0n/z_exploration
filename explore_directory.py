import os
import argparse
from datetime import datetime

def is_excluded(file_path, exclude_list):
    # Exclude a file if any of the exclude patterns are present in its path
    if exclude_list and any(excl in file_path for excl in exclude_list):
        return True
    return False

def explore_directory(directory, output_file, exclude_str, contain_str):
    explored_files = []
    exclude_list = [] if not exclude_str else exclude_str.split(",")
    contain_list = [] if not contain_str else contain_str.split(",")

    for root, dirs, files in os.walk(directory):
        # Ignore hidden directories (starting with a dot)
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            file_path = os.path.join(root, file)

            # Check if file should be excluded
            if is_excluded(file_path, exclude_list):
                continue

            # If contain_list is not empty, ensure the file name contains at least one pattern
            if contain_list and not any(c in file for c in contain_list):
                continue

            try:
                with open(file_path, "r") as file_content:
                    content = file_content.read()
                with open(output_file, "a") as output:
                    output.write(f"{os.path.basename(root)}/{os.path.basename(file)}\n")
                    output.write(content + "\n\n")
                    output.write("--------------------\n\n")

                explored_files.append(file_path)
            except Exception as e:
                print(f"Error while processing file {file_path}: {e}")
                continue

    print("Explored files:")
    for file_path in explored_files:
        print(f"- {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explore a directory and generate a .txt file with the structure and contents of its files.")
    parser.add_argument("-n", "--directory_name", type=str, required=True, help="The name of the directory to explore")
    parser.add_argument("-e", "--exclude", type=str, required=False, help="Comma-separated list of strings to exclude from file paths")
    parser.add_argument("-c", "--contain", type=str, required=False, help="Comma-separated list of strings required in file names")

    args = parser.parse_args()
    directory_to_explore = args.directory_name
    exclude_str = args.exclude
    contain_str = args.contain

    os.makedirs("z_exploration", exist_ok=True)

    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"z_exploration/{os.path.basename(directory_to_explore)}_{current_time}.txt"

    with open(output_file, "w") as f:
        pass

    explore_directory(directory_to_explore, output_file, exclude_str, contain_str)
    print(f"Exploration completed. Results saved in {output_file}")





