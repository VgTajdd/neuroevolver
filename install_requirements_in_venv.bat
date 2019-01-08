@echo off
setlocal
set CURRENT_DIR=%~dp0
set SWIG_PATH=C:/swigwin-3.0.12
set PATH=%SWIG_PATH%;%PATH%;
call "%CURRENT_DIR%/../../venv/Scripts/activate.bat"
call pip install -r requirements.txt
::call pip list
call deactivate
endlocal