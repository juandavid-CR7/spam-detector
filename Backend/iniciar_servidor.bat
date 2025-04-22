bat

@echo off
echo Entrenando modelo...
python eentrenar_modelo.py

echo Iniciando servidor...
python app.py
pause 