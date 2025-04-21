from flask import Flask, render_template, request, url_for, redirect, session
import pandas as pd
import joblib
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'PASSWORD'  # Set a secret key for session management
app.config["MONGO_URI"] = "mongodb://localhost:27017/loginMobile"
mongo = PyMongo(app)

try:
    model = joblib.load("model/model.pkl")
    label_encoders = joblib.load("model/label_encoders.pkl")
    scaler = joblib.load("model/scaler.pkl")  
    feature_columns = joblib.load("model/feature_columns.pkl")
except Exception as e:
    print("Error loading model assets:", e)
    model, label_encoders, scaler, feature_columns = None, None, None, None

INR_to_EUR = 0.011

@app.route('/')
def index():
    reviews = mongo.db.reviews.find()  
    return render_template('index.html', reviews=reviews,session=session)

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        title = request.form.get('title')
        review_content = request.form.get('review')
        rating = request.form.get('rating')
        word_count = len(review_content.strip().split())
        if word_count > 100:
            error = "Review must be 100 words or fewer."
            return render_template("review.html", error=error)

        # Insert review into the database
        mongo.db.reviews.insert_one({
            "username": username,
            "title": title,
            "review": review_content,
            "rating": rating
        })

        # Redirect to a page (e.g., the home page or review listing page)
        return redirect(url_for('index'))  # Or wherever you want to go after submission

    # If it's a GET request, render the review submission page
    return render_template('review.html')

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    
    return render_template('main.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Conversion rate
        INR_to_EUR = 0.011  # Update if necessary

        # Get form data
        input_data = {
            "device_brand": request.form["device_brand"].strip().title(),
            "os": request.form["os"].strip().title(),
            "4g": int(request.form["4g"].lower() == "yes"),
            "5g": int(request.form["5g"].lower() == "yes"),
            "screen_size": float(request.form["screen_size"]),
            "rear_camera_mp": float(request.form["rear_camera_mp"]),
            "front_camera_mp": float(request.form["front_camera_mp"]),
            "internal_memory": int(request.form["internal_memory"]),
            "ram": int(request.form["ram"]),
            "battery": int(request.form["battery"]),
            "weight": float(request.form["weight"]),
            "release_year": int(request.form["release_year"]),
            "days_used": int(request.form["days_used"]),
            "normalized_new_price": float(request.form["normalized_new_price"]) * INR_to_EUR
        }

        # Handle label encoding for categorical features
        for col in ["device_brand", "os"]:
            if input_data[col] in label_encoders[col].classes_:
                input_data[col] = label_encoders[col].transform([input_data[col]])[0]
            else:
                input_data[col] = label_encoders[col].transform(['Others'])[0]

        # Create DataFrame and align column order
        input_df = pd.DataFrame([input_data])[feature_columns]

        # Scale input
        input_scaled = scaler.transform(input_df)

        # Predict price in normalized euro (already scaled by 10)
        predicted_euro = model.predict(input_scaled)[0]

        # Convert back to INR
        final_price_inr = predicted_euro * 10 / INR_to_EUR * 2

        return render_template("main.html", prediction_text=f"Predicted Price: ₹{final_price_inr:.2f}")

    except Exception as e:
        return render_template("main.html", prediction_text=f"Error occurred: {str(e)}")


@app.route('/loginp')
def loginp():
    return render_template('login.html')


@app.route('/registerp')
def reg_page():
    return render_template('register.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        mobileno = request.form.get("mobilenumber")

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"mobilenumber": mobileno}]})
        
        if existing_user:
            # If username or mobile number already exists, show error
            return render_template('login.html', error="Username or Mobile Number already exists.")
        
        # Insert the new user into the database
        mongo.db.users.insert_one({"username": username, "password": password, "mobilenumber": mobileno})

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        session['user'] = True
        # Check if user exists with the provided username and password
        existing_user = mongo.db.users.find_one({"username": username, "password": password})
        
        if existing_user:
            # If user exists, store user id in session to track login status
            session['user_id'] = existing_user['_id']
            return redirect(url_for('index'))  # Redirect to home page or dashboard
        
        # If username or password is incorrect, show error
        return render_template('login.html', error="Username or Password is incorrect.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))  # Use the function name, NOT the route string

if __name__ == '__main__':
    app.run(debug=True)
