/**
 * script.js
 * Handles the user input, sends the URL to the Flask backend,
 * and updates the UI with the prediction result.
 */

// Define the API endpoint URL (must match the Flask route)
// FIX: Changed endpoint to match app.py route @app.route('/predict')
const API_URL = 'http://127.0.0.1:5000/predict';

// Get references to DOM elements
const form = document.getElementById('url-detection-form');
const urlInput = document.getElementById('url-input');
const resultDiv = document.getElementById('url-result');
const displayedUrlSpan = document.getElementById('displayed-url');
const predictedClassSpan = document.getElementById('predicted-class');
const messageBox = document.getElementById('message-box'); // Assuming you have a simple div for messages

// State to prevent multiple submissions
let isAnalyzing = false;

// --- Utility Functions ---

/**
 * Shows a temporary message in the message box.
 * @param {string} message The message to display.
 */
function showMessage(message) {
    messageBox.textContent = message;
    messageBox.style.display = 'block';
    messageBox.className = 'bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mb-4';
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 3000);
}


/**
 * Updates the result display with the prediction and corresponding style.
 * @param {string} url The URL that was classified.
 * @param {string} prediction The result text ('benign' or 'malicious' or 'ERROR').
 * @param {string} className The class name to apply for styling ('benign', 'malicious', or 'error').
 */
function updateResultDisplay(url, prediction, className) {
    // Clear previous classes
    predictedClassSpan.classList.remove('benign', 'malicious', 'error', 'analyzing');

    // Update text content
    displayedUrlSpan.textContent = url;
    predictedClassSpan.textContent = prediction;

    // Apply the new class for styling (green/red)
    predictedClassSpan.classList.add(className);

    // Make the result section visible
    resultDiv.style.display = 'block';
}

/**
 * Sets the display to the "Analyzing..." state.
 * @param {string} url The URL being processed.
 */
function setAnalyzingState(url) {
    updateResultDisplay(url, 'Analyzing...', 'analyzing');
    isAnalyzing = true;
    // Visually disable the button while waiting
    form.querySelector('.btn').disabled = true;
}

/**
 * Resets the state after analysis is complete (or failed).
 */
function resetState() {
    isAnalyzing = false;
    form.querySelector('.btn').disabled = false;
}


// --- Main Event Listener ---

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop the default form submission (page reload)

    if (isAnalyzing) {
        return; // Already processing
    }

    const url = urlInput.value.trim();

    if (!url) {
        // FIX: Use custom message box instead of alert()
        showMessage("Please enter a URL.");
        return;
    }

    // 1. Set the analyzing state
    setAnalyzingState(url);

    try {
        // 2. Send the URL data to the Flask API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                // IMPORTANT: Tells Flask to expect JSON
                'Content-Type': 'application/json',
            },
            // Convert the URL string into a JSON payload
            body: JSON.stringify({ url: url })
        });

        // Check for non-200 status codes (e.g., 404, 500)
        if (!response.ok) {
            // Read the server's error message if available
            const errorText = await response.text();
            // FIX: Ensure correct template literal usage (backticks `) here
            throw new Error(`HTTP error! Status: ${response.status}. Details: ${errorText}`);
        }

        // 3. Parse the JSON response
        const result = await response.json();

        // 4. Update the UI based on the response structure
        const prediction = result.prediction;
        const className = result.class_name; // Should be 'benign', 'malicious', or 'error'

        updateResultDisplay(url, prediction, className);

    } catch (error) {
        // Log the full error to the console for detailed debugging
        console.error('Fetch/Prediction Error:', error);

        // Inform the user that an error occurred
        updateResultDisplay(url, 'NETWORK ERROR: Check console for details.', 'error');

    } finally {
        // 5. Always reset the state (enable the button)
        resetState();
    }
});

// Initial setup to hide the result div
document.addEventListener('DOMContentLoaded', () => {
    resultDiv.style.display = 'none';
    messageBox.style.display = 'none'; // Ensure the new message box is hidden initially
});
