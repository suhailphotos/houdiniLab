# pythonrc.py
import os
import sys
import glob
import json


def add_poetry_site_packages(project_env="houdinilab"):
    """
    Locate the Poetry virtualenv for `project_env`, find its
    site-packages directory, and insert it at the front of sys.path.
    """
    home = os.path.expanduser("~")
    venvs_dir = os.path.join(home, "Library", "Caches", "pypoetry", "virtualenvs")
    pyver = f"{sys.version_info.major}.{sys.version_info.minor}"
    pattern = os.path.join(venvs_dir, f"{project_env}-*-py{pyver}")
    matches = glob.glob(pattern)
    if not matches:
        print(f"[pythonrc] no Poetry venv matching {pattern!r}")
        return

    venv_path = sorted(matches, key=os.path.getmtime, reverse=True)[0]
    site_pkgs = os.path.join(venv_path, "lib", f"python{pyver}", "site-packages")

    if os.path.isdir(site_pkgs) and site_pkgs not in sys.path:
        sys.path.insert(0, site_pkgs)
        print(f"[pythonrc] added site-packages: {site_pkgs}")
    else:
        print(f"[pythonrc] site-packages not found or already in path: {site_pkgs!r}")

def add_experimental_packages(course_root=None):
    """
    Walks your ML4VFX course worktree for any folders that look like packages
    (i.e. contain an __init__.py) inside `ml4vfxTrees/*` and adds them to sys.path.
    """
    if course_root is None:
        # hard-code your course location here, or read from an env var:
        course_root = os.path.expanduser(
            "~/Library/CloudStorage/SynologyDrive-dataLib/threeD/courses/"
            "05_Machine_Learning_in_VFX/ml4vfxTrees"
        )

    if not os.path.isdir(course_root):
        print(f"[pythonrc] course_root not found: {course_root!r}")
        return

    # find every subfolder in ml4vfxTrees that has an __init__.py
    for pkg_dir in glob.glob(os.path.join(course_root, "*")):
        init_py = os.path.join(pkg_dir, "__init__.py")
        if os.path.isfile(init_py):
            # add the parent so that "import houAStar" works
            parent = os.path.dirname(pkg_dir)
            if parent not in sys.path:
                sys.path.insert(0, parent)
                print(f"[pythonrc] added experimental package path: {parent!r}")

# Run them both
add_poetry_site_packages("houdinilab")
add_experimental_packages()

