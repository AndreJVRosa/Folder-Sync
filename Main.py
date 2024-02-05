from SelectFolder import OriginalFolder
from NewFolder import check_for_synced

select_folder = OriginalFolder()

select_folder.select_path()

folder = select_folder.get_folder_path()

folderName = select_folder.get_folder_name()

check_for_synced(folder, folderName)