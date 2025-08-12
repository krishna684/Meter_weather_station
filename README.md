<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3.x">
  <img src="https://img.shields.io/badge/Framework-Flask-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/Frontend-Bootstrap%205-purple.svg" alt="Bootstrap 5">
  <img src="https://img.shields.io/badge/Charting-Chart.js-red.svg" alt="Chart.js">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License: MIT">
</p>

# 🌦️ Meter Weather Station Dashboard

A clean and interactive dashboard to visualize data from an **ATMOS 41 Gen2** weather station.
It fetches the latest sensor readings from the **ZentraCloud API**, caches the data for high performance,
and presents it through a user-friendly interface with tables and dynamic charts.

---

## 📸 Screenshot

*(Add a screenshot of your application's dashboard here)*

---

## ✨ Features

* **Live Data Table** – View the most recent sensor readings at a glance. Auto-refreshes every 5 minutes.
* **Interactive Charts** – Visualize historical data with responsive line charts.
* **Customizable Views** – Filter charts by sensor type & time range (6h, 12h, 24h, 48h).
* **Downloadable Charts** – Save charts as PNG images directly from the dashboard.
* **Efficient Caching** – API responses cached for 10 minutes to minimize API calls.
* **Responsive Design** – Built with Bootstrap, works seamlessly on desktop & mobile.

---

## 🛠️ Technologies Used

**Backend:** Python, Flask
**Frontend:** HTML, CSS, JavaScript
**Styling:** Bootstrap 5
**Charting:** Chart.js
**API Communication:** `requests`
**Configuration:** `python-dotenv` for environment variables
**WSGI Server:** gunicorn

---

## 🚀 Getting Started

### **Prerequisites**

* Python 3.x
* pip (Python package installer)

---

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/krishna684/Meter_weather_station.git
cd Meter_weather_station
```

---

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### **3️⃣ Set Up Environment Variables**

Create a `.env` file in the project root:

```env
ZENTRA_API_TOKEN="your_zentracloud_api_token"
ZENTRA_DEVICE_SN="your_device_serial_number"
```

Replace `your_...` values with your actual credentials.

---

## 🏃‍♂️ Running the Application

### Development Server

```bash
python app.py
```

Open in your browser:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Production (gunicorn)

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

---

## 🤝 Contributing

Contributions are welcome!

1. **Fork** the repository
2. **Create your Feature Branch**

   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit Changes**

   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. **Push to Branch**

   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
