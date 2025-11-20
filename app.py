# app.py
from flask import Flask, render_template, jsonify, request
import requests
import csv, webbrowser, time, threading
import io
from datetime import datetime
from config import NASA_FIRMS_CSV_URL

app = Flask(__name__)

EONET_EVENTS_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

def fetch_eonet_fires():
    """Fetch latest wildfire events from NASA EONET and normalize to a list of points."""
    try:
        params = {"status": "open", "category": "wildfires", "limit": 1000}
        r = requests.get(EONET_EVENTS_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        points = []
        for evt in data.get("events", []):
            title = evt.get("title")
            geometries = evt.get("geometry", []) or []
            if not geometries:
                continue

            latest = geometries[-1]
            coords = latest.get("coordinates")

            if not coords or len(coords) < 2:
                continue

            lon, lat = coords[0], coords[1]
            dt = latest.get("date") or ""

            confidence = latest.get("confidence")
            if confidence is None:
                confidence = 60

            points.append({
                "id": f"{evt.get('id')}_{dt}",
                "source": "eonet",
                "title": title,
                "lat": lat,
                "lon": lon,
                "datetime": dt,
                "confidence": int(confidence)
            })

        return points
    except Exception as e:
        print("Error fetching EONET:", e)
        return []


# -----------------------------------------------------
# 🔥 FIXED FIRMS FUNCTION — UNIQUE REAL TIMESTAMPS
# -----------------------------------------------------
def fetch_firms_points():
    """Fetch NASA FIRMS CSV and return points with correct datetime."""
    if not NASA_FIRMS_CSV_URL:
        return []

    try:
        r = requests.get(NASA_FIRMS_CSV_URL, timeout=10)
        r.raise_for_status()
        csv_text = r.text
        reader = csv.DictReader(io.StringIO(csv_text))

        points = []
        for i, row in enumerate(reader):
            try:
                lat = float(row.get("latitude") or row.get("lat"))
                lon = float(row.get("longitude") or row.get("lon"))

                # --- Confidence mapping ---
                conf_raw = row.get("confidence") or ""
                if conf_raw.isdigit():
                    conf = int(conf_raw)
                else:
                    conf_map = {"low": 30, "nominal": 60, "normal": 60, "high": 90}
                    conf = conf_map.get(conf_raw.lower(), 60)

                # --- Correct FIRMS datetime parse ---
                date_raw = row.get("acq_date", "")
                time_raw = row.get("acq_time", "")

                try:
                    if date_raw and len(time_raw) == 4:
                        hh = time_raw[:2]
                        mm = time_raw[2:]
                        ss = "00"
                        dt = datetime.strptime(f"{date_raw} {hh}:{mm}:{ss}", "%Y-%m-%d %H:%M:%S")
                        dt_iso = dt.isoformat() + "Z"
                    elif date_raw:
                        dt = datetime.strptime(date_raw, "%Y-%m-%d")
                        dt_iso = dt.isoformat() + "Z"
                    else:
                        dt_iso = ""
                except:
                    dt_iso = ""

                points.append({
                    "id": f"firms_{i}",
                    "source": "firms",
                    "title": "FIRMS fire",
                    "lat": lat,
                    "lon": lon,
                    "datetime": dt_iso,
                    "confidence": conf
                })

            except Exception:
                continue

        return points

    except Exception as e:
        print("Error fetching FIRMS:", e)
        return []


@app.route("/")
def index():
    from config import NASA_MAP_KEY, POLL_INTERVAL_MS
    return render_template("index.html", nasa_map_key=NASA_MAP_KEY, poll_interval_ms=POLL_INTERVAL_MS)


@app.route("/api/fires")
def api_fires():
    """Return combined list of fire points."""
    eonet = fetch_eonet_fires()
    firms = fetch_firms_points()
    points = eonet + firms

    print("🔥 Total firepoints detected:", len(points))

    # deduplicate
    unique = {}
    for p in points:
        key = f"{round(p['lat'],4)}_{round(p['lon'],4)}_{p['source']}"
        if key not in unique:
            unique[key] = p

    return jsonify(list(unique.values()))


@app.route("/api/nearby")
def api_nearby():
    """Return fires within radius_km of provided lat, lon."""
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        radius_km = float(request.args.get("radius_km", 50))
    except:
        return jsonify({"error": "Provide lat, lon"}), 400

    import math
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        phi1 = math.radians(lat1); phi2 = math.radians(lat2)
        dphi = math.radians(lat2-lat1)
        dlambda = math.radians(lon2-lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    points = fetch_eonet_fires() + fetch_firms_points()
    nearby = []
    for p in points:
        d = haversine(lat, lon, p["lat"], p["lon"])
        if d <= radius_km:
            p2 = p.copy()
            p2["distance_km"] = round(d, 2)
            nearby.append(p2)

    nearby.sort(key=lambda x: x["distance_km"])
    return jsonify(nearby)


def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000/")


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
