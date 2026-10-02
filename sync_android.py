#!/usr/bin/env python3
"""
Copy the web app into the Android Chaquopy package.
============================================================

The Android build needs its own copy of app.py, templates/, static/ and
data/ inside `android/app/src/main/python/kotoba_app/`, because that
directory is what gets packaged into the APK.

Keeping two hand-maintained copies is how the two versions quietly drift
apart, so this script makes the top-level app the single source of truth
and regenerates the Android copy from it. CI runs it before every build;
run it yourself after editing anything under templates/ or static/:

    python sync_android.py

The only difference between the two copies of app.py is the `run_server`
entry point appended here, which MainActivity calls through Chaquopy.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
TARGET = ROOT / "android" / "app" / "src" / "main" / "python" / "kotoba_app"

# Directories copied wholesale.
TREES = ["templates", "static", "data"]

# Extra Python modules app.py imports (must ship next to app.py).
MODULES = ["everyday_nl.py", "roadmap_extra.py", "learner_engine.py"]

# Files the running app writes to itself - never ship a stale copy.
RUNTIME_FILES = {
    "streak.json", "feedback.json", "users.json", "user_streaks.json",
    "progress.json", "user_progress.json", "secret_key.txt",
    "roadmap_progress.json", "user_roadmap_progress.json",
    "roadmap_start.json", "user_roadmap_start.json",
    "learner_state.json", "user_learner_state.json",
}

RUN_SERVER = '''

_server_lock = __import__("threading").Lock()
_server_running = False


def run_server():
    \"\"\"Entry point called from Android's MainActivity via Chaquopy.

    Safe to call more than once per process. Android can recreate the
    Activity while this process (and the server thread) keeps running; a
    second app.run() on the same port makes Werkzeug call sys.exit(1),
    which Chaquopy turns into an exception that crashes the app. So a
    repeat call, or a port that is already bound, just returns quietly -
    the server that is already up keeps serving the new WebView.

    make_server never starts the reloader (which would fork a second
    process, unsupported inside Chaquopy), and threaded=True lets the
    WebView issue a few requests in parallel.
    \"\"\"
    global _server_running
    with _server_lock:
        if _server_running:
            return
        try:
            from werkzeug.serving import make_server
            server = make_server("127.0.0.1", 5000, app, threaded=True)
        except OSError:
            # Port taken: an earlier instance in this process still owns it.
            _server_running = True
            return
        _server_running = True
    try:
        server.serve_forever()
    finally:
        _server_running = False
'''


def ignored(_dir, names):
    return [
        n for n in names
        if n in RUNTIME_FILES or n == "__pycache__" or n.endswith(".pyc")
    ]


def main():
    if not (ROOT / "app.py").exists():
        print("app.py not found - run this from the project root", file=sys.stderr)
        return 1

    TARGET.mkdir(parents=True, exist_ok=True)
    for mod in MODULES:
        shutil.copy2(ROOT / mod, TARGET / mod)
        print(f"copied {mod}")
    (TARGET / "__init__.py").touch()

    for tree in TREES:
        src = ROOT / tree
        if not src.is_dir():
            print(f"skipping {tree}/ (not present)")
            continue
        dst = TARGET / tree
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=ignored)
        print(f"synced {tree}/")

    source = (ROOT / "app.py").read_text(encoding="utf-8").rstrip("\n")
    (TARGET / "app.py").write_text(source + "\n" + RUN_SERVER, encoding="utf-8")
    print("synced app.py (+ run_server)")

    print(f"\nAndroid package is up to date: {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
