# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import site
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Find the OR-Tools binary directories
ortools_paths = []
for path in site.getsitepackages():
    potential_path = os.path.join(path, 'ortools')
    if os.path.exists(potential_path):
        ortools_paths.append(potential_path)

# Collect all necessary packages
hiddenimports = [
    'openpyxl',
    'pandas', 
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'ortools',
    'ortools.sat.python',
    'ortools.sat.python.cp_model',
    'ortools.sat.python.cp_model_helper',  # Explicitly add this
    'pydantic',
    'typing',
    'tkinter',
    'pathlib',
    'collections',
    'datetime',
    'pytz',
]

# Add all scheduler submodules
scheduler_imports = [
    'scheduler',
    'scheduler.scheduler',
    'scheduler.scheduler_classes',
    'scheduler.export_schedules',
    'scheduler.data_loader',
]
hiddenimports.extend(scheduler_imports)

# Collect data files
datas = [
    ('Member&Task_Info.xlsx', '.'),  # Include your Excel file
]

# Add any other assets you might need
if os.path.exists('scheduler/assets'):
    datas.append(('scheduler/assets', 'scheduler/assets'))

# Explicitly collect OR-Tools binary files
binaries = []
for ortools_path in ortools_paths:
    for root, dirs, files in os.walk(ortools_path):
        for file in files:
            if file.endswith('.dll') or file.endswith('.pyd') or file.endswith('.so'):
                source_path = os.path.join(root, file)
                target_dir = os.path.relpath(root, os.path.dirname(ortools_path))
                binaries.append((source_path, target_dir))

a = Analysis(
    ['main.py'],  # Use your latest UI (main) file
    pathex=[os.path.dirname(os.path.abspath('main.py'))],
    binaries=binaries,  # Include the collected binaries
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],  # Look for hook files in the current directory
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FilmScheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='scheduler/assets/app_icon.ico' if os.path.exists('scheduler/assets/app_icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FilmScheduler',
)