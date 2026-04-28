REM Launch the game using the compatible Python 3.13 virtual environment
SET PYTHON_EXEC="%~dp0.venv313\Scripts\python.exe"
IF NOT EXIST %PYTHON_EXEC% (
    echo Error: virtual environment python not found at %PYTHON_EXEC%
    pause
    exit /b 1
)
%PYTHON_EXEC% "%~dp0main.py"
if %ERRORLEVEL% neq 0 pause
pause