@echo off
setlocal
set CURRENT_DIR=%~dp0
set SWIG_PATH=C:\dev\third_party\swigwin-3.0.12
set PATH=%SWIG_PATH%;%PATH%;
call "%CURRENT_DIR%/venv/Scripts/activate.bat"
call pip install -r requirements.txt
call deactivate

cmd \k
endlocal