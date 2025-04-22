
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Descargar recursos NLTK si no están disponibles
nltk.download('stopwords')

# Función para limpiar el texto
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

# Cargar dataset personalizado
df = pd.read_csv("dataset_personal.csv", names=["label", "text"])
# Limpiar datos vacíos y convertir etiquetas correctamente
df = df.dropna(subset=["label", "text"]) 

# Normalizar etiquetas a 0 o 1
df["label"] = df["label"].astype(str).str.strip().str.lower().map({"ham": 0, "spam": 1})
df = df.dropna(subset=["label"])  # Quita filas con etiquetas inválidas

# Limpiar texto
df["text"] = df["text"].astype(str).apply(limpiar_texto)


# Entrenamiento
X = df["text"]
y = df["label"]
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)

# Guardar modelo y vectorizador
joblib.dump(model, "modelo_spam.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Modelo entrenado y guardado usando dataset_personal.csv")
