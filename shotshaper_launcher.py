"""
Basic GUI for launching the Shotshaper script with selected files
This launcher uses a new script called disc_comp.py, which is a combination of two origional scripts
and modified to allow multiple disc throws to be overlaid and compare the results.

This launcher developed by Chris Egan in support of Trash Panda Disc Golf
chris.egan@ceganconsulting.com
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess

class ShotshaperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shotshaper Launcher")
        self.geometry("600x600")  # Adjust the size as needed
        
        # Define the initial directory
        self.initial_directory = os.path.join(os.getcwd(), "shotshaper", "discs")
        
        self.create_notebook()
        #self.create_widgets()
        self.populate_file_listbox(self.initial_directory)  # Populate listbox with files from the initial directory

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", pady=(10, 5))

        # Setup tab
        self.setup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.setup_tab, text="Setup")

        # Comparison Script tab
        self.comparison_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_tab, text="Comparison Script")

        # Original Script tab
        self.original_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.original_tab, text="Original disc_gui2d.py")

        # Coefficient Explorer tab
        self.coefficient_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.coefficient_tab, text="Coefficient Explorer")

        # Call separate methods to populate each tab with widgets
        self.create_setup_tab_widgets()
        self.create_comparison_tab_widgets()
        self.create_original_tab_widgets()
        self.create_coeffs_tab_widgets()
        # For Coefficient Explorer, you can add widgets similarly

        # File Listbox (common for all tabs)
        self.file_listbox = tk.Listbox(self, selectmode='multiple', exportselection=0)
        self.file_listbox.pack(pady=(5, 10), fill=tk.BOTH, expand=True)
        
    def create_setup_tab_widgets(self):
        # Select Folder Button
        self.select_folder_button = tk.Button(self.setup_tab, text="Select Alternate Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)
        
        # Unit selection checkbox
        self.unit_var = tk.BooleanVar()
        self.unit_checkbox = tk.Checkbutton(self.setup_tab, text="Use Metric Units", variable=self.unit_var)
        self.unit_checkbox.pack(pady=5)
        
        self.notes_text = tk.Text(self.setup_tab, height=5)
        self.notes_text.pack(pady=10)
        self.notes_text.insert("1.0", "Change folders if you've configured your install differently\n")
        self.notes_text.insert("2.0", "Use checkbox to use Metric units, leave unchecked for Imerial\n")

    def create_comparison_tab_widgets(self):
        # Add widgets specific to the Comparison Script tab
        self.launch_comparison_button = tk.Button(self.comparison_tab, text="Launch Comparison Script", command=self.launch_disc_comp)
        self.launch_comparison_button.pack(pady=10)
        
        # Text notes (example)
        self.notes_text = tk.Text(self.comparison_tab, height=5)
        self.notes_text.pack(pady=10)
        self.notes_text.insert("1.0", "This script allows you to compare up to 6 discs at once\n")
        self.notes_text.insert("2.0", "Select the discs from the list and click the button to launch the script\n")
        #self.notes_text.insert("3.0", "Up to 6 discs may be selected at once\n")

    def create_original_tab_widgets(self):
        # Add widgets specific to the Original Script tab
        self.launch_original_button = tk.Button(self.original_tab, text="Launch Original Script", command=self.launch_disc_gui2d)
        self.launch_original_button.pack(pady=10)
        
        self.notes_text = tk.Text(self.original_tab, height=5)
        self.notes_text.pack(pady=10)
        self.notes_text.insert("1.0", "This is the original disc_gui2d script\n")
        self.notes_text.insert("2.0", "Select a single disc from the list and launch the script\n")
        
    def create_coeffs_tab_widgets(self):
        # Add widgets specific to the Coefficient Explorer tab
        self.launch_coeffs_button = tk.Button(self.coefficient_tab, text="Launch Coefficients Script", command=self.launch_coeffs)
        self.launch_coeffs_button.pack(pady=10)
        
        self.notes_text = tk.Text(self.coefficient_tab, height=5)
        self.notes_text.pack(pady=10)
        self.notes_text.insert("1.0", "This script allows you to explore the coefficients of up to 6 discs\n")
        self.notes_text.insert("2.0", "Select discs from the list and launch the script\n")
    

    def launch_disc_comp(self):
        selected_indices = self.file_listbox.curselection()
        
        # Check if exactly one disc is selected
        if len(selected_indices) > 6:
            messagebox.showwarning("Warning", "Please select no more than 6 discs.")
            return
        
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
    
    def launch_disc_gui2d(self):
        selected_indices = self.file_listbox.curselection()
        
        # Check if exactly one disc is selected
        if len(selected_indices) != 1:
            messagebox.showwarning("Warning", "Please select exactly one disc.")
            return
        
        # Strip the .yaml extension from each selected file
        selected_file = self.file_listbox.get(selected_indices[0]).rsplit('.', 1)[0]
        
        # Determine the unit option based on the checkbox state
        unit_option = "metric" if self.unit_var.get() else "imperial"

        # Construct the command to run the script with selected files without their extensions
        command = ["python", "disc_gui2d.py", "--units", unit_option, selected_file]

        try:
            # Execute the command
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Shotshaper closed")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to launch Shotshaper: {e}")
    
    def launch_coeffs(self):
        selected_indices = self.file_listbox.curselection()
        
        # Check if exactly one disc is selected
        if len(selected_indices) > 6:
            messagebox.showwarning("Warning", "Please select no more than 6 discs.")
            return
        
        # Strip the .yaml extension from each selected file
        selected_files = [self.file_listbox.get(i).rsplit('.', 1)[0] for i in selected_indices]
        
        # Determine the unit option based on the checkbox state
        unit_option = "metric" if self.unit_var.get() else "imperial"

        # Construct the command to run the script with selected files without their extensions
        command = ["python", "coeffs.py", "--units", unit_option] + selected_files

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
