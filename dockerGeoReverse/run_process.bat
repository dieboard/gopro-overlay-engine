@echo off
REM This script automates the service startup process.

REM Step 1: Start the photon service in the background.
echo Starting Photon service in the background...
docker-compose up -d photon

REM Step 2: Wait for the photon service to become 'healthy'.
echo.
echo Waiting for Photon to become healthy. This can take several minutes...

:wait_loop
REM We use 'docker inspect' to directly query the health status.
REM We search for the word "healthy" in the output.
docker inspect --format "{{.State.Health.Status}}" photon_geocoder | findstr "healthy" > nul

REM findstr returns an 'errorlevel' of 0 if the text is found.
if %errorlevel% equ 0 (
    goto :photon_is_ready
)

echo Still waiting for Photon...
REM Wait 5 seconds before the next check.
timeout /t 5 /nobreak > nul
goto :wait_loop

:photon_is_ready
echo.
echo SUCCESS: Photon is healthy!
echo Starting the GoPro script now...
echo.

REM Step 3: Start the gopro-script in interactive mode.
docker-compose run --rm gopro-script

echo.
echo Script finished.

REM Step 4: Shut down all containers cleanly.
echo Shutting down all services...
docker-compose stop

echo.
echo All done.
pause