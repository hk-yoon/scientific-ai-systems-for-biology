# Run in PowerShell from this repository root, on a Windows PC with Python 3.11.
# Collects evidence; does NOT upload or publish anything.
$ErrorActionPreference = 'Stop'
$logdir = Join-Path (Get-Location) 'local_validation_logs'
New-Item -ItemType Directory -Force -Path $logdir | Out-Null
$log = Join-Path $logdir 'windows_fresh_validation.txt'
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss K'
"START: $stamp" | Set-Content -Encoding utf8 $log
function Run-Step([string]$label, [string]$exe, [string[]]$argv) {
    "`n=== $label ===" | Add-Content -Encoding utf8 $log
    & $exe @argv 2>&1 | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -ne 0) { throw "$label failed (exit $LASTEXITCODE)" }
}
try {
    Run-Step 'Python launcher' 'py' @('-3.11','--version')
    Run-Step 'Create venv' 'py' @('-3.11','-m','venv','.venv')
    $python = Join-Path (Get-Location) '.venv\Scripts\python.exe'
    Run-Step 'pip install requirements' $python @('-m','pip','install','-r','requirements.txt')
    Run-Step 'Python version and executable' $python @('-c','import sys; print(sys.version); print(sys.executable)')
    Run-Step 'Verify runnable examples' $python @('tools/verify_examples.py')
    'RESULT: PASS (technical check only, NOT publication approval)' | Add-Content -Encoding utf8 $log
    Write-Host "PASS; evidence file: $log"
} catch {
    "RESULT: FAIL - $($_.Exception.Message)" | Add-Content -Encoding utf8 $log
    Write-Error "FAILED; inspect $log"
    exit 1
}
