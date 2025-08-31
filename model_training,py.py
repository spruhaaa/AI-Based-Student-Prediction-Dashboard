import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load training data
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv")
y_test = pd.read_csv("y_test.csv")

# Train model
model = XGBClassifier()
model.fit(X_train, y_train.values.ravel())

# Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "student_model.pkl")
print("✅ Model saved as student_model.pkl")
