import os
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_test_folder(base_path):
    # Create a random folder name with hyphens and periods
    folder_name = f"{random_string(5)}-{random_string(3)}.{random_string(4)}"
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Create some random files with hyphens and periods in the names
    for _ in range(5):
        file_name = f"{random_string(4)}-{random_string(2)}.{random_string(3)}.txt"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as f:
            f.write("This is a test file.")

    return folder_path

# Specify the base path where you want to create the test folder
base_path = os.path.expanduser("~/Desktop")  # Change this to your desired location
test_folder = create_test_folder(base_path)
print(f"Test folder created at: {test_folder}")
