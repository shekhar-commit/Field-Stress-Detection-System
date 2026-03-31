from flask import Flask, render_template, request
import pandas as pd
import joblib
from utils.preprocessing import build_zone_input, get_recommendation_from_prediction

app = Flask(__name__)

# ============================
# LOAD TRAINED MODELS
# ============================
zone_status_model = joblib.load("zone_status_model.pkl")
zone_health_model = joblib.load("zone_health_score_model.pkl")


# ============================
# HOME PAGE
# ============================
@app.route("/")
def home():
    return render_template("index.html")


# ============================
# PREDICT SINGLE ZONE
# ============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input
        form_data = request.form.to_dict()

        # Convert into model-ready input
        final_input = build_zone_input(form_data)
        input_df = pd.DataFrame([final_input])

        # Predictions
        pred_status = zone_status_model.predict(input_df)[0]
        pred_health = zone_health_model.predict(input_df)[0]
        recommendation = get_recommendation_from_prediction(pred_status, pred_health)

        # Reasons
        reasons = []

        if final_input['soil_moisture'] < 20:
            reasons.append("Soil moisture is too low")

        if final_input['temperature_c'] > 35:
            reasons.append("Temperature is high")

        if final_input['humidity_percent'] < 40:
            reasons.append("Humidity is low")

        if final_input['ndvi_score'] < 0.4:
            reasons.append("Vegetation health is weak (low NDVI)")

        if final_input['fertilizer_deficiency_score'] > 0.7:
            reasons.append("Nutrient deficiency is high")

        if final_input['irrigation_score'] > 0.7:
            reasons.append("Irrigation demand is high")

        if final_input['waterlogging_risk'] == 'high':
            reasons.append("Waterlogging risk is high")

        if final_input['disease_risk_score'] > 0.7:
            reasons.append("Disease risk is high")

        if len(reasons) == 0:
            reasons.append("Zone conditions are mostly balanced")

        result = {
            "zone_status": pred_status,
            "health_score": round(float(pred_health), 2),
            "recommendation": recommendation,
            "crop_type": final_input['crop_type'],
            "crop_stage": final_input['crop_stage'],
            "soil_type": final_input['soil_type'],
            "soil_moisture": final_input['soil_moisture'],
            "temperature_c": final_input['temperature_c'],
            "humidity_percent": final_input['humidity_percent'],
            "ndvi_score": final_input['ndvi_score'],
            "disease_risk_score": final_input['disease_risk_score'],
            "fertilizer_deficiency_score": final_input['fertilizer_deficiency_score'],
            "irrigation_score": final_input['irrigation_score'],
            "waterlogging_risk": final_input['waterlogging_risk'],
            "reasons": reasons
        }

        return render_template("result.html", result=result)

    except Exception as e:
        return f"<h2>❌ Error:</h2><pre>{str(e)}</pre>"


# ============================
# RUN APP
# ============================
if __name__ == "__main__":
    app.run(debug=True)