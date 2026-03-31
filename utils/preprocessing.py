import pandas as pd

def build_zone_input(form_data):
    """
    Convert raw form data into model-ready DataFrame row
    """

    data = {
        'zone_row': int(form_data['zone_row']),
        'zone_col': int(form_data['zone_col']),
        'zone_position': form_data['zone_position'],

        'crop_type': form_data['crop_type'],
        'crop_age_days': int(form_data['crop_age_days']),
        'crop_stage': form_data['crop_stage'],

        'soil_type': form_data['soil_type'],
        'soil_moisture': float(form_data['soil_moisture']),
        'soil_temperature_c': float(form_data['soil_temperature_c']),
        'drainage_condition': form_data['drainage_condition'],
        'mulching': form_data['mulching'],

        'temperature_c': float(form_data['temperature_c']),
        'humidity_percent': float(form_data['humidity_percent']),
        'rainfall_last_24h_mm': float(form_data['rainfall_last_24h_mm']),
        'rain_probability_next_24h': float(form_data['rain_probability_next_24h']),
        'wind_speed_kmph': float(form_data['wind_speed_kmph']),
        'sunlight_hours': float(form_data['sunlight_hours']),
        'evapotranspiration_mm_day': float(form_data['evapotranspiration_mm_day']),
        'weather_condition': form_data['weather_condition'],

        'last_irrigation_days': int(form_data['last_irrigation_days']),
        'irrigation_method': form_data['irrigation_method'],
        'crop_water_requirement_mm': float(form_data['crop_water_requirement_mm']),

        'fertilizer_level': float(form_data['fertilizer_level']),
        'field_slope': form_data['field_slope'],

        'ndvi_score': float(form_data['ndvi_score']),
        'disease_risk_score': float(form_data['disease_risk_score']),
        'fertilizer_deficiency_score': float(form_data['fertilizer_deficiency_score']),
        'irrigation_score': float(form_data['irrigation_score']),
        'waterlogging_risk': form_data['waterlogging_risk'],
        'waterlogging_score': float(form_data['waterlogging_score']),

        'irrigation_needed_zone': int(form_data['irrigation_needed_zone']),
        'fertilizer_needed_zone': int(form_data['fertilizer_needed_zone']),
        'disease_risk_zone': int(form_data['disease_risk_zone'])
    }

    return data


def get_recommendation_from_prediction(status, health_score):
    """
    Human-readable recommendation
    """
    if status == "Dry":
        return "💧 Irrigation required in this zone."
    elif status == "Healthy":
        return "✅ Zone is healthy. No immediate action needed."
    elif status == "Risky":
        return "⚠️ Check for disease, crop stress, and growth issues."
    elif status == "Overwatered":
        return "🚫 Avoid irrigation. Improve drainage immediately."
    elif status == "Nutrient Deficient":
        return "🌱 Apply fertilizer or nutrient support in this zone."
    else:
        return f"📌 Monitor this zone carefully. Health score: {round(health_score, 2)}"