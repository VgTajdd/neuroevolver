@echo off
setlocal
set CURRENT_DIR=%~dp0
:: cd /d changes directly from C to without double command : "cd d:/some/route + d:"
::cmd /k "cd /d %CURRENT_DIR%/../..\venv\Scripts & activate & cd /d %CURRENT_DIR% & python demo.py & deactivate"
:: This make the same than the line above.
call "%CURRENT_DIR%/../../venv/Scripts/activate.bat"

:: Python use this path as reference for relative paths. e.g. "assets/x.png"
cd /d "%CURRENT_DIR%/src"

call python main.py --train neat_walker
call deactivate
endlocal