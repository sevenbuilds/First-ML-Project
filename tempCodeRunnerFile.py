from flask import Flask, jsonify, request, render_template
from ml_model import predict_image

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error: no image provided"}), 400
    image = request.files["image"]

    try: 
        digit, accuracy = predict_image(image.read())
        return jsonify({
            "prediction": digit,
            "accuracy": accuracy
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
