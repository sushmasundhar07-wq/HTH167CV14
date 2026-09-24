import os
import sys
import json

from flask import Flask, request, jsonify, send_from_directory
from PIL import Image


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(BACKEND_DIR)

FRONTEND_DIR = os.path.join(
    PROJECT_DIR,
    "frontend"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "crop_disease_mobilenetv3.pth"
)

CLASS_NAMES_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "class_names.json"
)


# ============================================================
# MAKE SRC FOLDER AVAILABLE
# ============================================================

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


# ============================================================
# IMPORT YOUR CV / ML CODE
# ============================================================

from src.classifier import CropDiseaseClassifier
from src.preprocessing import get_validation_transform


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# LOAD CLASS NAMES
# ============================================================

print("Loading class names...")

with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:

    class_names = json.load(file)


# Support dictionary format
if isinstance(class_names, dict):

    try:

        class_names = [
            class_names[str(i)]
            for i in range(len(class_names))
        ]

    except KeyError:

        class_names = list(
            class_names.values()
        )


print(
    f"Classes loaded: {len(class_names)}"
)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading trained model...")

classifier = CropDiseaseClassifier(
    num_classes=len(class_names)
)

classifier.load_weights(
    MODEL_PATH
)


print("Model loaded successfully.")

print(
    f"Device: {classifier.device}"
)


# ============================================================
# FRONTEND HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )
    
@app.route("/style.css")
def style():
    return send_from_directory(
        FRONTEND_DIR,
        "style.css"
    )


@app.route("/script.js")
def script():
    return send_from_directory(
        FRONTEND_DIR,
        "script.js"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "success": True,

        "message":
            "Crop Disease Prediction API is running",

        "classes":
            len(class_names),

        "model_loaded":
            True,

        "device":
            str(classifier.device)

    })


# ============================================================
# PREDICTION API
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if "image" not in request.files:

        return jsonify({

            "success": False,

            "error":
                "No image was uploaded."

        }), 400


    file = request.files["image"]


    if file.filename == "":

        return jsonify({

            "success": False,

            "error":
                "No image was selected."

        }), 400


    try:

        # ----------------------------------------------------
        # OPEN IMAGE
        # ----------------------------------------------------

        image = Image.open(
            file
        ).convert("RGB")


        # ----------------------------------------------------
        # PREPROCESS IMAGE
        # ----------------------------------------------------

        transform = (
            get_validation_transform()
        )


        image_tensor = transform(
            image
        )


        # Add batch dimension

        image_tensor = (
            image_tensor.unsqueeze(0)
        )


        # ----------------------------------------------------
        # RUN CV / ML MODEL
        # ----------------------------------------------------

        disease, confidence = (
            classifier.predict(
                image_tensor,
                class_names
            )
        )


        # ----------------------------------------------------
        # SEND RESULT TO FRONTEND
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "prediction":
                disease,

            "confidence":
                confidence

        })


    except Exception as error:

        print(
            "Prediction error:"
        )

        print(error)


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("=" * 60)

    print(
        "CROP DISEASE PREDICTION SYSTEM"
    )

    print("=" * 60)

    print("")

    print(
        "Frontend:",
        FRONTEND_DIR
    )

    print(
        "Model:",
        MODEL_PATH
    )

    print(
        "Classes:",
        len(class_names)
    )

    print("")

    print(
        "Server starting..."
    )

    print(
        "Open: http://127.0.0.1:5000"
    )

    print("")


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )