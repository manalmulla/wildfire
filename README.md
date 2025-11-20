# 🚀 Wildfire – Real-Time Wildfire & Firepoint Monitoring System

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Backend-Python-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-darkgreen)
![NASA](https://img.shields.io/badge/Data-NASA%20FIRMS-orange)
![EONET](https://img.shields.io/badge/API-NASA%20EONET-red)

**Wildfire** is a real-time wildfire detection and monitoring system that visualizes **live firepoints**, **wildfire events**, **confidence levels**, and **alerts directly in the browser**.
It uses **NASA FIRMS**, **NASA EONET**, and an interactive map interface to provide accurate and up-to-date wildfire information.

---

## 🌍 Features

* 🔥 **Live Wildfire Detection & Map View**
* 📍 **NASA FIRMS Firepoints Integration**
* 🌋 **NASA EONET Natural Hazard Events**
* 🎨 **Color-coded Confidence Markers**

  * 🟢 Low (<30%)
  * 🟠 Medium (30–60%)
  * 🔴 High (>60%)
* 🪧 **Popups Showing:**

  * Latitude
  * Longitude
  * Confidence
  * Date & Time
* 🔔 **Browser-based Alert System**

  * User clicks a button to enable alerts
  * Alerts appear *inside the webpage,* not the terminal
* ⚡ Lightweight, API-driven, and easy to use

---

## 📸 Screenshots

<img width="1919" height="875" alt="Screenshot 2025-11-20 025414" src="https://github.com/user-attachments/assets/06d2cb8c-913c-424a-8e2a-1c39648bca0c" />

<img width="1919" height="868" alt="Screenshot 2025-11-20 030104" src="https://github.com/user-attachments/assets/8762bd81-e4df-41d3-b9af-6f7b25ae13b5" />

<img width="1092" height="371" alt="Screenshot 2025-11-20 171501" src="https://github.com/user-attachments/assets/1553c899-7dcd-4d0e-9094-abab202d9b27" />


---

## 🗂 Project Structure

```
wildfire/
│── static/
│   ├── css/
│   ├── js/
│── templates/
│   └── index.html
│── app.py
│── config.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone this repository

```bash
git clone https://github.com/manalmulla/wildfire.git
cd wildfire
```

### 2️⃣ Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Add Your NASA API Key

Open **config.py** and update:

```python
NASA_API_KEY = "YOUR_NASA_MAPS_KEY"
NASA_FIRMS_CSV_URL = "YOUR_FIRMS_CSV_URL"
CONFIDENCE_HIGH = 60
```

---

## ▶️ Running the App

```bash
python app.py
```

Then open in your browser:

```
http://127.0.0.1:5000/
```

---

## 🎨 Confidence Color Logic

```javascript
if (confidence < 30) {
    color = "green";   // Low confidence
} else if (confidence < 60) {
    color = "orange";  // Medium confidence
} else {
    color = "red";     // High confidence
}
```

Ensures all three color levels are visible.

---

## 🔔 Browser Alert System

The webpage includes a button like:

**Enable Wildfire Alerts**

When a user clicks:

* System checks current wildfire data
* If a nearby event is found, user receives:
  ✔️ On-screen notification
  ✔️ Visual warning popup
  ✔️ Optional sound alert

All inside the web browser—no terminal messages.

---

## 📦 Requirements

Example **requirements.txt**:

```
Flask
requests
time
io
webbrowser
```

(Add additional packages based on your project)

---

## 🤝 Contributing

🚫 Code contributions are not accepted.
This repository is public for viewing and learning, but only the owner can modify the code.

💬 Suggestions and feedback are welcome!
If you wish to propose improvements, report bugs, or share ideas, please open an Issue in the repository.

👉 Issues are open for discussions, suggestions, & improvement requests.
👉 Pull Requests are disabled to prevent direct code changes.

---

## ⭐ Support the Project

If you find this project useful, please give it a **⭐ star** on GitHub:
👉 [https://github.com/manalmulla/wildfire](https://github.com/manalmulla/wildfire)
