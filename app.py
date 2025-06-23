from flask import Flask, jsonify, render_template
import os, requests, time
from threading import Thread
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
app = Flask(__name__)

API_TOKEN = os.getenv("ZENTRA_API_TOKEN")
DEVICE_SN = os.getenv("ZENTRA_DEVICE_SN")
BASE_URL = "https://zentracloud.com/api/v3/get_readings/"

# In-memory cache
cached_data = {}

def fetch_sensor_data():
    global cached_data
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
                for r in series.get("readings", []):
                    readings.append({
                        "time": r.get("datetime"),
                        "value": r.get("value")
                    })
            sensors[label] = readings

        cached_data = sensors
        print(f"✅ Fetched sensor data at {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")

def background_fetch_loop():
    while True:
        fetch_sensor_data()
        time.sleep(600)  # every 10 minutes

@app.route('/')
def home():
    # Show latest reading per sensor
    if not cached_data:
        fetch_data()
    latest = {}
    for sensor, values in cached_data.items():
        if values:
            latest[sensor] = values[-1]  # last = latest by time
    return render_template("home.html", latest=latest)

@app.route('/charts')
def charts():
    if not cached_data:
        fetch_data()
    return render_template("dashboard.html")

@app.route('/api/live')
def serve_data():
    return jsonify(cached_data)

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Only run once on reload
        Thread(target=background_fetch_loop, daemon=True).start()
    app.run(debug=True)
