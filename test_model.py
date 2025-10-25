import joblib
import pandas as pd
import re

# Load the trained model
model = joblib.load("phishing_model.pkl")

# --- Function to extract same features as before ---
def extract_features(url):
    return {
        "url_length": len(url),
        "count_dots": url.count("."),
        "has_at": int("@" in url),
        "has_dash": int("-" in url),
        "has_double_slash": int('//' in url[8:]),  # skip https://
        "https_present": int(url.startswith("https")),
        "is_ip_address": int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", url))),
        "count_suspicious_chars": sum(url.count(c) for c in ['!', '$', '%', '&', '*', '?'])
    }

# --- Test URLs ---
test_urls = [
    "https://www.google.com",
    "http://free-gift-now.ru",
    "https://secure-login-paypal.com",
    "https://www.wikipedia.org"
]

# Extract features into DataFrame
features_df = pd.DataFrame([extract_features(url) for url in test_urls])

# Predict using the trained model
predictions = model.predict(features_df)

# Display results
for url, pred in zip(test_urls, predictions):
    if pred == 1:
        print(f"⚠️ Phishing: {url}")
    else:
        print(f"✅ Safe: {url}")
