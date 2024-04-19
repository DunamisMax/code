# **Title and Informational Message**
Write-Host "Comprehensive Windows Maintenance Script" 

# **Logging** 
function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Output $logMessage
    $logMessage | Out-File -FilePath "MaintenanceLog.txt" -Append
}

# **Functions**
function Remove-TempFiles {
    # Define temporary file locations
    $tempPaths = @(
        "C:\Windows\Temp",
        $env:TEMP,               # User's temporary folder
        "C:\Windows\Logs\CBS",  
        "C:\inetpub\wwwroot\OpalWeb\OpalImages",
        "C:\inetpub\wwwroot\OpalWeb.Services\cache"
    ) 

    foreach ($path in $tempPaths) {
        if (Test-Path $path) {
            Write-Host " - Cleaning $path" 
            try {
                Remove-Item $path\* -Recurse -Force -ErrorAction Stop
            } catch {
                Write-Warning "Error cleaning $path: $($_.Exception.Message)"
            }
        } else {
            Write-Warning "Path not found: $path"
        }
    }
}


function Cleanup-WindowsUpdate {
    if (Get-Module -Name PSWindowsUpdate -ListAvailable) {
        Write-Log " - Using PSWindowsUpdate Module"
        Get-WindowsUpdate | Where-Object {$_.Title -like "*cleanup*"} | Install-WindowsUpdate -AcceptAll
    } else {
        Write-Log " - PSWindowsUpdate module not installed. Using DISM method."
        Start-Process dism.exe -ArgumentList "/online /cleanup-image /StartComponentCleanup /ResetBase" -Wait
    }
}

function Defragment-Disks {
    function Defragment-Disks {
        Write-Host " - Analyzing and Defragmenting Disks (HDDs only)"
    
        # Get disks, filter for HDDs, and NTFS file system
        Get-WmiObject -Class Win32_Volume -Filter "DriveType = 3" | 
            Where-Object { $_.FileSystem -match "NTFS" } | 
            ForEach-Object { 
                $drive = $_.DriveLetter + ":" 
                Write-Host "  - Checking $drive"
    
                # Analyze for fragmentation 
                $result = Optimize-Volume -DriveLetter $drive -Analyze -Verbose
                if ($result.FragmentationPercentage -gt 10) { # Adjust threshold if needed
                    Write-Host "  - Defragmenting $drive"
                    Optimize-Volume -DriveLetter $drive -Verbose 
                } else {
                    Write-Host "  - $drive is not significantly fragmented."
                }
            }  
    }
}

function Run-SFC-DISM {
    Write-Log " - Running System File Checker (SFC)"
    sfc.exe /scannow

    Write-Log " - Running DISM to Repair Component Store"
    Repair-WindowsImage /Online /Cleanup-Image /RestoreHealth 
}

function Tweak-Settings {
    function Tweak-Settings {
        # Performance / Power Settings
        Write-Host " - Applying Performance Optimizations"
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power" -Name "HiberbootEnabled" -Value 0  # Disable Fast Startup
        powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  # Set High-Performance power plan
    
        # Privacy Tweaks (adjust as needed)
        Write-Host " - Adjusting Privacy Settings"
        Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Search' -Name 'CortanaEnabled' -Value 0  # Disable Cortana (if desired)
        Set-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search' -Name 'AllowCortana' -Value 0  # Disable Cortana system-wide
        # ... add more privacy settings as needed
    }
}

function Check-Disk-Health {
    Write-Log "Checking Disk Health..."
    Get-WmiObject -Class Win32_LogicalDisk | ForEach-Object {
        $diskHealth = $_.ChkDsk()
        Write-Log "Disk $($_.DeviceID) health check result: $($diskHealth.Status)"
    }
}

function Generate-System-Report {
    Write-Log "Generating System Diagnostics Report..."
    Get-ComputerInfo | Out-File -FilePath "SystemDiagnostics.txt"
}

# **Script Execution**

# Disk Cleanup
Write-Log "Starting Disk Cleanup..."
Remove-TempFiles
Cleanup-WindowsUpdate

# System Integrity Checks
Write-Log "Running System Integrity Checks..."
Run-SFC-DISM

# Optimization
Write-Log "Optimizing System..."
Defragment-Disks
Check-Disk-Health

# Tweaks, Reports, Additional Security (if needed)
Write-Log "Applying Tweaks and Reports..."
Tweak-Settings 
Generate-System-Report

# Optional: Event Log Clearing, Malware Scans (if desired)

Write-Log "Maintenance Complete!" 
