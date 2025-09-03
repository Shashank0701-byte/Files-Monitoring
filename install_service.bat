@echo off
REM File Organizer Service Installation Script
REM Run as Administrator

echo ========================================
echo File Organizer Service Installation
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

echo Installing required Python packages...
pip install pywin32

echo.
echo Installing File Organizer Service...
python "%~dp0file_organizer_service.py" install

if %errorLevel% neq 0 (
    echo ERROR: Failed to install service!
    pause
    exit /b 1
)

echo.
echo Starting File Organizer Service...
python "%~dp0file_organizer_service.py" start

if %errorLevel% neq 0 (
    echo ERROR: Failed to start service!
    pause
    exit /b 1
)

echo.
echo ========================================
echo File Organizer Service installed and started successfully!
echo.
echo The service will now automatically:
echo - Monitor your Downloads folder
echo - Organize files based on file_rules.json
echo - Start automatically on system boot
echo.
echo To manage the service:
echo - Stop: python file_organizer_service.py stop
echo - Start: python file_organizer_service.py start
echo - Remove: python file_organizer_service.py remove
echo.
echo Log files are stored in:
echo %USERPROFILE%\AppData\Local\FileOrganizer\service.log
echo ========================================
echo.
pause