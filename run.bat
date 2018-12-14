@echo off
setlocal
set CURRENT_DIR=%~dp0

:: cd /d changes directly from C to without double command : "cd d:/some/route + d:"
::cmd /k "cd /d %CURRENT_DIR%\venv\Scripts & activate & cd /d %CURRENT_DIR% & python test.py & deactivate"

:: This make the same than the line above.
call "%CURRENT_DIR%/../../venv/Scripts/activate.bat"
::call pip list
::call pip install -r requirements.txt
call python demo.py
::call pip freeze > requirements.txt
call deactivate

::cmd /k 

endlocal