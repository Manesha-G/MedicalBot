from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
CORS(app)

# ✅ Load Model & Vectorizer
with open("disease_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ✅ Dummy Specialist Mapping
specialist_mapping = {
    "Flu": "General Physician",
    "Diabetes": "Endocrinologist",
    "Heart Attack": "Cardiologist",
}

def get_specialist(disease):
    return specialist_mapping.get(disease, "General Physician")

# ✅ Your Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyCABvpfto6a6HVUgu2E3WQeXi6fxu3UgZI"

# ✅ Predict Disease Route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        symptoms = data.get("symptoms", "").strip().lower()

        if not symptoms:
            return jsonify({"error": "No symptoms provided", "diseases": []}), 400

        user_features = vectorizer.transform([" ".join(symptoms.split(", "))])
        disease_probs = model.predict_proba(user_features)[0]
        disease_indices = disease_probs.argsort()[-3:][::-1]

        predicted_diseases = [
            {"name": model.classes_[i], "confidence": f"{disease_probs[i] * 100:.2f}%"}
            for i in disease_indices
        ]

        if not predicted_diseases:
            return jsonify({"error": "No diseases found. Try different symptoms.", "diseases": []}), 400

        specialist = get_specialist(predicted_diseases[0]["name"])

        return jsonify({
            "diseases": predicted_diseases,
            "specialist": specialist
        })

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}", "diseases": []}), 500

# ✅ New Route to Find Nearby Hospitals
@app.route("/find_hospitals", methods=["POST"])
def find_hospitals():
    try:
        data = request.json
        pincode = data.get("pincode")
        specialist = data.get("specialist", "doctor")

        # ✅ Convert PIN code to lat/lng using Geocoding API
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={pincode}&key={GOOGLE_MAPS_API_KEY}"
        geo_res = requests.get(geo_url).json()

        if geo_res["status"] != "OK":
            return jsonify({"error": "Invalid PIN code", "hospitals": []})

        location = geo_res["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        # ✅ Search for hospitals/specialists near location
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&keyword={specialist}&key={GOOGLE_MAPS_API_KEY}"
        places_res = requests.get(places_url).json()

        hospitals = []
        for place in places_res.get("results", []):
            hospitals.append({
                "name": place.get("name"),
                "address": place.get("vicinity")
            })

        return jsonify({"hospitals": hospitals})

    except Exception as e:
        return jsonify({"error": f"Failed to find hospitals: {str(e)}", "hospitals": []}), 500

@app.route("/")
def home():
    return "✅ Flask server is running!"

if __name__ == "__main__":
    print("\n🚀 Flask Server Running!")
    app.run(host="127.0.0.1", port=5000, debug=True)
