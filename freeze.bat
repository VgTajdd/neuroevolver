@echo off
setlocal
set CURRENT_DIR=%~dp0
call "%CURRENT_DIR%/venv/Scripts/activate.bat"
call pip freeze > requirements.txt
call deactivate
endlocal