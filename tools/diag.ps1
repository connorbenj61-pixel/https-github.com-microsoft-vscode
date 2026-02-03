<#
PowerShell diagnostics script.
Outputs a JSON blob describing basic system state.

Run locally to test:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\diag.ps1

This script is suitable to be invoked remotely using Invoke-Command.
#>

$obj = [ordered]@{}

try {
  $os = Get-CimInstance -ClassName Win32_OperatingSystem
  $cs = Get-CimInstance -ClassName Win32_ComputerSystem
  $obj.OS = @{ Caption = $os.Caption; Version = $os.Version; BuildNumber = $os.BuildNumber; LastBootUpTime = $os.LastBootUpTime }
  $obj.Computer = @{ Manufacturer = $cs.Manufacturer; Model = $cs.Model; TotalPhysicalMemory = $cs.TotalPhysicalMemory }
} catch {
  $obj.OS = "error"
  $obj.Computer = "error"
}

try {
  $drives = Get-PSDrive -PSProvider FileSystem | ForEach-Object { @{ Name=$_.Name; Root=$_.Root; Used=($_.Used -as [int64]); Free=($_.Free -as [int64]) } }
  $obj.Drives = $drives
} catch {
  $obj.Drives = @()
}

try {
  $procs = Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 10 | ForEach-Object { @{ Name=$_.ProcessName; Id=$_.Id; CPU=[math]::Round($_.CPU,2); WS=$_.WS } }
  $obj.TopProcesses = $procs
} catch {
  $obj.TopProcesses = @()
}

try {
  $services = Get-Service | Where-Object { $_.Status -eq 'Running' } | Select-Object -First 20 | ForEach-Object { @{ Name=$_.Name; DisplayName=$_.DisplayName } }
  $obj.Services = $services
} catch {
  $obj.Services = @()
}

$obj.Timestamp = (Get-Date).ToUniversalTime().ToString("o")

ConvertTo-Json $obj -Depth 5
