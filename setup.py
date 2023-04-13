from cx_Freeze import setup, Executable


exe = Executable(
    script="main.py",
    base="Win32GUI",
    icon="ressources/coesite.ico"
)


setup(
    name="Coesite",
    version="0.1",
    description="Music Downloader",
    executables=[exe],
    options={'build_exe': {'include_files': ['ressources/coesite.ico']}},
)