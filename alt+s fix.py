import winreg
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def change_network_shortcut():
    try:
        # Open the registry key for network shortcuts
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\NetworkShortcuts"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                            winreg.KEY_ALL_ACCESS)
        
        # Change the shortcut key to Alt+N
        winreg.SetValueEx(key, "ShortcutKey", 0, winreg.REG_SZ, "N")
        
        winreg.CloseKey(key)
        print("Successfully changed network shortcut to Alt+N")
        return True
    except FileNotFoundError:
        # If key doesn't exist, create it
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "ShortcutKey", 0, winreg.REG_SZ, "N")
        winreg.CloseKey(key)
        print("Successfully created and set network shortcut to Alt+N")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Check if script is running with admin privileges
    if not is_admin():
        # Re-run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        change_network_shortcut()