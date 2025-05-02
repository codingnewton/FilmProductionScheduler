# save as find_dlls.py
import os
import site
import ortools

# Find OR-Tools package directory
ortools_path = os.path.dirname(ortools.__file__)
print(f"OR-Tools path: {ortools_path}")

# Look for the cp_model_helper DLL or related files
for root, dirs, files in os.walk(ortools_path):
    for file in files:
        if "cp_model" in file.lower() and (file.endswith(".dll") or file.endswith(".pyd") or file.endswith(".so")):
            print(f"Found: {os.path.join(root, file)}")