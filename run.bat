@echo off
cd /d %~dp0

:: Run frontend in a new command window
start "Frontend" cmd /k "cd /d frontend && npm install && npm run build && npm run dev"

:: Run backend in a new command window
start "Backend" cmd /k "cd /d backend && call venv\Scripts\activate && flask run"

echo Frontend and backend processes started. Check the respective terminal outputs.
pause
