import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from FolderSync import FolderSync


def create_synced_folder(directory=None, syncfolder=None):
    if directory is None:
        directory = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    folder_name = 'Synced_Folder_' + syncfolder
    folder_path = os.path.join(directory, folder_name)


    os.makedirs(folder_path)

    print(f"Directory '{folder_name}' created successfully in '{directory}'.")

    state_folder = os.path.join(folder_path, 'SyncedState')
    os.makedirs(state_folder)

    return folder_path



def create_(folder):

    root = tk.Tk()
    root.withdraw()

    window = tk.Toplevel(root)
    window.title('Create Synced Folder')

    label = tk.Label(window, text=f"Do you want to use the default directory to create a synced folder for '{folder}'?")
    label.pack(pady=10)

    choice_var = tk.StringVar()

    yes_button = tk.Button(window, text=f"Yes", command=lambda: set_choice("yes"))
    yes_button.pack(side=tk.RIGHT, padx=10)

    no_button = tk.Button(window, text="No", command=lambda: set_choice("no"))
    no_button.pack(side=tk.RIGHT, padx= 10)

    def set_choice(choice):
        choice_var.set(choice)
        window.destroy()

    print(choice_var.get())
    
    window.wait_window()
        
    user_choice = choice_var.get()

    if user_choice == "yes":
        return create_synced_folder(None, folder)
    elif user_choice == "no":
        custom_path = filedialog.askdirectory("Select a directory")
        if custom_path:
            return create_synced_folder(custom_path, folder)
        else:
            print("You have to select a path!")



def check_for_synced(folder_path, folder_name):
    
    root = tk.Tk()
    root.withdraw()

    window = tk.Toplevel(root)
    window.title('Create Synced Folder')

    label = tk.Label(window, text=f"Does the '{folder_name}' folder already have a Synced Folder Associated?")
    label.pack(pady=10)

    choice_var = tk.StringVar()

    yes_button = tk.Button(window, text=f"Yes", command=lambda: set_choice("yes"))
    yes_button.pack(side=tk.RIGHT, padx=10)

    no_button = tk.Button(window, text="No", command=lambda: set_choice('no'))
    no_button.pack(side=tk.RIGHT, padx= 10)

    def set_choice(choice):
        choice_var.set(choice)
        window.destroy()
    
    window.wait_window()

    user_choice = choice_var.get()

    if user_choice == "yes":
        syncFolder = select_sync_folder(folder_name)
        if syncFolder:
            FolderSync(folder_path, syncFolder)
    elif user_choice == "no":
        newSyncFolder = create_(folder_name)
        if newSyncFolder:
            FolderSync(folder_path, newSyncFolder)
    


def select_sync_folder(folder):
     folder_selected = filedialog.askdirectory(title='Select your Folder: ')

     if folder_selected and folder_selected.endswith('Synced_Folder_' + folder):
         return folder_selected
     else:
         messagebox.showerror("Error", "Invalid selection. Please select the correct Synced folder.")
         return None
