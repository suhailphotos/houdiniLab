# pythonrc.py
import os
import sys
import glob
import json
import traceback

# ─────────────────────────────────────────────────────────────────────────
# 1) Compute BASE, JSON_DIR, and LOG_DIR robustly
# ─────────────────────────────────────────────────────────────────────────
try:
    BASE = os.path.realpath(os.path.dirname(__file__))
except NameError:
    import inspect
    BASE = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))

JSON_DIR = os.path.join(BASE, "..", "json")
LOG_DIR  = os.path.join(BASE, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
ERROR_LOG = os.path.join(LOG_DIR, "pythonrc_error.log")

# ─────────────────────────────────────────────────────────────────────────
# 2) Core functions
# ─────────────────────────────────────────────────────────────────────────
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


def load_config(fname):
    """
    Load and parse a JSON file if it exists, otherwise return empty dict.
    """
    path = os.path.join(JSON_DIR, fname)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[pythonrc] config not found: {fname}")
    except json.JSONDecodeError as e:
        print(f"[pythonrc] error parsing {fname}: {e}")
    return {}


def add_paths_from_config(config, key):
    """
    For each entry in config[key], if 'path' is non-empty,
    insert it into sys.path and set its env var.
    """
    for entry in config.get(key, []):
        p   = entry.get("path", "").strip()
        var = entry.get("var",  "").strip()
        if p and os.path.isdir(p):
            if p not in sys.path:
                sys.path.insert(0, p)
                print(f"[pythonrc] added {key[:-1]} path: {p}")
            if var:
                os.environ[var] = p
                print(f"[pythonrc] set env {var}={p}")

# ─────────────────────────────────────────────────────────────────────────
# 3) Bootstrap & error handling
# ─────────────────────────────────────────────────────────────────────────
def _bootstrap():
    # 3.1 Poetry packages
    add_poetry_site_packages("houdinilab")

    # 3.2 Projects
    projects_cfg = load_config("projects.json")
    add_paths_from_config(projects_cfg, "projects")

    # 3.3 Courses
    courses_cfg = load_config("courses.json")
    add_paths_from_config(courses_cfg, "courses")

try:
    _bootstrap()
except Exception:
    with open(ERROR_LOG, "w") as f:
        traceback.print_exc(file=f)
    # Uncomment to propagate error into Houdini console:
    # raise
