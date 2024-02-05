import os
import shutil
import filecmp
import hashlib
import json
import logging

class FolderSync:

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, original_folder_path, synced_folder_path):
        
        self.original_folder_path = original_folder_path
        self.synced_folder_path = synced_folder_path

        self.state_folder = os.path.join(self.synced_folder_path, "SyncedState")

        self.setup(self.original_folder_path, self.synced_folder_path)
    
    def setup(self, original_folder_path, synced_folder_path):
        self.saved_state = self.load_state()
        self.current_state = {}

        self.copy(original_folder_path, synced_folder_path)
        self.delete(original_folder_path, synced_folder_path)
        self.subdir_check(original_folder_path, synced_folder_path)

        self.save_state(original_folder_path)

    def copy(self, original_folder_path, synced_folder_path):
        dircmp = filecmp.dircmp(original_folder_path, synced_folder_path)

        for file_name in dircmp.left_only + dircmp.diff_files:
            original_file_path = os.path.join(original_folder_path, file_name)
            synced_file_path = os.path.join(synced_folder_path, file_name)

            self.current_state[file_name] = self.hash_file(original_file_path)

            logging.debug(f"Original Folder: {original_folder_path}\n"
              f"Original File Path: {original_file_path}\n"
              f"Synced Folder: {synced_folder_path}\n"
              f"Synced File Path: {synced_file_path}\n"
              f"Left Dircmp: {dircmp.left_only}\n"
              f"File Name: {file_name}\n"
              f"Current State: {str(self.current_state)}")


            try:
                if os.path.isdir(original_file_path):
                    logging.debug(f"Creating directory: {synced_file_path}")
                    os.makedirs(synced_file_path, exist_ok=True)
                    self.copy(original_file_path, synced_file_path)
                
                elif file_name not in self.saved_state or self.saved_state[file_name] != self.current_state[file_name]:
                    shutil.copy2(original_file_path, synced_file_path)

                    #Temp
                    logging.debug(f"File '{file_name}' copied/updated")

            except Exception as e:
                logging.error(f"Error syncing file '{file_name}': '{e}'")

    def delete(self, original_folder_path, synced_folder_path):
        dircmp = filecmp.dircmp(original_folder_path, synced_folder_path)

        for file_name in dircmp.right_only:
            synced_file_path = os.path.join(synced_folder_path, file_name)

            if os.path.isdir(synced_file_path) and file_name == "SyncedState":
                continue

            if file_name not in self.saved_state:
                if os.path.exists(synced_file_path):
                    try:
                        if os.path.isdir(synced_file_path):
                            shutil.rmtree(synced_file_path)

                            logging.debug(f"File '{file_name}' deleted from synced folder")
                        
                        else:
                            os.remove(synced_file_path)

                            #Temp
                            logging.debug(f"File '{file_name}' deleted from synced folder")
                    
                    except PermissionError as e:
                        logging.error(f"PermissionError deleting file '{file_name}': {e}")

                    except FileNotFoundError:
                        logging.error(f"File '{file_name}' not found in synced folder")

                    except Exception as e:
                        logging.error(f"Error deleting file '{file_name}': {e}")
                
                else:
                    logging.debug(f"File '{file_name}' not found in synced folder")

    def subdir_check(self, original_folder_path, synced_folder_path):
        dircmp = filecmp.dircmp(original_folder_path, synced_folder_path)

        for sub_dir in dircmp.common_dirs:
            original_sub_dir = os.path.join(original_folder_path, sub_dir)
            synced_sub_dir = os.path.join(synced_folder_path, sub_dir)
            self.setup(original_sub_dir, synced_sub_dir)

    def save_state(self, original_folder_path):
        state = {}

        for root, dirs, files in os.walk(original_folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, original_folder_path)
                state[relative_path] = self.hash_file(file_path)

        os.makedirs(self.state_folder, exist_ok=True)

        state_file = os.path.join(self.state_folder, 'sync_state.json')

        with open(state_file, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        state_file = os.path.join(self.state_folder, 'sync_state.json')

        try:
            with open(state_file) as f:
                return json.load(f)
        
        except FileNotFoundError:
            return {}
        
    def hash_file(self, file_path):
        if os.path.isdir(file_path):
            file_hashes = []

            for root, dirs, files in os.walk(file_path):
                print(f"Root: {root}")
                print(f"Dirs: {dirs}")
                print(f"Files: {files}")

                for file_name in files:
                    relative_path = os.path.relpath(os.path.join(root, file_name), file_path)
                    file_hashes.append(self.hash_file(os.path.join(file_path, relative_path)))

            return hashlib.md5(str(file_hashes).encode()).hexdigest()
        
        else:
            relative_path = os.path.relpath(file_path, self.original_folder_path)
            hasher = hashlib.md5()

            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b''):
                    hasher.update(chunk)
                
            hasher.update(str(relative_path).encode())
            
            return hasher.hexdigest()