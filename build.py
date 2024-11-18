import PyInstaller.__main__
import sys
import os

# Build the executable
PyInstaller.__main__.run([
    'main.py',
    '--name=TodoNotesManager',
    '--windowed',  # No console window
    '--onefile',   # Single executable file
    '--icon=app_icon.ico',
    '--add-data=app_icon.ico;.',
    '--clean',
    '--noconsole'
])