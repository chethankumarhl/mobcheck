import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# Load dataset
df = pd.read_csv("data/used_device_data.csv")

# Drop rows with missing values
df.dropna(inplace=True)

# Encode binary categorical columns like '4g' and '5g'
binary_columns = ["4g", "5g"]
for col in binary_columns:
    df[col] = df[col].map({"yes": 1, "no": 0})

# Encode other categorical columns
label_encoders = {}
categorical_columns = ["device_brand", "os"]
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
target_column = "normalized_used_price"
X = df.drop(columns=[target_column])
y = df[target_column]

# Optional: Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Store column order
feature_columns = X.columns.tolist()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Optional: Hyperparameter tuning (quick version)
param_grid = {
    'n_estimators': [100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}
model = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring='r2', n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"Best Parameters: {model.best_params_}")

# Save model and supporting files
os.makedirs("model", exist_ok=True)
joblib.dump(model.best_estimator_, "model/model.pkl")
joblib.dump(label_encoders, "model/label_encoders.pkl")
joblib.dump(feature_columns, "model/feature_columns.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model training complete! Artifacts saved to 'model/' directory.")
