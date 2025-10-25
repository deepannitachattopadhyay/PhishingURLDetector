# Phishing URL Detector (Flask + ML)

A web application to detect phishing URLs using a machine learning model.  
Built with **Python**, **Flask**, **scikit-learn**, and **pandas**.

---

## Features

- Predict if a URL is **malicious** or **benign**.
- Uses numeric features extracted from URLs.
- Web interface powered by **Flask**.
- API endpoint available for programmatic access.

---

## Project Structure
PhishingURLDetector/
│
├─ app.py # Flask app
├─ ml_model.py # Feature extraction logic
├─ phishing_model.pkl # Trained ML model
├─ templates/
│ └─ index.html # Frontend HTML
├─ static/
│ ├─ style.css
│ └─ script.js
├─ test_model.py # Test script for URLs
├─ requirements.txt # Python dependencies
└─ README.md


---

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/deepannitachattopadhyay/PhishingURLDetector.git
cd PhishingURLDetector

### Setup Dependencies
pip install -r requirements.txt

### Run the Flask app
python app.py

Open your browser at http://127.0.0.1:5000 to use the app
