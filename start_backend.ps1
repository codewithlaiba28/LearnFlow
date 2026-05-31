$services = @(
    @{ Name = "triage-agent"; Port = 8001 },
    @{ Name = "concepts-agent"; Port = 8002 },
    @{ Name = "debug-agent"; Port = 8003 },
    @{ Name = "exercise-agent"; Port = 8004 },
    @{ Name = "progress-agent"; Port = 8005 },
    @{ Name = "code-review-agent"; Port = 8006 }
)

Write-Host "Starting LearnFlow Backend Services without Docker..." -ForegroundColor Green

foreach ($service in $services) {
    Write-Host "Starting $($service.Name) on port $($service.Port)..." -ForegroundColor Cyan
    $name = $service.Name
    $port = $service.Port
    
    # Start each service in a new PowerShell window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend\services; ..\..\.venv312\Scripts\Activate.ps1; uvicorn ${name}.main:app --host 0.0.0.0 --port ${port} --env-file .env"
}

Write-Host "All services started in separate windows." -ForegroundColor Green
Write-Host "Make sure to keep those windows open while testing." -ForegroundColor Yellow
