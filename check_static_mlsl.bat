
set WORK_DIR=%~dp0

REM Include the libraries
set PATH=%PATH%;%WORK_DIR%\lib\z3\bin\
set PYTHONPATH=%PYTHONPATH%;%WORK_DIR%\lib\z3\bin\python\
set PYTHONPATH=%PYTHONPATH%;%WORK_DIR%\lib\waxeye\

REM The input files
set FORMULA=%2
set MODEL=%3

set PYTHON_V27=%1

%PYTHON_V27% check_static_mlsl.py %FORMULA% %MODEL%
