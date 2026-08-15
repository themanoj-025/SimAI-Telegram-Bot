# StartBot.ps1
# Auto-restart script for the Telegram bot on Windows
$maxRetries = 5
$retryCount = 0
$delay = 5  # seconds
while ($true) {
    try {
        Write-Host "[$(Get-Date -Format u)] Starting bot..."
        # Run the bot; replace with your python executable path if needed
        python "c:\Users\jm270\ai_daily_telegram_bot\run_bot.py"
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            Write-Host "[$(Get-Date -Format u)] Bot exited normally."
            break
        } else {
            Write-Warning "[$(Get-Date -Format u)] Bot exited with code $exitCode."
        }
    } catch {
        Write-Error "[$(Get-Date -Format u)] Exception: $_"
    }
    $retryCount++
    if ($retryCount -gt $maxRetries) {
        Write-Error "[$(Get-Date -Format u)] Max retries reached. Giving up."
        break
    }
    $delaySec = $delay * [math]::Pow(2, $retryCount-1) # exponential backoff
    Write-Host "[$(Get-Date -Format u)] Waiting $delaySec seconds before restart..."
    Start-Sleep -Seconds $delaySec
}
