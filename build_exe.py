import PyInstaller.__main__
import sys
import os

# Build the executable
PyInstaller.__main__.run([
    'main.py',
    '--name=TodoNotesManager',
    '--windowed',  # No console window
    '--onefile',   # Single executable file
    '--icon=checklist-hnt.ico',  # Add icon
    '--add-data=checklist-hnt.ico;.',  # Include icon in resources
    '--clean',
    '--noconsole'
])