import os
import subprocess
import shutil
import site
import sys

def main():
    print("Building application with PyInstaller...")
    
    # Run PyInstaller
    pyinstaller_result = subprocess.run(
        ["python", "-m", "PyInstaller", "film_scheduler.spec", "--clean"],
        capture_output=True,
        text=True
    )
    
    # Print PyInstaller output
    print(pyinstaller_result.stdout)
    if pyinstaller_result.stderr:
        print("ERRORS:", pyinstaller_result.stderr)
    
    if pyinstaller_result.returncode != 0:
        print("PyInstaller failed. See errors above.")
        return

    print("\nPyInstaller completed successfully. Now copying OR-Tools DLLs...")
    
    # Find the OR-Tools directory
    ortools_path = None
    try:
        import ortools
        ortools_path = os.path.dirname(ortools.__file__)
        print(f"Found OR-Tools at: {ortools_path}")
    except ImportError:
        print("ERROR: Could not import ortools. Make sure it's installed.")
        return

    # Target directory (PyInstaller output)
    target_dir = "dist/FilmScheduler"
    if not os.path.exists(target_dir):
        print(f"ERROR: Target directory {target_dir} does not exist.")
        return
    
    # Make sure the target directories exist
    os.makedirs(os.path.join(target_dir, "ortools/sat/python"), exist_ok=True)
    
    # Copy the CP Model files
    cp_model_dir = os.path.join(ortools_path, "sat", "python")
    print(f"Copying files from {cp_model_dir}...")
    
    if os.path.exists(cp_model_dir):
        for file in os.listdir(cp_model_dir):
            if file.endswith((".dll", ".pyd", ".so")):
                source = os.path.join(cp_model_dir, file)
                dest = os.path.join(target_dir, "ortools/sat/python", file)
                print(f"Copying {source} to {dest}")
                shutil.copy2(source, dest)
    else:
        print(f"WARNING: Directory {cp_model_dir} not found")
    
    # Copy other DLLs from the main ortools directory
    print(f"Copying files from {ortools_path}...")
    for file in os.listdir(ortools_path):
        if file.endswith((".dll", ".pyd", ".so")):
            source = os.path.join(ortools_path, file)
            dest = os.path.join(target_dir, "ortools", file)
            print(f"Copying {source} to {dest}")
            shutil.copy2(source, dest)
    
    # Copy additional potential DLLs from site-packages
    for site_dir in site.getsitepackages():
        potential_dll_dirs = [site_dir]
        for dll_dir in potential_dll_dirs:
            if os.path.exists(dll_dir):
                for file in os.listdir(dll_dir):
                    if file.lower().startswith("cp_model") and file.endswith((".dll", ".pyd", ".so")):
                        source = os.path.join(dll_dir, file)
                        dest = os.path.join(target_dir, file)
                        print(f"Copying additional DLL: {source} to {dest}")
                        shutil.copy2(source, dest)
    
    print("\nBuild process completed successfully!")
    
    print(f"Your application is available in: {os.path.abspath(target_dir)}")

if __name__ == "__main__":
    main()