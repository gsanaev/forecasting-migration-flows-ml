import kagglehub
import os
import shutil



def _move_files(source_path: str, destination: str):
    """
    Moves files from the source path to the destination directory.
    Args:
        source_path (str): The path where the files are currently located.
        destination (str): The directory where the files will be moved.
    Returns:
        None
    """
    data_dir = os.path.join(os.getcwd(), destination)
    os.makedirs(data_dir, exist_ok=True)
    
    files = os.listdir(source_path)
    for file_name in files:
        full_file_name = os.path.join(source_path, file_name)
        if os.path.isfile(full_file_name):
            print(f"Moving file: {full_file_name} to {data_dir}")
            shutil.move(full_file_name, data_dir)
    
    print(f"Files moved to '{destination}' directory.")


def load_from_kaggle(dataset_link: str, destination: str = None):
    """
    Loads a dataset from Kaggle and moves it to the specified destination directory.
    Args:
        dataset_link (str): The Kaggle dataset link in the format 'username/dataset-name' 
        
        destination (str): The directory where the dataset will be saved. Defaults to the dataset name.
    Returns:
        None
    """
    path = kagglehub.dataset_download(dataset_link, force_download=True)
    if destination is None:
        destination = dataset_link.split("/")[-1]
    _move_files(path, destination)

