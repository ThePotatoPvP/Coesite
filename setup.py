import sys
from cx_Freeze import setup, Executable

# informations sur l'exécutable
exe = Executable(
    script="main.py",
    base="Win32GUI",
    icon="ressources/coesite.ico"
)

# création du setup
setup(
    name="Coesite",
    version="0.1",
    description="Music Downloader",
    executables=[exe],
    options={'build_exe': {'include_files': ['ressources/coesite.ico']}},
)