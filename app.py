from flask import Flask, request, jsonify
import pickle
import warnings
from flask_cors import CORS

# Suppress warnings about unsupported indices
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the model
MODEL_PATH = "model_odgj.pkl"
try:
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
        print(f"Model loaded successfully from '{MODEL_PATH}'.")
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' not found.")
    model = None


# Function to encode inputs
def encode_input(kecamatan, target):
    kecamatan_mapping = {
        "ANDIR": 0,
        "ANTAPANI": 1,
        "ARCAMANIK": 2,
        "ASTANAANYAR": 3,
        "BABAKAN CIPARAY": 4,
        "BANDUNG KIDUL": 5,
        "BANDUNG KULON": 6,
        "BANDUNG WETAN": 7,
        "BATUNUNGGAL": 8,
        "BOJONGLOA KALER": 9,
        "BOJONGLOA KIDUL": 10,
        "BUAHBATU": 11,
        "CIBEUNYING KALER": 12,
        "CIBEUNYING KIDUL": 13,
        "CIBIRU": 14,
        "CICENDO": 15,
        "CIDADAP": 16,
        "CINAMBO": 17,
        "COBLONG": 18,
        "GEDEBAGE": 19,
        "KIARACONDONG": 20,
        "LENGKONG": 21,
        "MANDALAJATI": 22,
        "PANYILEUKAN": 23,
        "RANCASARI": 24,
        "REGOL": 25,
        "SUKAJADI": 26,
        "SUKASARI": 27,
        "SUMUR BANDUNG": 28,
        "UJUNG BERUNG": 29,
    }
    target_mapping = {"odgj": 0, "pelayanan": 1}

    encoded_kecamatan = kecamatan_mapping.get(kecamatan.upper(), -1)
    encoded_target = target_mapping.get(target.lower(), -1)

    return encoded_kecamatan, encoded_target


# Function to map years to indices
def year_to_index(year, base_year=2024, base_index=29, interval=30):
    if year <= base_year:
        raise ValueError(f"Year must be above {base_year}.")
    return base_index + (year - base_year) * interval


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded."}), 500

    try:
        data = request.json
        year = int(data.get("year"))
        kecamatan = data.get("kecamatan")
        target = data.get("target")

        # Encode inputs
        encoded_kecamatan, encoded_target = encode_input(kecamatan, target)

        if encoded_kecamatan == -1 or encoded_target == -1:
            return jsonify({"error": "Invalid kecamatan or target value."}), 400

        # Map year to index
        year_index = year_to_index(year)

        # Perform prediction
        prediction = model.predict(start=year_index, end=year_index).tolist()
        return jsonify({"year": year, "prediction": prediction[0]})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {e}"}), 500


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
