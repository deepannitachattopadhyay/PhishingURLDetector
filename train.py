import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from ml_model import extract, features_columns

df = pd.read_csv('dataset.csv')
df = df.dropna(subset=['url'])

print(f"Dataset size: {len(df)} rows")
print("Extracting features from raw URLs...")

X = pd.DataFrame(list(df['url'].apply(extract)))[features_columns]
y = (df['status'] == 'phishing').astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"✅ Accuracy:  {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(f"✅ Precision: {precision_score(y_test, y_pred) * 100:.2f}%")
print(f"✅ Recall:    {recall_score(y_test, y_pred) * 100:.2f}%")
print(f"✅ F1 Score:  {f1_score(y_test, y_pred) * 100:.2f}%")

joblib.dump(model, 'phishing_model.pkl')
print("✅ Model saved!")