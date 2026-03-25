import joblib
import pandas as pd
from ml_model import extract, features_columns

model = joblib.load('phishing_model.pkl')

test_urls = [
    "https://www.google.com",
    "http://free-gift-now.ru",
    "https://secure-login-paypal.com",
    "https://www.wikipedia.org",
    "http://192.168.1.1/login",
    "https://paypal.com-verify-account.info/secure",
    "http://bit.ly/3xFakeLink",
    "https://www.amazon.com/orders"
]

X = pd.DataFrame([extract(url) for url in test_urls])[features_columns]
predictions = model.predict(X)

for url, pred in zip(test_urls, predictions):
    label = "⚠️  Phishing" if pred == 1 else "✅ Safe"
    print(f"{label}: {url}")