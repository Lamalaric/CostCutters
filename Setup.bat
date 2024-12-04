@echo off
color a
cls
echo Please make sure you run as admin
timeout /t 5 /nobreak
echo INSTALLING DEPENDANCIES
timeout /t 3
pip install flask 
pip install flask_cors
echo Press enter to exit
set /p input=