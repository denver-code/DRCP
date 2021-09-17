echo off

pyinstaller --clean --noconsole drpcs_main.py

del /s /q /f RAT.spec
rmdir /s /q __pycache__
rmdir /s /q build

:cmd
pause null