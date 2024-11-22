import os
import re
import platform

def get_houdini_versions(base_dir, pattern):
    versions = []
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            match = re.match(pattern, item)
            if match:
                versions.append(match.group(1))
    return versions

def get_latest_houdini_version(base_dir, pattern):
    versions = get_houdini_versions(base_dir, pattern)
    if versions:
        return max(versions, key=lambda v: list(map(int, v.split('.'))))
    return None

def get_current_houdini_version(base_dir, pattern):
    current_path = os.path.join(base_dir, 'Current')
    if os.path.islink(current_path):
        actual_path = os.readlink(current_path)
        version = os.path.basename(actual_path)
        match = re.match(pattern, version)
        if match:
            return match.group(1)
    return None

def main():
    system = platform.system()
    if system == "Windows":
        base_dir = "C:\\Program Files\\Side Effects Software"
        pattern = r'Houdini (\d+\.\d+)\.\d+'
        check_current = False
    elif system == "Darwin":
        base_dir = "/Applications/Houdini"
        pattern = r'Houdini(\d+\.\d+)\.\d+'
        check_current = True
    else:
        print("Unsupported operating system.")
        return

    latest_version = get_latest_houdini_version(base_dir, pattern)

    if latest_version:
        print(f"The latest installed major version of Houdini is: {latest_version}")
    else:
        print("No Houdini versions found.")

    if check_current:
        current_version = get_current_houdini_version(base_dir, pattern)
        if current_version:
            print(f"The current major version of Houdini is: {current_version}")
        else:
            print("No current Houdini version found.")

if __name__ == "__main__":
    main()
