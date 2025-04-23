
@echo off
echo Entrenando modelo...
python entrenar_modelo.py

echo Iniciando servidor...
python app.py
pause 