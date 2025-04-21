import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from utils import limpiar_texto

df = pd.read_csv("https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv", sep='\\t', names=['label', 'text'])
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
df['text'] = df['text'].apply(limpiar_texto)

X = df['text']
y = df['label']

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2)
model = MultinomialNB()
model.fit(X_train, y_train)

joblib.dump(model, "modelo_spam.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("✅ Modelo y vectorizador guardados.")
