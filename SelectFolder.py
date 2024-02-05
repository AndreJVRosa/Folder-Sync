from os.path import basename
import tkinter.messagebox as messagebox
from tkinter import filedialog

class OriginalFolder:
    
    def __init__(self):
        self._path = ''
        self._name = ''

    def select_path(self):
        while True:
            folder_selected = filedialog.askdirectory(title='Select your Folder: ')

            if folder_selected:
                self.path = folder_selected
                self.name = basename(self.path)
            else:
                messagebox.showerror('You must select a folder')
            
    
    @property
    def name(self):
        return self._name
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value

    @name.setter
    def name(self, value):
        self._name = value
    