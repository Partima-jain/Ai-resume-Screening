# train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
df = pd.read_csv('data/resumes.csv')

# Basic preprocessing
df['resume_text'] = df['resume_text'].str.lower()  # Lowercasing

# Split the data
X = df['resume_text']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

# Train the model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Save the trained model and vectorizer
joblib.dump(model, 'model.pkl')  # Save the model
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')  # Save the vectorizer
