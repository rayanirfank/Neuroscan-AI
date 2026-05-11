from flask import (
    Flask,
    request,
    jsonify,
    render_template
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

# Home route

@app.route('/')

def home():

    return render_template("Dashboard.html")

# About route

@app.route('/about')

def about():

    return render_template("About.html")

# Upload + Prediction route

@app.route('/upload', methods=['POST'])

def upload_image():

    try:

        if 'file' not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files['file']

        if file.filename == '':

            return jsonify({
                "error": "Empty filename"
            }), 400

        # Save uploaded file

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(file_path)

        # Load image

        img = image.load_img(
            file_path,
            target_size=(240, 240)
        )

        # Convert image to array

        img_array = image.img_to_array(img)

        # Expand dimensions

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        # Preprocess image

        img_array = preprocess_input(img_array)

        # Model prediction

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

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({

            "error": str(e)

        }), 500

# Run app

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )