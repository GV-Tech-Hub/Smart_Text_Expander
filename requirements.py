import os
import sys
import subprocess
import winreg
from pathlib import Path

def verify_tkinter():
    try:
        import tkinter
        tkinter.Tk().destroy()
        return True
    except:
        print("Warning: tkinter not properly installed.")
        print("Please reinstall Python 3.11.5 with tcl/tk support.")
        return False

def check_python_version():
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True
    print(f"Warning: Python version {version.major}.{version.minor} detected.")
    print("Recommended: Python 3.11.5")
    return False

def setup_virtual_environment():
    print("Setting up virtual environment...")
    try:
        # Remove existing venv if it exists
        if os.path.exists("venv"):
            print("Removing existing virtual environment...")
            if os.name == 'nt':  # Windows
                subprocess.run(["rmdir", "/S", "/Q", "venv"], shell=True)
            else:
                subprocess.run(["rm", "-rf", "venv"])

        # Create new virtual environment
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Get the correct paths
        if os.name == 'nt':  # Windows
            scripts_dir = os.path.join("venv", "Scripts")
            python_path = os.path.join(scripts_dir, "python.exe")
        else:
            scripts_dir = os.path.join("venv", "bin")
            python_path = os.path.join(scripts_dir, "python")

        # Install keyboard package directly
        print("Installing required packages...")
        subprocess.run([python_path, "-m", "pip", "install", "keyboard"], check=True)
        
        print("Virtual environment setup complete!")
        return True
    except Exception as e:
        print(f"Error setting up virtual environment: {e}")
        return False

def create_shortcut():
    try:
        print("Creating desktop shortcut...")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            desktop = winreg.QueryValueEx(key, "Desktop")[0]
        
        shortcut_path = os.path.join(desktop, "Smart Text Expander.bat")
        current_dir = os.getcwd()
        
        # Create batch file with full paths
        batch_content = f'''@echo off
cd /d "{current_dir}"
set PYTHONPATH={current_dir}
call "{current_dir}\\venv\\Scripts\\activate.bat"
"{current_dir}\\venv\\Scripts\\python.exe" "{current_dir}\\text_expander.py"
if errorlevel 1 pause
'''
        
        with open(shortcut_path, 'w') as f:
            f.write(batch_content)
            
        print(f"Shortcut created successfully at: {shortcut_path}")
        return True
    except Exception as e:
        print(f"Warning: Could not create shortcut: {e}")
        print("You can still run the app using 'python text_expander.py' from this directory")
        return False

def verify_files():
    required_files = ['text_expander.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("Error: Missing required files:")
        for file in missing_files:
            print(f"- {file}")
        return False
    return True

def main():
    print("Starting Smart Text Expander installation...")
    print(f"Current directory: {os.getcwd()}")
    
    # Check Python version
    if not check_python_version():
        print("\nPlease install Python 3.11.5 from:")
        print("https://www.python.org/downloads/release/python-3115/")
        input("Press Enter to exit...")
        return
    
    # Verify required files exist
    if not verify_files():
        input("Press Enter to exit...")
        return
    
    # Verify tkinter
    if not verify_tkinter():
        input("Press Enter to exit...")
        return
    
    # Setup virtual environment and install dependencies
    if not setup_virtual_environment():
        input("Press Enter to exit...")
        return
    
    # Create desktop shortcut
    create_shortcut()
    
    print("\nInstallation complete!")
    print("\nYou can now run the app using:")
    print("1. The desktop shortcut: 'Smart Text Expander'")
    print("2. Or by running 'python text_expander.py' from this directory")
    
    # Ask if user wants to run the app now
    response = input("\nWould you like to run the app now? (y/n): ").lower()
    if response == 'y':
        try:
            if os.name == 'nt':  # Windows
                python_path = os.path.join("venv", "Scripts", "python.exe")
            else:
                python_path = os.path.join("venv", "bin", "python")
            subprocess.run([python_path, "text_expander.py"])
        except Exception as e:
            print(f"Error running app: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("\nPress Enter to exit...")