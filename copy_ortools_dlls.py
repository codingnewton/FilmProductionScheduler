# save as copy_ortools_dlls.py
import os
import shutil
import ortools

def copy_ortools_dlls():
    # Get the OR-Tools directory
    ortools_path = os.path.dirname(ortools.__file__)
    print(f"OR-Tools path: {ortools_path}")
    
    # Target directory (your PyInstaller output)
    target_dir = "dist/FilmScheduler"
    
    # Make sure the target directories exist
    os.makedirs(os.path.join(target_dir, "ortools/sat/python"), exist_ok=True)
    
    # Copy the CP Model files
    cp_model_dir = os.path.join(ortools_path, "sat", "python")
    for file in os.listdir(cp_model_dir):
        if file.endswith(".dll") or file.endswith(".pyd") or file.endswith(".so"):
            source = os.path.join(cp_model_dir, file)
            dest = os.path.join(target_dir, "ortools/sat/python", file)
            print(f"Copying {source} to {dest}")
            shutil.copy2(source, dest)
    
    # Copy other DLLs from the main ortools directory
    for file in os.listdir(ortools_path):
        if file.endswith(".dll") or file.endswith(".pyd") or file.endswith(".so"):
            source = os.path.join(ortools_path, file)
            dest = os.path.join(target_dir, "ortools", file)
            print(f"Copying {source} to {dest}")
            shutil.copy2(source, dest)

if __name__ == "__main__":
    copy_ortools_dlls()