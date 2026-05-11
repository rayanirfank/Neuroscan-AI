from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

import os
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

app = Flask(__name__)

CORS(app)

# Upload folder

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load trained model

model = load_model("brain_tumor_model.keras")

# Class labels

classes = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary"
]

# Dashboard route

@app.route('/')

def home():

    return send_from_directory('.', 'Dashboard.html')

# About page route

@app.route('/About.html')

def about():

    return send_from_directory('.', 'About.html')

# Upload prediction route

@app.route('/upload', methods=['POST'])

def upload_image():

    if 'file' not in request.files:

        return jsonify({
            "error": "No file uploaded"
        })

    file = request.files['file']

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    # Load image

    img = image.load_img(
        file_path,
        target_size=(240,240)
    )

    # Convert image to array

    img_array = image.img_to_array(img)

    # Expand dimensions

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # EfficientNet preprocessing

    img_array = preprocess_input(img_array)

    # Prediction

    prediction = model.predict(img_array)

    predicted_class = classes[
        np.argmax(prediction)
    ]

    confidence = float(
        np.max(prediction) * 100
    )

    return jsonify({

        "prediction": predicted_class,

        "confidence": round(confidence, 2)

    })

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )