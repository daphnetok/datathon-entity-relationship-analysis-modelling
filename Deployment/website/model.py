from flask import Flask, request, jsonify, Blueprint
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Get the absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path to the model
MODEL_PATH = os.path.join(BASE_DIR, "models", "stacking_model.pkl")

# Print the full path for debugging
print(f"🔍 Looking for model at: {MODEL_PATH}")

# Check if the file exists before loading
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# Load the trained stacking model
stacking_model = joblib.load(MODEL_PATH)

# Load the SBERT model for text embeddings
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")  # Adjust based on your model

cluster_map = {
    0: 'Tribal Affairs and Regional Violent Incidents',
    1: 'Celebrity News and Entertainment',
    2: 'Monetary and Financial Law Violations',
    3: 'Legal and Regulatory Violations',
    4: 'International Relations and Foreign Affairs',
    5: 'Social and Local News',
    6: 'Drug and Tobacco-Related Issues',
    7: 'Violent Crime Incidents',
    8: 'Corporate Affairs and Market Dynamics',
    9: 'Medical News and Advancements'
}

def classifier(text):
    try:
        # Convert text input to embeddings using SBERT
        text_embedding = sbert_model.encode([text])

        # Make predictions using the stacking model
        prediction = stacking_model.predict(text_embedding)
        print(type(prediction))
        return cluster_map[prediction[0]]
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500