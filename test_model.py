import joblib
import pandas as pd
import re

model = joblib.load("phishing_model.pkl")

def extract_features(url):
    return {
        "url_length": len(url),
        "count_dots": url.count("."),
        "has_at": int("@" in url),
        "has_dash": int("-" in url),
        "has_double_slash": int('//' in url[8:]),
        "https_present": int(url.startswith("https")),
        "is_ip_address": int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", url))),
        "count_suspicious_chars": sum(url.count(c) for c in ['!', '$', '%', '&', '*', '?'])
    }

test_urls = [
    "https://www.google.com",
    "http://free-gift-now.ru",
    "https://secure-login-paypal.com",
    "https://www.wikipedia.org"
]

features_df = pd.DataFrame([extract_features(url) for url in test_urls])

predictions = model.predict(features_df)

for url, pred in zip(test_urls, predictions):
    if pred == 1:
        print(f"⚠️ Phishing: {url}")
    else:
        print(f"✅ Safe: {url}")