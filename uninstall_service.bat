@echo off
REM File Organizer Service Uninstallation Script
REM Run as Administrator

echo ========================================
echo File Organizer Service Uninstallation
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Stopping File Organizer Service...
python "%~dp0file_organizer_service.py" stop

echo.
echo Removing File Organizer Service...
python "%~dp0file_organizer_service.py" remove

if %errorLevel% neq 0 (
    echo ERROR: Failed to remove service!
    pause
    exit /b 1
)

echo.
echo ========================================
echo File Organizer Service removed successfully!
echo.
echo The service has been completely uninstalled.
echo Log files remain in:
echo %USERPROFILE%\AppData\Local\FileOrganizer\service.log
echo ========================================
echo.
pause