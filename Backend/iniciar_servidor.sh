bash

#!/bin/bash

echo "Entrenando modelo..."
python3 entrenar_modelo.py

echo "Iniciando servidor Flask..."

python3 app.py