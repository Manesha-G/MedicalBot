import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ✅ Load Dataset
dataset_path = "disease_symptom_specialist_dataset_500.csv"
df = pd.read_csv(dataset_path)

# ✅ Extract Symptoms and Disease Labels
X = df["Symptoms"]  # Input Features (Symptoms)
y = df["Disease"]   # Output Labels (Diseases)

# ✅ Load Trained Vectorizer & Model
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("disease_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

# ✅ Convert Symptoms to Vectors
X_vectorized = vectorizer.transform(X)

# ✅ Split Data into Train and Test Sets (80-20 Split)
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# ✅ Make Predictions on Test Data
y_pred = model.predict(X_test)

# ✅ Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ **Model Accuracy:** {accuracy * 100:.2f}%")

# ✅ Print Detailed Performance Report
print("\n📊 **Classification Report:**")
print(classification_report(y_test, y_pred))
