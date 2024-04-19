# **Title and Informational Messages**
Write-Host "Running Fixes (this might take a while)"

# **Close StudyList**
Write-Host "* Closing the StudyList"
Stop-Process -Name OPALStudyList -Force
Write-Host "done!"

# **Start SQL Server and WWW Services**
Write-Host "* Starting SQL and WWW"
Start-Service -Name "MSSQLSERVER", "W3SVC"
Write-Host "done!"

# **Stop Opal Services**
Write-Host "* Stopping all Opal Services"
Stop-Service -Name "Opal Agent", "Opal Backup", "OpalRad Dicom Print", "OpalRad DICOM Receive", "OpalRad Listener", "OpalRad Router", "OpalRad ImageServer"
Write-Host "done!"

# **Backup Config Files**
Write-Host "* Backing up Config Files"
$backupDir = "C:\opal\cfg\Backup"
if (!(Test-Path $backupDir)) { New-Item -Path $backupDir -ItemType Directory }
Copy-Item -Path "C:\opal\cfg\opalconfiguration.xml" -Destination $backupDir
Copy-Item -Path "C:\opal\cfg\OpalStudyListConfig.xml" -Destination $backupDir
Write-Host "done!"

# **Reset the Opal Configuration File (opalconfiguration.xml)**
Write-Host "* Resetting the Opal Configuration File"
$opalConfig = "C:\opal\cfg\opalconfiguration.xml"
Remove-Item $opalConfig 
Set-Content $opalConfig -Value @"
<?xml version="1.0" encoding="utf-8"?>
<opalconfiguration>
  <database location="localhost@OPALRAD" user="sa" password="1q2w3e4r5t" />
  <packet_size value="4096" />
  <persist_security_info value="True" />
  <ServerConnections>
    <database location="localhost" initialcatalog="OPALRAD" user="sa" password="1q2w3e4r5t" packet_size="4096" name="localhost" />
  </ServerConnections>
  <study_list_refresh_interval value="2" />
  <transfer_log_refresh_interval value="90" />
  <send_queue_refresh_interval value="90" />
  <IISEnable value="0" />
  <MWLMyAETitle value="" />
  <MWLAETitle value="" />
  <MWLNetworkAddress value="" />
  <MWLPort value="" />
  <MWLName value="" />
  <MWLQueryAETitle value="" />
  <MWLDateRange value="" />
  <MWLModality value="" />
  <MWLStatus value="" />
  <MWLInstitution value="" />
  <MWLNewUID value="False" />
  <MWLIssuerPID value="MWLIssuerPID" />
  <Skin value="1" />
</opalconfiguration>
"@
Write-Host "done!"

# **Reset StudyList Configuration file (OpalStudyListConfig.xml)**
Write-Host "* Resetting the Opal Studylist Configuration File (Acquire Active 4)"
$studyListConfig = "C:\opal\cfg\OpalStudyListConfig.xml"
Remove-Item $studyListConfig 
Set-Content $studyListConfig -Value @"
<?xml version="1.0"?>
<Config>
  <acquire active="4" />
  <series_per_image active="True" />
  <autoopen active="False" />
  <teachingstudy active="False" />
  <tsname active="" />
  <tsid active="" />
  <krez active="1" />
  <kodakSingleMode active="False" />
  <series_per_image_paper active="True" />
  <splitEditScreen active="True" />
  <ignoreViewed active="False" />
  <maintainLastSearch active="False" />
  <show_desc_bttn active="True" />
  <show_bp_bttn active="True" />
  <show_ref_bttn active="True" />
  <show_read_bttn active="True" />
  <show_inst_bttn active="True" />
  <show_facil_bttn active="True" />
  <show_dept_bttn active="True" />
</Config>
"@
Write-Host "done!"

# **Change SA Password for SQL Server**
Write-Host "* Changing the SA password for SQL"
Invoke-Sqlcmd -Query "ALTER LOGIN [sa] WITH PASSWORD=N'1q2w3e4r5t'" -ServerInstance localhost
Write-Host "done!"

# **Terminate SQL Sessions**
Write-Host "* Terminating Sessions"
Invoke-SqlCmd -Query "DELETE FROM USERS_SESSION_INFO" -ServerInstance localhost -Database opalrad 
Write-Host "done!"

# **Enable TCP/IP and Named Pipes in SQL**
Write-Host "* Enabling TCP/IP and Named Pipes in SQL"
Invoke-WmiMethod -Namespace "root\Microsoft\SqlServer\ComputerManagement12" -Class ServerNetworkProtocol -Name SetEnable -ArgumentList "Tcp" 
Invoke-WmiMethod -Namespace "root\Microsoft\SqlServer\ComputerManagement12" -Class ServerNetworkProtocol -Name SetEnable -ArgumentList "Np" 
Write-Host "done!"

# **Add Firewall Ports for Opal**
Write-Host "* Add Firewall Ports for Opal"
New-NetFirewallRule -Name "Opal" -DisplayName "Opal" -Direction Inbound -Action Allow -Protocol TCP,UDP -LocalPort 104,1433,33333-33338,80
Write-Host "done!"

# **Free Up Storage Space**
Write-Host "* Freeing up storage space"
Stop-Service -Name W3SVC

Remove-Item -Path "C:\Windows\Temp\*.*" -Recurse -Force
Remove-Item -Path "C:\Windows\Logs\CBS\*.*" -Recurse -Force
Remove-Item -Path "C:\inetpub\wwwroot\OpalWeb\OpalImages\*.*" -Recurse -Force
Remove-Item -Path "C:\inetpub\wwwroot\OpalWeb.Services\cache\*.*" -Recurse -Force

