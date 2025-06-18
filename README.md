# 🩺 MedicalBot - AI-Powered Medical Chatbot

**MedicalBot** is an intelligent AI chatbot that accepts symptoms through **text or voice**, predicts possible **diseases**, recommends the appropriate **specialist**, and optionally shows **nearby hospitals** based on the user’s pincode using the **Google Maps API**.

🔗 **Live Repository:** [github.com/Manesha-G/MedicalBot](https://github.com/Manesha-G/MedicalBot)

---

## 🚀 Features

- ✅ Symptom input via **Text and Speech** (Google Speech API)
- ✅ Disease prediction using ML models: **Random Forest**, **SVM**, and **LSTM**
- ✅ NLP-powered symptom processing using **NLTK**
- ✅ **Specialist recommendation** based on predicted disease
- ✅ **Nearby hospital locator** using **Google Maps API**
- ✅ Clean frontend using **HTML, CSS, JavaScript**
- ✅ Backend with **Flask**, **MySQL**, and **scikit-learn**

---

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask), MySQL
- **ML Libraries:** Scikit-learn, TensorFlow/Keras, NLTK
- **APIs:** Google Maps API, Google Speech-to-Text API
- **Models:** Random Forest, Support Vector Machine (SVM), LSTM

---

📸 Screenshots
 ### CHATBOT PAGE
(https://github.com/Manesha-G/MedicalBot/blob/main/Medicalbotpage.jpeg)


### DISEASE PREDICTION
(https://github.com/Manesha-G/MedicalBot/blob/main/Diseaseprediction.jpeg)


### SPECIALIST RECOMMENDATION
( https://github.com/Manesha-G/MedicalBot/blob/main/Diseaseprediction.jpeg)


### PINCODE INPUT ANG NEARBY SPECIALIST RECOMMENDED
(https://github.com/Manesha-G/MedicalBot/blob/main/PincodeInput.jpeg)



## 📁 Project Structure

MedicalBot/
│
├── MedicalBot/
├── index.html
├── styles.css
|__ script.js
|__speech_to_text_disease_disease.py
├── disease_prediction_model.pkl
├── disease_symptom_specialist_dataset_500
├── evaluate_model.py
├── server.py
|__vectorizer.pkl
|__readme.md(about the project)

---

## ⚙️ Setup Instructions

🔹 1. Clone the Repository

```bash
git clone https://github.com/Manesha-G/MedicalBot.git
cd MedicalBot

🔹 2. Create and Activate a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate      # On Windows use: venv\Scripts\activate

🔹 3. Install Dependencies
pip install -r requirements.txt

🔹 4. Install NLTK Resources
import nltk
nltk.download('punkt')
nltk.download('wordnet')

🔹 5. Set Up the MySQL Database
Open your MySQL client
Create a database, e.g., medicalbot_db
Run the SQL scripts you used to create user data, symptoms table, specialist mapping, etc.
Update DB credentials inside server.py or a config file.


🔹 6. Configure Google APIs!

***Create API keys from:
Google Speech API
Google Maps Platform
***Replace placeholder API keys in the appropriate part of your code (server.py or config file).

🔹 7. Run the Flask App
python server.py

🔹 8. Open in Browser
http://127.0.0.1:5000
![1O](https://github.com/user-attachments/assets/4a822e06-6b06-4542-b92d-a86d3f680db5)



##🧪 How It Works
1.User enters symptoms using a form or speaks using voice input.
2.Input is cleaned and processed using NLTK and vectorized using TF-IDF.
3.The processed data is passed to ML models (Random Forest, SVM, LSTM).
4.The predicted disease is mapped to a specialist type.
5.If pincode is provided, Google Maps API fetches nearby hospitals/specialists.
6.Final output is displayed with disease, specialist, and location info.



📚 Future Enhancements
✅ Multilingual input support
✅ Mobile-responsive UI
❌ Appointment scheduling feature (planned)
❌ Integration with government health APIs (planned)


🤝 Contribution
Feel free to fork this repo, raise issues, or submit pull requests.



👩‍💻 Author
Manesha G
GitHub: @Manesha-G
Email: maneshagold@gmail.com




