import os
import sys
import subprocess
import winreg
import time
from pathlib import Path

def check_python():
    print("Checking Python installation...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        return False
    return True

def install_dependencies():
    print("Installing/Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        print(f"Error upgrading pip: {e}")
        return False

def setup_virtual_environment():
    print("Setting up Smart Text Expander...")
    try:
        # Remove existing venv if it exists
        if os.path.exists("venv"):
            print("Removing existing virtual environment...")
            try:
                if os.name == 'nt':  # Windows
                    os.system('rmdir /S /Q venv')
                else:
                    os.system('rm -rf venv')
                time.sleep(2)  # Wait for system to release files
                print("Existing virtual environment removed.")
            except Exception as e:
                print(f"Warning: Could not remove existing venv: {e}")
                print("Attempting to continue anyway...")

        # Create virtual environment with specific python version
        print("Creating virtual environment...")
        result = subprocess.run([sys.executable, "-m", "venv", "venv"], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            print(f"Error creating venv: {result.stderr}")
            return False

        # Wait for venv creation to complete
        time.sleep(2)

        # Get the correct pip and python paths
        if os.name == 'nt':  # Windows
            python_path = os.path.join("venv", "Scripts", "python.exe")
            pip_path = os.path.join("venv", "Scripts", "pip.exe")
        else:
            python_path = os.path.join("venv", "bin", "python")
            pip_path = os.path.join("venv", "bin", "pip")

        # Verify paths exist
        if not os.path.exists(python_path) or not os.path.exists(pip_path):
            print(f"Error: Virtual environment files not found at expected location")
            return False

        print("Installing required packages...")
        
        # Upgrade pip first
        print("Upgrading pip in virtual environment...")
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)

        # Install each package separately with error handling
        packages = ["wheel", "keyboard", "PySide6", "pywin32"]
        for package in packages:
            print(f"Installing {package}...")
            try:
                result = subprocess.run([pip_path, "install", package], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode != 0:
                    print(f"Error installing {package}: {result.stderr}")
                    return False
                print(f"{package} installed successfully!")
            except Exception as e:
                print(f"Error installing {package}: {e}")
                return False

        print("All packages installed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during setup: {e}")
        return False

def create_shortcut():
    try:
        print("Creating desktop shortcut...")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            desktop = winreg.QueryValueEx(key, "Desktop")[0]
        
        shortcut_path = os.path.join(desktop, "Smart Text Expander.bat")
        current_dir = os.path.abspath(os.getcwd())
        
        batch_content = f"""@echo off
cd /d "{current_dir}"
start /min cmd /c "
call "{current_dir}\\venv\\Scripts\\activate.bat" && 
"{current_dir}\\venv\\Scripts\\pythonw.exe" "{current_dir}\\text_expander.py"
"
"""
        
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
            
        print(f"Shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"Shortcut creation failed: {e}")
        return False

def main():
    print("Smart Text Expander - Installation")
    print("=================================")
    
    if not check_python():
        print("\\nPython requirements not met!")
        input("Press Enter to exit...")
        return
    
    try:
        print("\\nStep 1: Installing core dependencies...")
        if not install_dependencies():
            print("Failed to install core dependencies")
            input("Press Enter to exit...")
            return
            
        print("\\nStep 2: Setting up virtual environment...")
        if not setup_virtual_environment():
            print("\\nFailed to set up virtual environment")
            print("Please try the following:")
            print("1. Run as administrator")
            print("2. Check your internet connection")
            print("3. Make sure you have enough disk space")
            print("4. Temporarily disable your antivirus")
            input("Press Enter to exit...")
            return
        
        print("\\nStep 3: Creating shortcut...")
        create_shortcut()
        
        print("\\nInstallation complete!")
        print("\\nYou can run Smart Text Expander using:")
        print("1. Desktop shortcut: 'Smart Text Expander'")
        print("2. Or: python text_expander.py")
        
        response = input("\\nWould you like to run it now? (y/n): ").lower()
        if response == 'y':
            try:
                if os.name == 'nt':
                    python_path = os.path.join("venv", "Scripts", "pythonw.exe")
                    subprocess.Popen([python_path, "text_expander.py"], 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                print(f"Error running app: {e}")
        
    except Exception as e:
        print(f"An error occurred during installation: {e}")
        print("\\nPlease try running the installer again as administrator.")
    
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\\nAn error occurred: {e}")
        input("\\nPress Enter to exit...")
