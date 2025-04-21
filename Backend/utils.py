import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+|https\S+", '', texto)
    texto = re.sub(r'[^a-z\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    tokens = texto.strip().split()
    tokens = [stemmer.stem(w) for w in tokens if w not in stop_words]
    return ' '.join(tokens)

def detectar_razones_de_spam(texto):
    razones = []
    if ".exe" in texto.lower() or ".uue" in texto.lower() or "rar5" in texto.lower():
        razones.append("Contiene ejecutable o archivo comprimido sospechoso (.exe, .uue, .rar)")
    if "factura" in texto.lower() and "pago" in texto.lower():
        razones.append("Contenido relacionado con facturas y pagos (potencial phishing)")
    if "eset" in texto.lower() or "troyano" in texto.lower():
        razones.append("Mención de antivirus o troyanos detectados")
    if "urgente" in texto.lower() or "por favor" in texto.lower():
        razones.append("Tono de urgencia típico de spam")
    if any(p in texto.lower() for p in ["premio", "has ganado", "click aquí"]):
        razones.append("Lenguaje de estafa o clickbait")
    return razones

def evaluar_factores_extra(asunto, dominio, hora_envio, contenido=""):
    score = 0
    if asunto:
        if any(pal in asunto.lower() for pal in ["ganaste", "urgente", "premio", "problema", "factura", "pago"]):
            score += 1
        if asunto.isupper():
            score += 1
        if "!!!" in asunto or "$$$" in asunto:
            score += 1
    if dominio and (dominio.endswith(".xyz") or "free" in dominio or "@" not in dominio):
        score += 1
    if hora_envio:
        try:
            hora = hora_envio.split("T")[1][:5]
            if "02:00" <= hora <= "06:00":
                score += 1
        except:
            pass
    if any(ext in contenido.lower() for ext in [".exe", ".uue", ".rar"]):
        score += 2  # ⚠️ Peligro elevado
    return score


def revisar_listas_personalizadas(dominio):
    try:
        with open("lista_bloqueados.txt", encoding='utf-8') as f:
            bloqueados = [line.strip() for line in f.readlines()]
        with open("lista_permitidos.txt", encoding='utf-8') as f:
            permitidos = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return "desconocido"

    if dominio in bloqueados:
        return "bloqueado"
    if dominio in permitidos:
        return "permitido"
    return "desconocido"

