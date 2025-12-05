# config.py
import os
NASA_MAP_KEY = os.getenv("NASA_MAP_KEY", "YOUR_MAP_KEY")

NASA_FIRMS_CSV_URL = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/YOUR_MAP_KEY/VIIRS_SNPP_NRT/world/1"

# Confidence thresholds:
# >=80 -> high -> red
# 50-79 -> normal -> orange
# <50 -> low -> green
CONFIDENCE_HIGH = 80
CONFIDENCE_NORMAL = 60

# How often front-end polls for new data (milliseconds)
POLL_INTERVAL_MS = 120000  # 2 minutes
