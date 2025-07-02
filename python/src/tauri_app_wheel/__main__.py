"""The main entry point for the Tauri app."""
import sys
import os
from tauri_app_wheel import main

def _macos_gui_optimizations():
    """Apply macOS-specific optimizations for GUI apps."""
    if sys.platform == "darwin":
        # Redirect stdout/stderr to prevent console flashing
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        
        # Ensure proper GUI process initialization
        os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

if __name__ == "__main__":
    _macos_gui_optimizations()
    sys.exit(main())