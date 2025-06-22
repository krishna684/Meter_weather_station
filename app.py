import os
import requests
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Load environment variables from .env
load_dotenv()
app = Flask(__name__)

# Load credentials and endpoint
API_TOKEN = os.getenv("ZENTRA_API_TOKEN")
DEVICE_SN = os.getenv("ZENTRA_DEVICE_SN")
BASE_URL = "https://zentracloud.com/api/v3/get_readings/"

@app.route('/')
def dashboard():
    return render_template("dashboard.html")  # Ensure dashboard.html exists in templates/

@app.route('/api/live')
def get_atmos41_data():
    headers = {
        "Authorization": API_TOKEN,
        "Accept": "application/json"
    }

    params = {
        "device_sn": DEVICE_SN,
        "start_date": (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"),
        "end_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "output_format": "json",
        "per_page": 1000
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        raw_data = response.json()

        data = raw_data.get("data", {})
        sensors = {}

        for label, series_list in data.items():
            readings = []
            for series in series_list:
                for reading in series.get("readings", []):
                    readings.append({
                        "time": reading.get("datetime"),
                        "value": reading.get("value")
                    })
            sensors[label] = readings

        return jsonify(sensors)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
