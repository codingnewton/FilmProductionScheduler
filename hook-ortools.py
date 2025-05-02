# hook-ortools.py
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, collect_submodules

# Collect all OR-Tools DLLs and binary files
binaries = collect_dynamic_libs('ortools')

# Collect all submodules (important for OR-Tools internal imports)
hiddenimports = collect_submodules('ortools')

# Add specific submodules that might be missed
hiddenimports += [
    'ortools.sat.python.cp_model',
    'ortools.sat.python.cp_model_helper',
    'ortools.constraint_solver',
    'ortools.linear_solver',
    'ortools.sat',
    'ortools.util',
    'ortools.init',
]

# Collect package data
datas = collect_data_files('ortools')