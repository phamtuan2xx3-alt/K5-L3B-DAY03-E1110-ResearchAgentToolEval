param([ValidateSet('start', 'status', 'stop', 'clean')][string]$Action = 'status')
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$stateDir = Join-Path $repoRoot '.local-models'
$ollamaExe = Join-Path $stateDir 'runtime/ollama.exe'
$serverState = Join-Path $stateDir 'server.json'
$apiUrl = 'http://127.0.0.1:11435'

function Get-OwnedServer {
    if (-not (Test-Path -LiteralPath $serverState)) { return $null }
    $savedServer = Get-Content -Raw -LiteralPath $serverState | ConvertFrom-Json
    $serverProcess = Get-Process -Id $savedServer.pid -ErrorAction SilentlyContinue
    if ($serverProcess -and $serverProcess.Path -eq $ollamaExe -and $serverProcess.StartTime.ToUniversalTime().Ticks.ToString() -eq $savedServer.startedTicks) {
        return $serverProcess
    }
    return $null
}

function Stop-OwnedServer {
    $ownedServer = Get-OwnedServer
    if ($ownedServer) {
        Stop-Process -Id $ownedServer.Id
        Write-Output 'Stopped the project Ollama server.'
    }
}

switch ($Action) {
    'start' {
        if (-not (Test-Path -LiteralPath $ollamaExe)) { throw 'Portable Ollama is still downloading/extracting.' }
        if (Get-OwnedServer) { Write-Output "Already running: $apiUrl"; break }
        $occupied = Get-NetTCPConnection -LocalPort 11435 -State Listen -ErrorAction SilentlyContinue
        if ($occupied) { throw 'Port 11435 is occupied by another process; it was not stopped.' }
        $env:OLLAMA_HOST = '127.0.0.1:11435'
        $env:OLLAMA_MODELS = Join-Path $stateDir 'models'
        $env:OLLAMA_NO_CLOUD = '1'
        $env:OLLAMA_NOPRUNE = '1'
        $env:OLLAMA_NUM_PARALLEL = '1'
        $env:OLLAMA_MAX_LOADED_MODELS = '1'
        $env:OLLAMA_CONTEXT_LENGTH = '8192'
        $env:OLLAMA_KEEP_ALIVE = '1m'
        New-Item -ItemType Directory -Force -Path (Join-Path $stateDir 'logs') | Out-Null
        $started = Start-Process -FilePath $ollamaExe -ArgumentList 'serve' -WorkingDirectory $stateDir -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $stateDir 'logs/ollama.stdout.log') -RedirectStandardError (Join-Path $stateDir 'logs/ollama.stderr.log')
        @{pid=$started.Id; startedTicks=$started.StartTime.ToUniversalTime().Ticks.ToString()} | ConvertTo-Json | Set-Content -Encoding utf8 -LiteralPath $serverState
        $ready = $false
        for ($attempt = 0; $attempt -lt 30; $attempt++) {
            try { $null = Invoke-RestMethod "$apiUrl/api/version" -TimeoutSec 2; $ready = $true; break } catch { Start-Sleep -Seconds 1 }
        }
        if (-not $ready) { throw 'Ollama did not become ready; inspect .local-models/logs/ollama.stderr.log.' }
        Write-Output "Ollama ready: $apiUrl (OpenAI-compatible API: $apiUrl/v1)"
    }
    'status' {
        Write-Output "Local model folder: $stateDir"
        if (Test-Path -LiteralPath (Join-Path $stateDir 'logs/weights-download.log')) {
            Get-Content -LiteralPath (Join-Path $stateDir 'logs/weights-download.log') -Tail 6
        }
        if (Get-OwnedServer) {
            Write-Output "Project Ollama server is running: $apiUrl"
            $models = Invoke-RestMethod "$apiUrl/api/tags" -TimeoutSec 5
            $models.models | Select-Object name, @{Name='Size_GB';Expression={[math]::Round($_.size/1GB,2)}} | Format-Table
        } else { Write-Output 'Project Ollama server is stopped.' }
    }
    'stop' { Stop-OwnedServer }
    'clean' {
        if (-not (Test-Path -LiteralPath $stateDir)) { Write-Output 'Nothing to clean.'; break }
        $resolvedTarget = (Resolve-Path -LiteralPath $stateDir).Path
        $marker = Join-Path $resolvedTarget '.e1110-managed'
        if ($resolvedTarget -ne [IO.Path]::GetFullPath((Join-Path $repoRoot '.local-models')) -or -not $resolvedTarget.StartsWith($repoRoot + [IO.Path]::DirectorySeparatorChar) -or -not (Test-Path -LiteralPath $marker)) {
            throw 'Cleanup target failed the workspace/ownership check.'
        }
        if ((Get-Content -Raw -LiteralPath $marker).Trim() -ne $repoRoot) { throw 'Ownership marker does not match this project.' }
        $activeArchive = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'curl.exe' -and $_.CommandLine -like '*ollama-windows-amd64.zip*' }
        if ($activeArchive) { throw 'Runtime download is still active; wait for completion before cleanup.' }
        $downloadPidFile = Join-Path $stateDir 'weights-download.pid'
        if (Test-Path -LiteralPath $downloadPidFile) {
            $workerId = [int](Get-Content -Raw -LiteralPath $downloadPidFile)
            $worker = Get-CimInstance Win32_Process -Filter "ProcessId=$workerId"
            if ($worker -and $worker.CommandLine.Contains((Join-Path $repoRoot 'starter_v0/scripts/download_local_weights.py'))) { Stop-Process -Id $workerId }
        }
        Stop-OwnedServer
        Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
        Write-Output 'Removed only the project .local-models folder.'
    }
}
