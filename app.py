import os
import json
import requests
from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_TOKEN = os.getenv("ZENTRA_API_TOKEN")
DEVICE_SN = os.getenv("ZENTRA_DEVICE_SN")
BASE_URL = "https://zentracloud.com/api/v3/get_readings/"
CACHE_FILE = "data_cache.json"
CACHE_TTL_MINUTES = 10

# Function to fetch fresh data from API
def fetch_fresh_data():
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

    return sensors

# Caching layer
def get_cached_data():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cached = json.load(f)
        timestamp = datetime.fromisoformat(cached["timestamp"])
        if (datetime.now(timezone.utc) - timestamp) < timedelta(minutes=CACHE_TTL_MINUTES):
            return cached["data"]

    fresh = fetch_fresh_data()
    with open(CACHE_FILE, 'w') as f:
        json.dump({"timestamp": datetime.now(timezone.utc).isoformat(), "data": fresh}, f)
    return fresh

# Route: Home
@app.route("/")
def home():
    sensor_data = get_cached_data()
    return render_template("home.html", sensors=sensor_data)

# Route: Charts
@app.route("/charts")
def charts():
    return render_template("dashboard.html")

# Route: API for AJAX
@app.route("/api/live")
def api_live():
    return jsonify(get_cached_data())

if __name__ == "__main__":
    app.run(debug=True)
