"""
Basic GUI for launching the Shotshaper script with selected files
This launcher uses a new script called disc_comp.py, which is a combination of two origional scripts
and modified to allow multiple disc throws to be overlaid and compare the results.

This launcher developed by Chris Egan in support of Trash Panda Disc Golf
chris.egan@ceganconsulting.com
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os  # Import the os module
import subprocess  # Import the subprocess module

class ShotshaperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shotshaper Launcher")
        self.geometry("400x600")  # Adjust the size as needed
        
        # Define the initial directory
        self.initial_directory = os.path.join(os.getcwd(), "shotshaper", "discs")
        self.create_widgets()
        self.populate_file_listbox(self.initial_directory)  # Populate listbox with files from the initial directory


    def create_widgets(self):
        # Launch Button
        self.launch_button = tk.Button(self, text="Launch Shotshaper", command=self.launch_shotshaper)
        self.launch_button.pack(pady=10)

        # Select Folder Button
        self.select_folder_button = tk.Button(self, text="Select Alternate Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)
        
        # Unit selection checkbox
        self.unit_var = tk.BooleanVar()
        self.unit_checkbox = tk.Checkbutton(self, text="Use Metric Units", variable=self.unit_var)
        self.unit_checkbox.pack(pady=5)

        # File Listbox
        self.file_listbox = tk.Listbox(self, selectmode='multiple', exportselection=0)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def launch_shotshaper(self):
        selected_indices = self.file_listbox.curselection()
        # Strip the .yaml extension from each selected file
        selected_files = [self.file_listbox.get(i).rsplit('.', 1)[0] for i in selected_indices]
        
        # Determine the unit option based on the checkbox state
        unit_option = "metric" if self.unit_var.get() else "imperial"

        # Construct the command to run the script with selected files without their extensions
        command = ["python", "disc_comp.py", "--units", unit_option] + selected_files

        try:
            # Execute the command
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Shotshaper closed")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to launch Shotshaper: {e}")

    def select_folder(self):
        initial_dir = os.getcwd()  # Get the current working directory
        folder_path = filedialog.askdirectory(initialdir=initial_dir)  # Open the dialog in the current working directory
        if folder_path:
            self.populate_file_listbox(folder_path)

    def populate_file_listbox(self, folder_path):
        self.file_listbox.delete(0, tk.END)  # Clear the listbox

        # List all files in the directory and filter for .yaml files
        for file in os.listdir(folder_path):
            if file.endswith(".yaml"):
                self.file_listbox.insert(tk.END, file)

if __name__ == "__main__":
    app = ShotshaperGUI()
    app.mainloop()
