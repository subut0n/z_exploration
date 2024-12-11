import os
from datetime import datetime

def explore_directory(directory, exclude_list, contain_list):
    output_file = f"z_exploration/{os.path.basename(directory)}_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"
    explored_files = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            file_path = os.path.join(root, file)

            if any(file_path.endswith(ext) for ext in exclude_list):
                continue

            if contain_list and not any(pattern in file for pattern in contain_list):
                continue

            with open(file_path, "r") as f:
                content = f.read()

            with open(output_file, "a") as f:
                f.write(f"{os.path.relpath(file_path, directory)}\n")
                f.write(content + "\n\n")
                f.write("-" * 20 + "\n\n")

            explored_files.append(file_path)

    return output_file if explored_files else None
