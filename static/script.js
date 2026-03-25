const API_URL = 'http://127.0.0.1:5000/predict';

const form = document.getElementById('url-detection-form');
const urlInput = document.getElementById('url-input');
const resultDiv = document.getElementById('url-result');
const displayedUrlSpan = document.getElementById('displayed-url');
const predictedClassSpan = document.getElementById('predicted-class');

let isAnalyzing = false;

function updateResultDisplay(url, prediction, className) {
    predictedClassSpan.classList.remove('benign', 'malicious', 'error', 'analyzing');
    displayedUrlSpan.textContent = url;
    predictedClassSpan.textContent = prediction;
    predictedClassSpan.classList.add(className);
    resultDiv.style.display = 'block';
}

function setAnalyzingState(url) {
    updateResultDisplay(url, 'Analyzing...', 'analyzing');
    isAnalyzing = true;
    form.querySelector('.btn').disabled = true;
}

function resetState() {
    isAnalyzing = false;
    form.querySelector('.btn').disabled = false;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (isAnalyzing) return;

    const url = urlInput.value.trim();

    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    setAnalyzingState(url);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}. Details: ${errorText}`);
        }

        const result = await response.json();
        updateResultDisplay(url, result.prediction, result.class_name);

    } catch (error) {
        console.error('Fetch/Prediction Error:', error);
        updateResultDisplay(url, 'NETWORK ERROR: Check console for details.', 'error');

    } finally {
        resetState();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    resultDiv.style.display = 'none';
});