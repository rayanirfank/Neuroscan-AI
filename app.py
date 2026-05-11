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

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model(
    "brain_tumor_model.keras",
    compile=False
)

classes = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary"
]

@app.route('/')

def home():

    return render_template("Dashboard.html")


@app.route('/about')

def about():

    return render_template("About.html")


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
                "error": "No file selected"
            }), 400

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(file_path)

        img = image.load_img(
            file_path,
            target_size=(240, 240)
        )

        img_array = image.img_to_array(img)

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        img_array = preprocess_input(img_array)

        prediction = model.predict(
            img_array,
            verbose=0
        )

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

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == '__main__':

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host='0.0.0.0',
        port=port
    )