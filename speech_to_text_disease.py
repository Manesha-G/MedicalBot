import speech_recognition as sr
import pickle
import pandas as pd
import re
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ Load Dataset
dataset_path = "disease_symptom_specialist_dataset_500.csv"  # Updated to use 1000+ dataset
df = pd.read_csv(dataset_path)

# ✅ Load Trained Model
with open("disease_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ✅ Load Disease-to-Specialist Mapping
specialist_mapping = dict(zip(df["Disease"], df["Specialist"]))

# ✅ Function to Preprocess Symptoms
def preprocess_symptoms(symptoms, known_symptoms):
    symptoms = re.sub(r'[^a-zA-Z, ]', '', symptoms).lower().split(", ")
    matched_symptoms = [process.extractOne(sym, known_symptoms)[0] if process.extractOne(sym, known_symptoms)[1] > 80 else sym for sym in symptoms]
    return matched_symptoms if matched_symptoms else None  # Return None if no valid symptoms are found

# ✅ Load Symptoms List
known_symptom_list = df['Symptoms'].unique().tolist()

# ✅ Function to Record and Convert Speech to Text
def record_speech(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"🎤 {prompt}")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        print(f"📝 Recognized Symptoms: {recognized_text}")
        return recognized_text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand the audio. Please try again.")
        return None
    except sr.RequestError:
        print("❌ API request failed. Check internet connection.")
        return None

# ✅ Chatbot Function
def chatbot():
    print("\n💬 Welcome to the AI Medical Chatbot! 💬")

    # ✅ Step 1: Choose Input Mode
    input_mode = input("Type 'voice' to use voice input, or press Enter for text input: ").lower()

    if input_mode == "voice":
        # Record and convert speech to text for initial symptoms
        user_input = record_speech("Speak your symptoms clearly for prediction.")
    else:
        user_input = input("Enter symptoms: ")

    # ✅ Step 2: Process the Input and Predict Disease
    if user_input:
        user_symptoms = preprocess_symptoms(user_input, known_symptom_list)

        if user_symptoms:
            user_features = vectorizer.transform([" ".join(user_symptoms)])
            possible_diseases = model.predict_proba(user_features)[0]
            disease_indices = possible_diseases.argsort()[-3:][::-1]  # Get top 3 possible diseases
            predicted_diseases = [model.classes_[i] for i in disease_indices]
            predicted_probabilities = [possible_diseases[i] * 100 for i in disease_indices]  # Convert to %

            print("\n✅ **Possible Diseases and Confidence Levels:**")
            for disease, prob in zip(predicted_diseases, predicted_probabilities):
                print(f"🔹 {disease} ({prob:.2f}% confidence)")

            # ✅ Step 3: Ask for additional symptoms (voice input if 'voice' selected)
            extra_symptoms = ""
            if input_mode == "voice":
                extra_symptoms = record_speech("Please provide additional symptoms for more accurate prediction.")  # Use speech input for additional symptoms
            else:
                extra_symptoms = input("\n💬 Please enter additional symptoms for a more accurate prediction: ")

            extra_symptoms_processed = preprocess_symptoms(extra_symptoms, known_symptom_list) if extra_symptoms else None

            if extra_symptoms_processed:
                final_features = vectorizer.transform([" ".join(user_symptoms + extra_symptoms_processed)])
                final_disease_probs = model.predict_proba(final_features)[0]
                final_disease_index = final_disease_probs.argmax()
                final_disease = model.classes_[final_disease_index]
                final_accuracy = final_disease_probs[final_disease_index] * 100

                print(f"\n✅ **Final Predicted Disease:** {final_disease} ({final_accuracy:.2f}% confidence)")

                # ✅ Step 4: Ask if the user wants to know the specialist
                choice = input("\n💬 Do you want to know which specialist to consult? (yes/no): ").strip().lower()
                if choice == "yes":
                    recommended_specialist = specialist_mapping.get(final_disease, "General Physician")
                    print(f"🩺 **Recommended Specialist:** {recommended_specialist}")
                else:
                    print("✅ Exiting the chatbot. Stay healthy!")

            else:
                print("\n⚠ No additional symptoms provided. Proceeding with initial prediction.")
                recommended_specialist = specialist_mapping.get(predicted_diseases[0], "General Physician")
                print(f"🩺 **Recommended Specialist:** {recommended_specialist}")

        else:
            print("⚠ No valid symptoms detected. Please try again.")
    else:
        print("⚠ No input detected. Please try again.")

# ✅ Run the Chatbot
chatbot()
