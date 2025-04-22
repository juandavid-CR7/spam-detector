from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
import os

from utils import (
    limpiar_texto,
    evaluar_factores_extra,
    revisar_listas_personalizadas,
    detectar_razones_de_spam
)

app = Flask(__name__)
CORS(app)

# Cargar modelo y vectorizador
model = joblib.load("modelo_spam.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route('/clasificar', methods=['POST'])
def clasificar():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    asunto = data.get('asunto', '')
    dominio = data.get('dominio', '')
    hora_envio = data.get('horaEnvio', '')
    nivel = data.get('nivel', 'medio')

    mensaje_limpio = limpiar_texto(mensaje)
    texto_vec = vectorizer.transform([mensaje_limpio])
    pred = model.predict(texto_vec)[0]

    feature_names = vectorizer.get_feature_names_out()
    vect_array = texto_vec.toarray()[0]
    tokens_pesados = [
        (feature_names[i], vect_array[i])
        for i in texto_vec.nonzero()[1]
        if vect_array[i] > 0
    ]
    tokens_top = [token for token, peso in sorted(tokens_pesados, key=lambda x: x[1], reverse=True)[:5]]
    razones = detectar_razones_de_spam(mensaje)

    score = evaluar_factores_extra(asunto, dominio, hora_envio)
    estado_lista = revisar_listas_personalizadas(dominio)

    resultado = "No Spam"
    if estado_lista == "bloqueado":
        resultado = "Spam"
    elif estado_lista == "permitido":
        resultado = "No Spam"
    else:
        if nivel == "bajo":
            resultado = "Spam" if pred == 1 else "No Spam"
        elif nivel == "medio":
            resultado = "Spam" if pred == 1 or score >= 2 else "No Spam"
        elif nivel == "alto":
            resultado = "Spam" if pred == 1 or score >= 1 else "No Spam"

    return jsonify({
        "resultado": resultado,
        "prediccion": int(pred),
        "mensaje": mensaje,
        "palabras_clave": tokens_top,
        "razones": razones
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    prediccion = data.get("prediccion", "")
    correcto = data.get("correcto", None)
    if not mensaje or correcto is None:
        return jsonify({"error": "Faltan datos"}), 400

    fila = f'"{mensaje.replace("\"", "\'")}",{prediccion},{correcto}\n'
    with open("backend/feedback.csv", "a", encoding="utf-8") as f:
        f.write(fila)
    return jsonify({"estado": "Feedback guardado correctamente"})

@app.route('/guardar_correo', methods=['POST'])
def guardar_correo():
    data = request.get_json()
    asunto = data.get('asunto', '')
    mensaje = data.get('mensaje', '')
    etiqueta = data.get('etiqueta', '')

    if not asunto or not mensaje or etiqueta not in ['spam', 'ham']:
        return jsonify({"error": "Datos incompletos"}), 400

    dataset_path = "backend/dataset_personal.csv"
    linea = f"{etiqueta},{asunto} | {mensaje.replace(',', ';')}\n"
    with open(dataset_path, "a", encoding="utf-8") as f:
        f.write(linea)

    return jsonify({"estado": "Correo guardado exitosamente ✅"})
@app.route('/agregar_correo', methods=['POST'])
def agregar_correo():
    data = request.get_json()
    texto = data.get('texto', '')
    etiqueta = data.get('etiqueta', '').lower()
    remitente = data.get('remitente', '').strip()

    if not texto or etiqueta not in ['spam', 'ham'] or not remitente:
        return jsonify({"mensaje": "❌ Faltan datos obligatorios"}), 400

    # Guardar en dataset_personal.csv
    with open("dataset_personal.csv", "a", encoding="utf-8") as f:
        f.write(f"{etiqueta},{texto.replace(',', ';')}\n")

    # Guardar remitente en lista correspondiente
    if etiqueta == "spam":
        with open("lista_bloqueados.txt", "a", encoding="utf-8") as f:
            f.write(remitente + "\n")
    else:
        with open("lista_permitidos.txt", "a", encoding="utf-8") as f:
            f.write(remitente + "\n")

    return jsonify({"mensaje": "✅ Correo y remitente guardados correctamente"})


if __name__ == '__main__':
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import subprocess
    import time
    import os
    import sys

    class ReloadOnChange(FileSystemEventHandler):
        def on_any_event(self, event):
            print(" Cambios detectados, reiniciando...")
            os.execv(sys.executable, ['python'] + sys.argv)

    event_handler = ReloadOnChange()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()

    try:
        app.run(debug=True)
    finally:
        observer.stop()
        observer.join()

