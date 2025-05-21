# pythonrc.py
import os
import sys
import glob

def add_poetry_site_packages(project_env="houdinilab"):
    """
    Locate the Poetry virtualenv for `project_env`, find its
    site-packages directory, and insert it at the front of sys.path.
    """
    home = os.path.expanduser("~")
    # macOS Poetry cache location; adjust if you’ve set POETRY_CACHE_DIR elsewhere
    venvs_dir = os.path.join(home, "Library", "Caches", "pypoetry", "virtualenvs")
    
    # match folders like "houdinilab-<hash>-py3.11"
    pyver = f"{sys.version_info.major}.{sys.version_info.minor}"
    pattern = os.path.join(venvs_dir, f"{project_env}-*-py{pyver}")
    matches = glob.glob(pattern)
    if not matches:
        print(f"[pythonrc] no Poetry venv matching {pattern!r}")
        return
    
    # pick the most recently modified (in case there are old envs)
    venv_path = sorted(matches, key=os.path.getmtime, reverse=True)[0]
    site_pkgs = os.path.join(venv_path, "lib", f"python{pyver}", "site-packages")
    
    if os.path.isdir(site_pkgs):
        if site_pkgs not in sys.path:
            sys.path.insert(0, site_pkgs)
            print(f"[pythonrc] added site-packages: {site_pkgs}")
    else:
        print(f"[pythonrc] expected site-packages not found at {site_pkgs!r}")

# run it
add_poetry_site_packages()
