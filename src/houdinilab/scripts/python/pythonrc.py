# pythonrc.py
import os
import sys
import glob
import json

# >>> BEGIN DEBUG LOG SETUP <<<
import atexit

# open log in append mode
LOG_PATH = "/tmp/houdini_pythonrc.log"
_log = open(LOG_PATH, "a", encoding="utf-8")

def log(msg):
    _log.write(msg.rstrip() + "\n")
    _log.flush()

# ensure file is closed when Houdini exits
atexit.register(lambda: _log.close())
# >>> END DEBUG LOG SETUP <<<

BASE = os.path.dirname(__file__)
JSON_DIR = os.path.path(os.path.join(BASE, "..", "json"))


def load_config(fname):
    """Load and parse a JSON file if it exists, otherwise return empty dict."""
    path = os.path.join(JSON_DIR, fname)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[pythonrc] config not found: {fname}")
    except json.JSONDecodeError as e:
        print(f"[pythonrc] error parsing {fname}: {e}")
    return {}

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
            log(f"[pythonrc] added site-packages: {site_pkgs}")
    else:
        print(f"[pythonrc] expected site-packages not found at {site_pkgs!r}")


def add_paths_from_config(config, key):
    """
    For each entry in config[key], if 'path' is non-empty,
    insert it into sys.path and set an env var.
    """
    for entry in config.get(key, []):
        p = entry.get("path", "").strip()
        var = entry.get("var", "").strip()
        if p and os.path.isdir(p):
            if p not in sys.path:
                sys.path.insert(0, p)
                print(f"[pythonrc] added {key[:-1]} path: {p}")
            if var:
                os.environ[var] = p
                print(f"[pythonrc] set env {var}={p}")

# === Bootstrap sequence for projects & courses ===
# 1) Poetry venv
add_poetry_site_packages("houdinilab")

# 2) Projects
projects_cfg = load_config("projects.json")
add_paths_from_config(projects_cfg, "projects")

# 3) Courses
courses_cfg = load_config("courses.json")
add_paths_from_config(courses_cfg, "courses")
### End additions ###
