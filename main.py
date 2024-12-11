import tkinter as tk
from tkinter import filedialog, messagebox
from config import load_config, save_config
from explorer import explore_directory
from utils import copy_to_clipboard
import os

# Load configuration
config = load_config()

# Default values for directory, excludes, and contains
default_directory = config.get("default_directory", "")
default_excludes = config.get("default_excludes", [])
default_contains = config.get("default_contains", [])

# Main window
root = tk.Tk()
root.title("Directory Explorer")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))

# Interface variables
directory_var = tk.StringVar(value=default_directory)
exclude_var = tk.StringVar(value=",".join(default_excludes))
contain_var = tk.StringVar(value=",".join(default_contains))
last_output_file = tk.StringVar()

# Interactions
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)

def toggle_default_excludes():
    current_excludes = exclude_var.get().split(",")
    for ext in default_excludes:
        if ext in current_excludes:
            current_excludes.remove(ext)
        else:
            current_excludes.append(ext)
    exclude_var.set(",".join(current_excludes))

def generate_output():
    directory = directory_var.get()
    exclude_list = [ext.strip() for ext in exclude_var.get().split(",") if ext.strip()]
    contain_list = [pattern.strip() for pattern in contain_var.get().split(",") if pattern.strip()]

    if not directory:
        messagebox.showerror("Error", "Please select a directory to explore.")
        return

    os.makedirs("z_exploration", exist_ok=True)
    output_file = explore_directory(directory, exclude_list, contain_list)

    if output_file:
        last_output_file.set(output_file)
        messagebox.showinfo("Success", f"Exploration completed. Results saved in {output_file}")
    else:
        messagebox.showinfo("No Files Found", "No files matched the criteria.")

    config["default_directory"] = directory
    config["default_excludes"] = exclude_list
    config["default_contains"] = contain_list
    save_config(config)

def clean_exploration_folder():
    folder = "z_exploration"
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting {file_path}: {e}")
        messagebox.showinfo("Success", f"The folder '{folder}' has been cleaned.")
    else:
        messagebox.showwarning("Warning", f"The folder '{folder}' does not exist.")

# User Interface
# Création d'un cadre central
frame = tk.Frame(root)
frame.pack(expand=True)  # Centrer le cadre dans la fenêtre

# Directory selection
tk.Label(frame, text="Directory to explore:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame, textvariable=directory_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

# Exclude patterns
tk.Label(frame, text="Exclude extensions (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame, textvariable=exclude_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame, text="Toggle Default Excludes", command=toggle_default_excludes).grid(row=1, column=2, padx=10, pady=5)

# Contain patterns
tk.Label(frame, text="Contain patterns (comma-separated):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(frame, textvariable=contain_var, width=50).grid(row=2, column=1, padx=10, pady=5)

# Action buttons
tk.Button(frame, text="Explore Directory", command=generate_output).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(last_output_file.get()), bg="blue").grid(row=3, column=2, padx=10, pady=10)

# Clean exploration folder
tk.Button(frame, text="Clean Folder", command=clean_exploration_folder, bg="red").grid(row=4, column=0, columnspan=3, pady=10)

# Start Application
root.mainloop()
