import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import logging

class Synced_Folder:

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self):
        self._path = ''
        self._name = os.path.basename(self.path)


    def create_synced_folder(self, directory, original_folder_path):
        while True:
            if directory is None:
                directory = os.path.join(os.path.expanduser('~'), 'Desktop')
        
            if os.path.exists(directory):
                os.makedirs(directory)
            else:
                messagebox.showerror('Error', 'You must specify a directory')
                logging.error('You must specify a directory')
                directory = self.select_directory()
                if not directory:
                    return

            if 'Synced_Folder_' in directory:
                messagebox.showerror('Error', 'You cannot create a Synced Folder inside a Synced Folder')
                directory = self.select_directory()
                if not directory:
                    return
            else:
                break
        
        folder_name = 'Synced_Folder_' + os.path.basename(original_folder_path)
        self.path = os.path.join(directory, folder_name)
        os.makedirs(self.path)

        state_folder = os.path.join(self.path, 'SyncedState')
        os.makedirs(state_folder)



    def select_sync_folder(self):
        while True:
            folder_selected = filedialog.askdirectory(title='Select your Synced Folder: ')

            if not folder_selected:
                messagebox.showinfo('Info', 'Operation canceled.')
                #method to previous operation

            if folder_selected.endswith('Synced_Folder_' + os.path.basename(self.path)):
                return folder_selected
            else:
                messagebox.showerror('Error', "Invalid Selection. Please select the correct Synced Folder or click return.")
        

    def select_directory(self, original_folder_path):
        while True:    
            if user_choice == 'yes':
                self.create_synced_folder(None, None)
            elif user_choice == 'no':
                custom_path = filedialog.askdirectory("Select the directory where you want your Synced Folder to be created in:")
                if custom_path:
                    self.create_synced_folder(custom_path, original_folder_path)
                else:
                    messagebox.showerror("You have to select either a custom or the default directory!")
            elif user_choice == 'cancel':
                shutil.rmt(0)

    @property
    def path(self):
        return self._path
    
    @property
    def name(self):
        return self._name

    @path.setter
    def path(self, value):
        self._path = value


