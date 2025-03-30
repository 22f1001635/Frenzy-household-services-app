@echo off
setlocal enabledelayedexpansion

:: Save current directory (PWD)
set PWD=%CD%

echo Setting up the backend...
cd backend || exit /b

:: Create virtual environment if not exists
if not exist "venv" (
    python -m venv venv
)

:: Activate virtual environment using cmd
cmd /c "venv\Scripts\activate.bat && pip install -r requirements.txt"

:: Run Flask application
start /B python main.py

echo Flask started successfully.

:: Go back to the original directory
cd %PWD%

echo Setting up the frontend...
cd frontend || exit /b

:: Install frontend dependencies
if not exist "node_modules" (
    npm install || exit /b
)

:: Start Vue app
start /B npm run dev

echo Frontend started successfully.
exit /b