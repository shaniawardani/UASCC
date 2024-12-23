import pickle
import warnings

# Suppress warnings about unsupported indices
warnings.filterwarnings("ignore", category=FutureWarning)

# Load the model
MODEL_PATH = "model_odgj.pkl"
try:
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
        print(f"Model loaded successfully from '{MODEL_PATH}'.")
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' not found.")
    exit(1)


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

    # Allow numeric inputs
    if isinstance(kecamatan, int):
        if kecamatan in kecamatan_mapping.values():
            encoded_kecamatan = kecamatan
        else:
            encoded_kecamatan = -1
    else:
        encoded_kecamatan = kecamatan_mapping.get(kecamatan.upper(), -1)

    if isinstance(target, int):
        if target in target_mapping.values():
            encoded_target = target
        else:
            encoded_target = -1
    else:
        encoded_target = target_mapping.get(target.lower(), -1)

    return encoded_kecamatan, encoded_target


# Function to map years to indices
def year_to_index(year, base_year=2025, base_index=29, interval=30):
    """
    Convert a year to the corresponding integer index for the model.
    """
    if year <= base_year:
        raise ValueError(f"Year must be above {base_year}.")
    return base_index + (year - base_year) * interval


# Function to predict mental health cases for a single year
def predict_mental_health(model, year, kecamatan, target):
    encoded_kecamatan, encoded_target = encode_input(kecamatan, target)

    if encoded_kecamatan == -1 or encoded_target == -1:
        return "Invalid kecamatan or target value."

    try:
        # Map the year to the corresponding index
        base_year = 2025
        base_index = 29
        interval = 30

        year_index = year_to_index(year, base_year, base_index, interval)

        # Perform prediction
        prediction = model.predict(start=year_index, end=year_index).tolist()
        return f"Prediction for {year}: {prediction[0]:.2f}"
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Error during prediction: {e}"


# Main program
if __name__ == "__main__":
    print("=== Mental Health Prediction App ===")
    print("Predict mental health cases for years above 2025.")

    while True:
        try:
            year = int(input("Enter the prediction year (e.g., 2026): ").strip())
            kecamatan = input(
                "Enter the kecamatan (name or number, e.g., ANDIR or 1): "
            ).strip()
            target = input(
                "Enter the target (name or number, e.g., odgj or 1): "
            ).strip()

            # Convert numeric inputs to integers if applicable
            if kecamatan.isdigit():
                kecamatan = int(kecamatan)
            if target.isdigit():
                target = int(target)

            result = predict_mental_health(model, year, kecamatan, target)
            print(result)

            again = (
                input("Do you want to make another prediction? (yes/no): ")
                .strip()
                .lower()
            )
            if again != "yes":
                print("Exiting the app. Goodbye!")
                break
        except KeyboardInterrupt:
            print("\nExiting the app. Goodbye!")
            break
        except ValueError as ve:
            print(f"Input Error: {ve}")
