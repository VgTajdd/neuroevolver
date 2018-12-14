@echo off
echo Start
::MODE con:cols=130 lines=40

setlocal

set CURRENT_DIR=%~dp0

set PYTHONHOME=D:\Compiled_libs\python\Installer\Python-3.7.1
set pythonExe="%PYTHONHOME%\python.exe"
::set PYTHONPATH=%CURRENT_DIR%;%PYTHONHOME%;%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs;%PYTHONHOME%\Lib\site-packages;%PYTHONHOME%\Scripts
set PYTHONPATH=%PYTHONHOME%;%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs;%PYTHONHOME%\Lib\site-packages;%PYTHONHOME%\Scripts
set PATH=%PYTHONPATH%;%PATH%;

:: cd /d changes directly from C to without double command : "cd d:/some/route + d:"
cd /d %CURRENT_DIR%../../

echo "python Version:" 
%pythonExe% --version
%pythonExe% -m pip list
:: This creates a directory called venv eith a copy of python. But it needs to be activated.
%pythonExe% -m virtualenv venv

endlocal

echo End