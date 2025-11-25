import streamlit.web.cli as stcli
import os, sys
import webbrowser
from threading import Timer

def resolve_path(path):
    if getattr(sys, "frozen", False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == "__main__":
    # 1. Close splash screen if frozen
    if getattr(sys, 'frozen', False):
        try:
            import pyi_splash
            pyi_splash.close()
        except ImportError:
            pass

    # 2. Redirect stdout/stderr to log file
    if getattr(sys, 'frozen', False):
        log_path = os.path.join(os.path.dirname(sys.executable), 'app_debug.log')
        sys.stdout = open(log_path, 'w', encoding='utf-8')
        sys.stderr = open(log_path, 'w', encoding='utf-8')
    
    app_path = resolve_path("app.py")
    
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.address=localhost",
        "--server.port=8501",
        "--server.headless=true",
    ]
    
    # Open browser after 1.5s
    Timer(1.5, open_browser).start()
    
    sys.exit(stcli.main())