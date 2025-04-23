Proyecto Spam/ ├── Backend/ │ ├── app.py # Archivo principal de Flask │ ├── entrenar_modelo.py # Script para entrenar el modelo │ ├── modelo_spam.pkl # Modelo entrenado de clasificación │ ├── vectorizer.pkl # Vectorizador de texto para el modelo │ ├── dataset_personal.csv # Dataset personalizado de correos │ ├── feedback.csv # Archivo donde se guardan las retroalimentaciones │ ├── lista_bloqueados.txt # Lista de remitentes bloqueados (Spam) │ ├── lista_permitidos.txt # Lista de remitentes permitidos (No Spam) │ ├── templates/ │ │ ├── index.html # Interfaz de usuario para la clasificación │ │ └── crear_dataset.html # Interfaz para agregar correos al dataset │ ├── static/ │ │ ├── style.css # Estilos de la aplicación │ │ └── script.js # Lógica de la aplicación en JavaScript ├── requirements.txt # Requerimientos de Python ├── README.md # Este archivo
yaml
Copiar

---

## Requisitos

### 1. Requisitos del sistema

- **Ubuntu** 20.04+ o cualquier sistema compatible con Python y Flask
- **Python 3.6+**
- **pip** para instalar las dependencias de Python
- **VirtualBox** o algún VPS (opcional si quieres desplegarlo en un servidor)

### 2. Dependencias

Para instalar las dependencias necesarias, crea un entorno virtual (opcional pero recomendado) y ejecuta:

```bash
# Crear un entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
________________________________________
Ejecución local
1. Iniciar el servidor Flask
Para correr el servidor localmente, simplemente ejecuta:
bash
Copiar
python3 app.py
Esto hará que el servidor Flask corra en http://0.0.0.0:5001, y podrás acceder a la interfaz desde cualquier navegador en la misma red usando:
cpp
Copiar
http://192.168.100.37:5001
Asegúrate de actualizar las URLs en tu archivo script.js si estás accediendo desde otra máquina, apuntando a tu IP local en lugar de localhost.
________________________________________
Despliegue en servidor
Para desplegar el proyecto en un servidor remoto (por ejemplo, en un VPS de DigitalOcean):
1. Instalar dependencias
En tu servidor, sigue estos pasos:
bash
Copiar
# Instalar dependencias de Python
sudo apt update
sudo apt install python3-pip python3-dev
pip3 install -r requirements.txt
2. Configurar Gunicorn (servidor WSGI para Flask)
Instala Gunicorn para servir la aplicación Flask:
bash
Copiar
pip install gunicorn
Luego, ejecuta la aplicación con Gunicorn:
bash
Copiar
gunicorn --workers 3 --bind 0.0.0.0:5001 app:app
Esto hará que el servidor Flask sea accesible desde tu servidor remoto en http://<IP_DEL_SERVIDOR>:5001.
3. Configurar Nginx (opcional para producción)
Si deseas servir la aplicación a través de Nginx (lo cual es recomendado para producción), configura un archivo de configuración en /etc/nginx/sites-available/:
nginx
Copiar
server {
    listen 80;
    server_name <tu_dominio_o_IP>;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
4. Abrir el puerto en el firewall
Asegúrate de permitir el puerto 5001 si estás usando UFW:
bash
Copiar
sudo ufw allow 5001
5. Acceder a la aplicación desde el navegador
Una vez que todo esté configurado, podrás acceder a la aplicación desde el navegador en:
cpp
Copiar
http://<tu_dominio_o_IP>:5001
________________________________________
¿Cómo agregar correos al dataset?
1.	Accede a la interfaz de crear_dataset.html.
2.	Introduce un correo con el asunto, dominio y contenido.
3.	Elige si el correo es Spam o No Spam.
4.	Haz clic en "Guardar" para agregarlo al dataset.
________________________________________
Mejoras y próximos pasos
1.	Implementar reentrenamiento automático del modelo cuando se agreguen nuevos correos al dataset.
2.	Agregar más validaciones de correo electrónico (por ejemplo, verificar que la dirección de correo sea válida).
3.	Desplegar el proyecto en un servidor con Nginx para manejar más tráfico.
________________________________________
Contribuciones
Si deseas contribuir a este proyecto, por favor sigue estos pasos:
1.	Fork este repositorio.
2.	Crea una rama (git checkout -b feature-xyz).
3.	Haz tus cambios y haz commit de ellos (git commit -am 'Agrega nueva funcionalidad').
4.	Haz push a la rama (git push origin feature-xyz).
5.	Crea un Pull Request para que tus cambios sean revisados.

```
