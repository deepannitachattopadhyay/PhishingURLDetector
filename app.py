from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
from ml_model import extract, features_columns  # ✅ import correct ones

app = Flask(__name__)
CORS(app)

# Load Model
model = joblib.load('phishing_model.pkl')
print("✅ Model loaded successfully!")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def classify_url():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # ✅ correct feature extraction + ordering
        features_dict = extract(url)
        features_df = pd.DataFrame([features_dict])[features_columns]

        # ✅ Proper prediction
        prediction = model.predict(features_df)[0]
        result = "malicious" if int(prediction) == 1 else "benign"

        return jsonify({
            "url": url,
            "prediction": result,
            "class_name": result
        })

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)