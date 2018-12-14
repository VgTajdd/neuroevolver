@echo off
setlocal
set CURRENT_DIR=%~dp0
call "%CURRENT_DIR%/../../venv/Scripts/activate.bat"
call pip install -r requirements.txt
::call pip list
call deactivate
endlocal