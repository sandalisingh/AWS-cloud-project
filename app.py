from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from PIL import Image
import pickle
import io
import os
try:
    import tflite_runtime.interpreter as tflite # for EC2
except ImportError:
    import tensorflow as tf # for MAC
    tflite = tf.lite
import requests
import psycopg2

DB_CONFIG = {
    "host": "database-for-projects.cx2ai206wfec.eu-north-1.rds.amazonaws.com",
    "database": "postgres",
    "user": "sandalisingh",
    "password": "password",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_URL = "https://sandali-project.s3.eu-north-1.amazonaws.com/flower_model.tflite"
CLASS_URL = "https://sandali-project.s3.eu-north-1.amazonaws.com/class_indices.pkl"

MODEL_PATH = os.path.join(BASE_DIR, "flower_model.tflite")
CLASS_PATH = os.path.join(BASE_DIR, "class_indices.pkl")

def download_file(url, path):
    if not os.path.exists(path):
        print(f"Downloading {path}...")
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)

download_file(MODEL_URL, MODEL_PATH)
download_file(CLASS_URL, CLASS_PATH)

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open(os.path.join(BASE_DIR, "class_indices.pkl"), "rb") as f:
    class_indices = pickle.load(f)

index_to_class = {v: k for k, v in class_indices.items()}
IMAGE_SIZE = (224, 224)


def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMAGE_SIZE)
    image = np.array(image, dtype=np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_bytes = request.files["image"].read()
    image = preprocess_image(image_bytes)

    interpreter.set_tensor(input_details[0]["index"], image)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]["index"])
    idx = int(np.argmax(output))
    confidence = float(output[0][idx])
    flower = index_to_class[idx]

    # Store in RDS
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (flower_name, confidence) VALUES (%s, %s)",
        (flower, confidence)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "prediction": flower,
        "confidence": round(confidence, 4)
    })

@app.route("/history")
def history():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT flower_name, confidence, created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)