# 📱 MobCheck – Used Mobile Price Estimator

MobCheck is a full-stack machine learning-powered web application designed to estimate the resale value of used mobile phones based on brand, technical specifications, and usage. Built with **Flask**, integrated with **MongoDB Atlas**, and deployed on **Render**, the app also allows users to register, log in, and submit reviews, creating a complete and interactive experience.

🔗 **Live Demo:** [mobcheck.onrender.com](https://mobcheck.onrender.com)

---

## 🚀 Project Features

- 📊 **Price Prediction:** Uses a trained Random Forest Regressor model to predict used mobile prices based on key features.
- 🧠 **Machine Learning Integration:** Model trained using real-world data from Kaggle, including preprocessing, scaling, and label encoding.
- 🔐 **User Authentication:** Login and registration functionality using secure session management.
- 📝 **Review System:** Users can submit reviews and ratings that are stored in MongoDB Atlas and displayed in real time.
- 🌐 **Deployment Ready:** End-to-end deployment using Render with integrated .env for secure configuration.

---

## 📁 Dataset

- **Source:** [Kaggle – Used Mobile Phone Dataset](https://www.kaggle.com/datasets)
- **Features:** Device brand, OS, screen size, memory, camera specs, battery, weight, release year, days used, etc.
- **Target:** Normalized used price (predicted in INR using conversion logic)

---

## 🔍 ML Model

- **Algorithm:** Random Forest Regressor
- **Accuracy:** ~92% (R² score)
- **Preprocessing:** Label encoding (for categorical data), feature scaling, PCA (optional)
- **Saved Assets:** `model.pkl`, `scaler.pkl`, `label_encoders.pkl`, `feature_columns.pkl`

---

## 🔧 Tech Stack

| Layer        | Technology Used                        |
|--------------|-----------------------------------------|
| Frontend     | HTML, CSS (Bootstrap), JavaScript       |
| Backend      | Python, Flask                           |
| Database     | MongoDB Atlas (Cloud NoSQL DB)          |
| Machine Learning | Scikit-learn, Pandas, Joblib       |
| Deployment   | Render                                  |
| Others       | Gunicorn, dotenv, Jinja2 Templates      |

---

## 🔄 App Flow

1. **User registers or logs in**
2. **Home page displays recent user reviews**
3. **User visits main prediction page**
4. **Inputs mobile phone details → ML model predicts resale price**
5. **User can submit a review which gets stored in MongoDB Atlas**
6. **All predictions and reviews are visible in real-time**

---

## 🖼️ Screenshots

> Add screenshots of your app's home page, login form, prediction form, and result page for better visuals.

---

## 📂 Project Structure

mobcheck/
│
├── model/ # Saved ML model files
├── static/ # CSS and JS assets
├── templates/ # HTML templates (Jinja2)
├── app.py # Flask app
├── train_model.py # ML training and saving script
├── requirements.txt # Python dependencies
├── Procfile # For deployment on Render/Heroku
├── .env # Environment variables (Mongo URI, secret key)
└── README.md # Project documentation



---

## ⚙️ Installation & Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/mobcheck.git
cd mobcheck

# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up .env file (MongoDB URI, secret key)
# Example:
# MONGO_URI="your_mongodb_atlas_uri"
# SECRET_KEY="your_secret_key"

# Run ML training (only once)
python train_model.py

# Start the Flask app
python app.py
```

##🌐 Deployment
Deployed on Render

Use Procfile with web: gunicorn app:app

Environment variables handled using .env

MongoDB hosted on MongoDB Atlas

##👨‍💻 Author
Chethan Kumar H L

A passionate developer with a focus on machine learning, web development, and practical deployment of ML models.
