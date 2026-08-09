import os
import sys
import shutil
import subprocess

def build_exe():
    print("==========================================")
    print("Building Sticky Notes Executable (.exe)")
    print("==========================================")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    dist_dir = os.path.join(base_dir, "dist")
    build_dir = os.path.join(base_dir, "build")

    # Clean old build artifacts to prevent locked files / base_library corruption
    for folder in [build_dir, dist_dir]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Cleaned {folder}")
            except Exception as e:
                print(f"Warning: Could not remove {folder}: {e}")

    # Generate assets if not present
    ico_path = os.path.join(assets_dir, "app_icon.ico")
    if not os.path.exists(ico_path):
        print("Generating application icons...")
        from assets.generate_assets import create_sticky_note_icon
        create_sticky_note_icon(assets_dir)

    main_script = os.path.join(base_dir, "src", "main.py")
    add_data_flag = f"{assets_dir};assets"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        "--noupx",  # Disable UPX compression to prevent PyQt6 DLL corruption
        "--name=StickyNotes",
        f"--icon={ico_path}",
        f"--add-data={add_data_flag}",
        f"--paths={base_dir}",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=sqlite3",
        "--clean",
        main_script,
    ]

    print(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            exe_path = os.path.join(dist_dir, "StickyNotes.exe")
            print("\nBUILD SUCCESSFUL!")
            print(f"Executable generated at: {exe_path}")
    except subprocess.CalledProcessError as e:
        print(f"\nBUILD FAILED with error code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
