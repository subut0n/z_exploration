import pyperclip
import os
from tkinter import messagebox

def copy_to_clipboard(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            pyperclip.copy(f.read())
        messagebox.showinfo("Copied", "The content of the file has been copied to the clipboard.")
    else:
        messagebox.showerror("Error", "The output file does not exist.")
