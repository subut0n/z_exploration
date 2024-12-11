import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import json
import pyperclip  # To handle clipboard copying

# Configuration file to save default settings
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"default_directory": "", "default_excludes": [], "default_contains": []}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def is_excluded(file_path, exclude_list):
    if exclude_list and any(file_path.endswith(excl) for excl in exclude_list):
        return True
    return False

def explore_directory(directory, output_file, exclude_list, contain_list):
    explored_files = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            file_path = os.path.join(root, file)

            if is_excluded(file_path, exclude_list):
                continue

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

    return explored_files

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)

def generate_output():
    directory = directory_var.get()
    exclude_list = [ext.strip() for ext in exclude_var.get().split(",") if ext.strip()]
    contain_list = [pattern.strip() for pattern in contain_var.get().split(",") if pattern.strip()]

    if not directory:
        messagebox.showerror("Error", "Please select a directory to explore.")
        return

    os.makedirs("z_exploration", exist_ok=True)
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"z_exploration/{os.path.basename(directory)}_{current_time}.txt"

    with open(output_file, "w") as f:
        pass

    explored_files = explore_directory(directory, output_file, exclude_list, contain_list)

    if explored_files:
        # Save the path to the last output file
        last_output_file.set(output_file)
        file_list = "\n".join([f"- \033[1;33m{os.path.basename(file)}\033[0m" for file in explored_files])
        messagebox.showinfo("Success", f"Exploration completed. Results saved in {output_file}\n\nFiles explored:\n{file_list}")
    else:
        messagebox.showinfo("No Files Found", "No files matched the criteria.")

    # Save the current settings to the config file
    config["default_directory"] = directory
    config["default_excludes"] = exclude_list
    config["default_contains"] = contain_list
    save_config(config)

def toggle_default_excludes():
    current_excludes = exclude_var.get().split(",")
    for ext in default_excludes:
        if ext in current_excludes:
            current_excludes.remove(ext)
        else:
            current_excludes.append(ext)
    exclude_var.set(",".join(current_excludes))

def copy_to_clipboard():
    output_file = last_output_file.get()

    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            pyperclip.copy(f.read())
        messagebox.showinfo("Copied", "The content of the file has been copied to the clipboard.")
    else:
        messagebox.showerror("Error", "The output file does not exist. Please generate the output first.")

# Load saved configuration
config = load_config()

default_directory = config.get("default_directory", "")
default_excludes = config.get("default_excludes", [])
default_contains = config.get("default_contains", [])

# Create the GUI
root = tk.Tk()
root.title("Directory Explorer")

# Variable to track the last output file
last_output_file = tk.StringVar()

# Directory selection
tk.Label(root, text="Directory to explore:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
directory_var = tk.StringVar(value=default_directory)
tk.Entry(root, textvariable=directory_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

# Exclude patterns
tk.Label(root, text="Exclude extensions (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
exclude_var = tk.StringVar(value=",".join(default_excludes))
tk.Entry(root, textvariable=exclude_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Toggle Default Excludes", command=toggle_default_excludes).grid(row=1, column=2, padx=10, pady=5)

# Contain patterns
tk.Label(root, text="Contain patterns (comma-separated):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
contain_var = tk.StringVar(value=",".join(default_contains))
tk.Entry(root, textvariable=contain_var, width=50).grid(row=2, column=1, padx=10, pady=5)

# Run button
tk.Button(root, text="Explore Directory", command=generate_output).grid(row=3, column=0, columnspan=2, pady=10)

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="blue", fg="white").grid(row=3, column=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