# Adjust permissions as needed (replace with actual users/groups)
$acl = Get-Acl "c:\inetpub\wwwroot"
$acl.SetAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("Administrators", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")))
$acl.SetAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("2020tech", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")))
# ... add more rules if necessary 
Set-Acl "c:\inetpub\wwwroot" $acl

Start-Service -Name W3SVC
Write-Host "done!"

# **Disable Fast Startup**
Write-Host "* Disable Fast Startup"
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power" -Name "HiberbootEnabled" -Value 0
Write-Host "done!"

# **Disable Security Warnings**
Write-Host "* Disable Security Warnings"
New-ItemProperty -Path 'HKCU:\Environment' -Name 'SEE_MASK_NOZONECHECKS' -Value 1 -PropertyType DWORD -Force 
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' -Name 'SEE_MASK_NOZONECHECKS' -Value 1 -PropertyType DWORD -Force
Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Associations' -Name "LowRiskFileTypes" -Value ".bat" -Force
Write-Host "done!"

# **Disable UAC**
Write-Host "* Disabling UAC"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" -Value 0 -Force
Write-Host "done!"
 
# **High Performance Power Plan and Additional Settings**
Write-Host "* Set High Performance Power Plan"
Write-Host "* Set HDD Always on" 
powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c # High Performance plan GUID
powercfg -change -disk-timeout-ac 0

Write-Host "* Set High Performance Power Plan"
Write-Host "* Disable USB Selective Suspend Setting and Adaptive Display Setting"
Write-Host "* Set HDD sleep to 2hrs" 
$activeScheme = (powercfg -getactivescheme).Guid
powercfg -setacvalueindex $activeScheme 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 000
powercfg -setdcvalueindex $activeScheme 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 000
powercfg -setacvalueindex $activeScheme 7516b95f-f776-4464-8c53-06167f40cc99 fbd9aa66-9553-4097-ba44-ed6e9d65eab8 000
powercfg -setdcvalueindex $activeScheme 7516b95f-f776-4464-8c53-06167f40cc99 fbd9aa66-9553-4097-ba44-ed6e9d65eab8 000
powercfg -change -disk-timeout-ac 240 # 240 minutes = 4 hours
Write-Host "done!"

# **Add ASPState Database in SQL**
Write-Host "* Adding ASPState Database in SQL"
& C:\Windows\Microsoft.NET\Framework\v2.0.50727\aspnet_regSQL -E -S localhost -ssadd
Write-Host "done!"

# **Register ASP.NET**
Write-Host "* Register ASP.NET"
& C:\Windows\Microsoft.NET\Framework\v2.0.50727\aspnet_regiis.exe -i
& C:\Windows\Microsoft.NET\Framework\v4.0.30319\aspnet_regiis.exe -i
Write-Host "done!"

# **Set StudyList to Run as Admin**
Write-Host "* Setting StudyList to run as admin"
New-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers' -Name 'C:\opal\bin\OPALStudyList.exe' -Value 'RUNASADMIN' -Force
Write-Host "done!"

# **Restart Opal Services**
Write-Host "* Restarting all Opal Services"
Stop-Service -Name "Opal Agent", "Opal Backup", "OpalRad Dicom Print", "OpalRad DICOM Receive", "OpalRad Listener", "OpalRad Router", "OpalRad ImageServer", "MSSQLSERVER"
Start-Service -Name "MSSQLSERVER", "OpalRad ImageServer", "OpalRad Dicom Print", "OpalRad DICOM Receive", "OpalRad Listener", "OpalRad Router", "Opal Agent", "Opal Backup", "OpalRad Modality Worklist", "W3SVC"
Write-Host "done!"

# **Fixing Opal Web**
# Stop the web service for safer modification
Stop-Service -Name "W3SVC"
# Navigate to the web.config location 
cd C:\inetpub\wwwroot\OpalWeb
# Optimized PowerShell filtering and update
powershell.exe -Command " & { (Get-Content -Path '.\web.config') | Where-Object { $_ -notmatch 'UnhandledExceptionModule' } | Set-Content '.\web.config' }"
# Restart the web service
Start-Service -Name "W3SVC"

# Title and Informational Message
Write-Host "Setting Permissions"

# Function to set permissions with inheritance
function Set-Permissions($path, $permissions) {
    $acl = Get-Acl -Path $path
    foreach ($permission in $permissions) {
        $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($permission, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
        $acl.AddAccessRule($accessRule)
    }
    Set-Acl -Path $path -AclObject $acl

    # Take ownership recursively (if needed)
    takeown.exe /f $path /r /d y 
}

# Array of base folders
$folders = @(
    "C:\opal\bin",
    "C:\opal\cfg",
    "C:\opal\data",
    "C:\opal\Backup",
    # ... Add other base folders here 
)

# Array of permissions to apply
$permissions = @(
    "NETWORK SERVICE",
    "LOCAL SERVICE",
    "Everyone",
    "Authenticated Users",
    "Users",
    "Administrators"
)

# Set permissions on each folder
foreach ($folder in $folders) {
    Write-Host "* Setting permissions for $folder"
    Set-Permissions $folder $permissions
}

Write-Host "done!"


# **Completion Message**
Write-Host "* Fixes Complete!"
Write-Host "." 