# This script automates the service startup process.

# Step 1: Start the photon service in the background.
Write-Host "Starting Photon service in the background..."
docker-compose up -d photon

# Step 2: Wait for the photon service to become 'healthy'.
Write-Host ""
Write-Host "Waiting for Photon to become healthy. This can take several minutes..."

while ($true) {
    # We use 'docker inspect' and pipe it to PowerShell's 'Select-String'
    $isHealthy = docker inspect --format "{{.State.Health.Status}}" photon_geocoder | Select-String -Quiet "healthy"

    # Check if the string "healthy" was found
    if ($isHealthy) {
        break # Exit the loop
    }

    Write-Host "Still waiting for Photon..."
    # Wait 5 seconds before the next check.
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "SUCCESS: Photon is healthy!"
Write-Host "Starting the GoPro script now..."
Write-Host ""

# Step 3: Start the gopro-script in interactive mode.
docker-compose run --rm gopro-script

Write-Host ""
Write-Host "Script finished."

# Step 4: Stop the containers cleanly.
Write-Host "Stopping all services..."
docker-compose stop

Write-Host ""
Write-Host "All done."
Read-Host -Prompt "Press any key to continue..."