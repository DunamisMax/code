# Run this script as an administrator

$logFile = "Windows_Update_Fix_Log.txt"
$servicesRestartMaxRetries = 3
$servicesRestartRetryDelay = 5

function Write-Log {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

function Restart-ServiceSafely {
    param (
        [string]$serviceName
    )
    Write-Log "Restarting the $serviceName service..."
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($service) {
        $retryCount = 0
        while ($retryCount -lt $servicesRestartMaxRetries) {
            Restart-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
            if ($?) {
                Write-Log "$serviceName restarted successfully."
                return
            } else {
                Write-Log "Failed to restart $serviceName. Retry attempt: $($retryCount + 1)"
                $retryCount++
                Start-Sleep -Seconds $servicesRestartRetryDelay
            }
        }
        Write-Log "Failed to restart $serviceName after $servicesRestartMaxRetries attempts."
    } else {
        Write-Log "$serviceName service not found."
    }
}

Write-Log "Stopping Windows Update services..."
$services = @("BITS", "wuauserv", "appidsvc", "cryptsvc")
foreach ($service in $services) {
    Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
    if ($?) {
        Write-Log "$service stopped successfully."
    } else {
        Write-Log "Failed to stop $service or service not found."
    }
}

Write-Log "Removing old Windows Update download cache..."
$cacheDirectories = @("$env:systemroot\SoftwareDistribution\*", "$env:systemroot\System32\catroot2\*")
foreach ($directory in $cacheDirectories) {
    Remove-Item -Path $directory -Recurse -Force -ErrorAction SilentlyContinue
    if ($?) {
        Write-Log "$(Split-Path $directory -Leaf) cache removed successfully."
    } else {
        Write-Log "Failed to remove $(Split-Path $directory -Leaf) cache."
    }
}

Write-Log "Resetting the Windows Update components security descriptors..."
foreach ($service in $services) {
    sc.exe sdset $service "D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;AU)(A;;CCLCSWRPWPDTLOCRRC;;;PU)" -ErrorAction SilentlyContinue
    if ($?) {
        Write-Log "Security descriptors for $service reset successfully."
    } else {
        Write-Log "Failed to reset security descriptors for $service."
    }
}

Write-Log "Registering DLLs..."
$dlls = @("atl.dll", "urlmon.dll", "mshtml.dll", "shdocvw.dll", "browseui.dll", "jscript.dll", "vbscript.dll", "scrrun.dll",
          "msxml.dll", "msxml3.dll", "msxml6.dll", "actxprxy.dll", "softpub.dll", "wintrust.dll", "dssenh.dll", "rsaenh.dll",
          "gpkcsp.dll", "sccbase.dll", "slbcsp.dll", "cryptdlg.dll", "oleaut32.dll", "ole32.dll", "shell32.dll", "initpki.dll",
          "wuapi.dll", "wuaueng.dll", "wuaueng1.dll", "wucltui.dll", "wups.dll", "wups2.dll", "wuweb.dll", "qmgr.dll",
          "qmgrprxy.dll", "wucltux.dll", "muweb.dll", "wuwebv.dll")
foreach ($dll in $dlls) {
    regsvr32.exe /s $dll -ErrorAction SilentlyContinue
    if ($?) {
        Write-Log "$dll registered successfully."
    } else {
        Write-Log "Failed to register $dll."
    }
}

Write-Log "Resetting Winsock..."
netsh winsock reset -ErrorAction SilentlyContinue
if ($?) {
    Write-Log "Winsock reset successfully."
} else {
    Write-Log "Failed to reset Winsock."
}

foreach ($service in $services) {
    Restart-ServiceSafely -serviceName $service
}

Write-Log "Script completed. Please reboot your machine."