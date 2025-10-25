# ml_model.py
import re
import pandas as pd

# ========================
# Feature extraction for a URL
# ========================
def extract(url):
    """
    Extract numeric features from a URL for phishing detection.
    Returns a dictionary of features.
    """
    return {
        'url_length': len(url),
        'count_dots': url.count('.'),
        'has_at': int('@' in url),
        'has_dash': int('-' in url),
        'has_double_slash': int('//' in url[8:]),  # skip https://
        'https_present': int(url.startswith('https')),
        'is_ip_address': int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", url))),
        'count_suspicious_chars': sum(url.count(c) for c in ['!', '$', '%', '&', '*', '?'])
    }

# ========================
# Correct feature order for the trained model
# ========================
features_columns = [
    'url_length', 'count_dots', 'has_at',
    'has_dash', 'has_double_slash', 'https_present',
    'is_ip_address', 'count_suspicious_chars'
]

# ========================
# Placeholder for model (loaded in app.py)
# ========================
model = None