import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load the generated CSV
df = pd.read_csv('student_data.csv')

# Encode 'Pass'/'Fail' as 1/0
le = LabelEncoder()
df['final_result_encoded'] = le.fit_transform(df['final_result'])

# Select features and label
X = df[['attendance_percent', 'internal_marks', 'past_sem_marks']]
y = df['final_result_encoded']

# Split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save for next step
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("✅ Data preprocessing completed and saved.")
