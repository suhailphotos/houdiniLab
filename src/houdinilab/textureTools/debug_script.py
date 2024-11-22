import hou
import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def rename_debug(source_folder):
    try:
        # Strip trailing slashes from the source folder
        source_folder = source_folder.rstrip('/\\')

        # Check if the source folder exists
        if not os.path.isdir(source_folder):
            logging.error(f"The specified folder does not exist: {source_folder}")
            return

        # Get the folder name and new folder name
        parent_folder = os.path.dirname(source_folder)
        folder_name = os.path.basename(source_folder)
        logging.info(f'folder_name: {folder_name}')
        new_folder_name = re.sub(r'[.\s-]', '_', folder_name)
        logging.info(new_folder_name)
        
        if not new_folder_name:
            logging.error("New folder name is empty.")
            return

        new_folder_path = os.path.join(parent_folder, new_folder_name)

        # Rename the folder
        try:
            if source_folder != new_folder_path:
                os.rename(source_folder, new_folder_path)
                logging.info(f"Renamed folder {source_folder} to {new_folder_path}")
                source_folder = new_folder_path
        except PermissionError:
            logging.error(f"Permission denied while renaming folder {source_folder} to {new_folder_path}")
            return
        except Exception as e:
            logging.error(f"Error renaming folder {source_folder} to {new_folder_path}: {e}")
            return

        # Rename the files in the folder
        try:
            for file in os.listdir(source_folder):
                file_path = os.path.join(source_folder, file)
                if os.path.isfile(file_path) and not file.startswith('.'):
                    file_name, file_ext = os.path.splitext(file)
                    new_file_name = re.sub(r'[.\s-]', '_', file_name) + file_ext
                    new_file_path = os.path.join(source_folder, new_file_name)
                    
                    if new_file_name == file:
                        continue
                    
                    try:
                        os.rename(file_path, new_file_path)
                        logging.info(f"Renamed file {file_path} to {new_file_path}")
                    except PermissionError:
                        logging.error(f"Permission denied while renaming file {file_path} to {new_file_path}")
                    except Exception as e:
                        logging.error(f"Error renaming file {file_path} to {new_file_path}: {e}")
        except PermissionError:
            logging.error(f"Permission denied while accessing folder {source_folder}")
        except Exception as e:
            logging.error(f"Error during renaming files in folder {source_folder}: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Prompt user to select the source folder
start_directory = hou.getenv('HIP')
title = 'Select root folder'
file_type = hou.fileType.Directory
source_folder = hou.ui.selectFile(start_directory=start_directory, title=title, file_type=file_type)

# Expand the selected folder path
source_folder = hou.text.expandString(source_folder) if source_folder else None

if source_folder:
    rename_debug(source_folder)
else:
    logging.info('No source folder selected. Operation cancelled.')
