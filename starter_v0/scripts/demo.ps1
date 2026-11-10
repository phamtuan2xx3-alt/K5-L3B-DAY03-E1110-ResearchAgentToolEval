param([ValidateSet('status', 'stop')][string]$Action = 'status')
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$demoRoot = Join-Path $repoRoot '.local-demo'
foreach ($role in @('ui', 'tunnel')) {
    $stateFile = Join-Path $demoRoot "$role.json"
    if (-not (Test-Path -LiteralPath $stateFile)) { Write-Output "$role : no process metadata"; continue }
    $saved = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
    $owned = Get-Process -Id $saved.pid -ErrorAction SilentlyContinue
    $matches = $owned -and $owned.Path -eq $saved.executable -and $owned.StartTime.ToUniversalTime().Ticks.ToString() -eq $saved.startedTicks
    if (-not $matches) { Write-Output "$role : stopped or process identity changed"; continue }
    if ($Action -eq 'stop') { Stop-Process -Id $owned.Id; Write-Output "$role : stopped" }
    else { Write-Output "$role : running, PID=$($owned.Id)" }
}
$urlFile = Join-Path $demoRoot 'public-url.txt'
if ($Action -eq 'status' -and (Test-Path -LiteralPath $urlFile)) { Get-Content -LiteralPath $urlFile }
