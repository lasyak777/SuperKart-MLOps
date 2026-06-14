
# Standard library
from pathlib import Path
import logging
import sys

# Third-party libraries
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Initialize Flask app
superkart_api = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Locate and load the trained model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "superkart_sales_forecast_model.joblib"

logger.info(f"Loading model from {MODEL_PATH}")

model = joblib.load(MODEL_PATH)


@superkart_api.route("/", methods=["GET"])
def home():
    """
    Home endpoint.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SuperKart Sales Prediction API</title>
    </head>
    <body>
        <h1>Welcome to the SuperKart Sales Prediction API</h1>
        <p>Submit a POST request to <code>/v1/predict</code> to obtain sales predictions.</p>
    </body>
    </html>
    """


@superkart_api.route("/v1/predict", methods=["POST"])
def predict_sales():
    """
    Predict total sales for a product.
    """
    try:
        data = request.get_json()

        sample = {
            "Product_Weight": data["Product_Weight"],
            "Product_Sugar_Content": data["Product_Sugar_Content"],
            "Product_Allocated_Area": data["Product_Allocated_Area"],
            "Product_MRP": data["Product_MRP"],
            "Store_Size": data["Store_Size"],
            "Store_Location_City_Type": data["Store_Location_City_Type"],
            "Store_Type": data["Store_Type"],
            "Store_Age_Years": data["Store_Age_Years"],
            "Product_Type_Category": data["Product_Type_Category"],
            "Product_Id_char": data["Product_Id_char"],
        }

        input_df = pd.DataFrame([sample])

        prediction = float(model.predict(input_df)[0])

        return jsonify(
            {
                "predicted_sales": prediction
            }
        )

    except KeyError as e:
        logger.exception("Missing input feature.")
        return jsonify(
            {
                "error": f"Missing required field: {e}"
            }
        ), 400

    except Exception as e:
        logger.exception("Prediction failed.")
        return jsonify(
            {
                "error": str(e)
            }
        ), 500


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=5000, debug=False)
