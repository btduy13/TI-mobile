import os
import zipfile
import shutil
from datetime import datetime

def create_build_zip():
    """
    Creates a zip file containing all necessary files for building the APK.
    """
    # Define the output zip file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"TapeInventoryMobile_build_{timestamp}.zip"
    
    # Define directories and files to include
    include_dirs = ['src', 'assets']
    include_files = ['main.py', 'buildozer.spec', 'requirements.txt']
    
    # Create a temporary directory for the build
    build_dir = "build_temp"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Copy directories
    for dir_name in include_dirs:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(build_dir, dir_name))
    
    # Copy files
    for file_name in include_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, os.path.join(build_dir, file_name))
    
    # Create the zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arcname)
    
    # Clean up the temporary directory
    shutil.rmtree(build_dir)
    
    print(f"Build package created: {zip_filename}")
    print("Upload this file to Google Colab using the build_apk_colab.ipynb notebook.")

if __name__ == "__main__":
    create_build_zip() 