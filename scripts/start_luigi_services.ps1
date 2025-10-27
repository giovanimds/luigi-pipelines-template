param(
    [string]$ProjectPath = 'your-project-path',
    [int]$LuigidStartupTimeoutSeconds = 60
)

$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$timestamp] $Message"
}

Write-Log "Starting combined Luigi services bootstrap using Project Venv..."
Write-Log "Project path: $ProjectPath"

if (!(Test-Path $ProjectPath)) {
    throw "Project path not found: $ProjectPath"
}

Set-Location -Path $ProjectPath

## DEFINIÇÃO DO EXECUTÁVEL PYTHON DO VENV
$VenvPython = Join-Path $ProjectPath '.venv\Scripts\python.exe'
$VenvPip = Join-Path $ProjectPath '.venv\Scripts\pip.exe'

if (!(Test-Path $VenvPython)) {
    throw "Venv Python executable not found: $VenvPython. Did you run 'python -m venv .venv' and install dependencies?"
}

# 1. GARANTE A INSTALAÇÃO DO PACOTE (CHAMADO DIRETO PELO VENV PIP)
Write-Log "Ensuring custom Python package is installed in editable mode..."
$installCmd = "$VenvPip install -e ."
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', $installCmd -WorkingDirectory $ProjectPath -WindowStyle Hidden -Wait
Write-Log "Package 'pipelines_planejamento' installed/updated."

# --------------------------------------------------------------------------
# CONFIGURAÇÃO DE LOGS E ESTADO (INALTERADA)
# --------------------------------------------------------------------------
$logsPath = Join-Path $ProjectPath 'logs'
$statePath = Join-Path $ProjectPath 'state//state.pickle'
$luigidLog = Join-Path $logsPath 'luigid.log'
$schedulerLog = Join-Path $logsPath 'luigi_scheduler.log'

foreach ($path in @($logsPath, $statePath)) {
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Log "Created directory: $path"
    }
}

# 2. INICIA O LUIGID (USANDO 'uv run luigid' NO CWD DO PROJETO)
Write-Log "Launching luigid via 'uv run luigid' in project cwd..."

# Construímos o comando para redirecionar logs do luigid para o arquivo de log
$luigidCmd = "uv run luigid --logdir `"$logsPath`" --state-path `"$statePath`" --port 8082 > `"$luigidLog`" 2>&1"

# Executamos o comando usando cmd.exe para preservar redirecionamentos e rodar no WorkingDirectory
$luigidProcess = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', $luigidCmd -WorkingDirectory $ProjectPath -WindowStyle Hidden -PassThru
Write-Log "luigid started (uv) with PID $($luigidProcess.Id)"

# --------------------------------------------------------------------------
# VERIFICAÇÃO DO LUIGID (INALTERADA)
# --------------------------------------------------------------------------
Write-Log "Waiting for luigid to accept connections on port 8082..."
# ... [O código de verificação do socket permanece o mesmo] ...
$luigidReady = $false
$attemptInterval = 2
$maxAttempts = [math]::Ceiling($LuigidStartupTimeoutSeconds / $attemptInterval)

for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect('127.0.0.1', 8082)
        if ($client.Connected) {
            $client.Close()
            $luigidReady = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds $attemptInterval
    }
    finally {
        if ($client) { $client.Dispose() }
    }
}

if ($luigidReady) {
    Write-Log "luigid is online. Proceeding to start Luigi cron scheduler."
}
else {
    Write-Warning "luigid did not respond within $LuigidStartupTimeoutSeconds seconds. Continuing anyway."
}

# --------------------------------------------------------------------------  
# 3. INICIA O SCHEDULER CUSTOMIZADO (USANDO UV RUN - MAIS LIMPO)
# --------------------------------------------------------------------------
$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
"[$timestamp] Starting Luigi scheduler daemon..." | Out-File -FilePath $schedulerLog -Encoding UTF8 -Append

# Define o módulo Python a ser executado
$schedulerModule = "pipelines_planejamento.scheduler"

Write-Log "Running Luigi cron scheduler with uv run (logging to $schedulerLog)..."

# Usa uv run para consistência com o luigid
$schedulerCmd = "uv run python -m $schedulerModule > `"$schedulerLog`" 2>&1"
$luigiSchedulerProcess = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', $schedulerCmd -WorkingDirectory $ProjectPath -WindowStyle Hidden -PassThru

Write-Log "Luigi scheduler started in background with PID $($luigiSchedulerProcess.Id). Script complete."
