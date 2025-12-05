
let map = L.map('map').setView([20, 0], 2);

const tileUrl = NASA_MAP_KEY && NASA_MAP_KEY !== "YOUR_MAP_KEY"
  ? `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` // fallback
  : `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`;

L.tileLayer(tileUrl, {
  maxZoom: 18,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markersLayer = L.layerGroup().addTo(map);
let userLocation = null;
let alertEnabled = false;
const CONF_HIGH = 80, CONF_NORMAL = 60;
let userRadiusCircle = null;

//determine color by confidence
function colorForConfidence(c) {
  if (c >= CONF_HIGH) return '#ff0000';      // red
  if (c >= CONF_NORMAL) return '#ff8c00';    // orange
  return '#00a000';                          // green
}

function showToast(html, timeout=6000) {
  const t = document.getElementById('toast');
  t.innerHTML = html;
  t.classList.remove('hidden');
  if (timeout>0) {
    setTimeout(()=> t.classList.add('hidden'), timeout);
  }
}

async function loadFiresAndRender() {
  try {
    const r = await fetch('/api/fires');
    const points = await r.json();

    markersLayer.clearLayers();

    points.forEach(p => {
      const color = colorForConfidence(Number(p.confidence || 60));
      const circle = L.circleMarker([p.lat, p.lon], {
        radius: 3,
        color: color,
        fillColor: color,
        fillOpacity: 0.8,
        weight: 1
      });

      const dt = p.datetime ? new Date(p.datetime).toLocaleString() : (p.datetime || "unknown");

      const popupHtml = `
        <strong>${p.title}</strong><br/>
        <b>Source:</b> ${p.source}<br/>
        <b>Date:</b> ${dt}<br/>
        <b>Confidence:</b> ${p.confidence}<br/>
        <b>Lat, Lon:</b> ${p.lat.toFixed(4)}, ${p.lon.toFixed(4)}
      `;

      circle.bindPopup(popupHtml);

      circle.on('click', () => {
        showToast(`<strong>Fire</strong><br/>${p.title}<br/>${dt}<br/>Confidence: ${p.confidence}`, 8000);
      });

      circle.addTo(markersLayer);
    });

  } catch (e) {
    console.error("Failed to load fires", e);
  }
}

// Polling
loadFiresAndRender();
setInterval(loadFiresAndRender, POLL_INTERVAL_MS);

// alerts flow
document.getElementById('enableAlerts').addEventListener('click', async () => {
  if (!("Notification" in window)) {
    alert("This browser does not support notifications.");
    return;
  }
  let perm = await Notification.requestPermission();
  if (perm !== "granted") {
    alert("Please allow notifications to receive wildfire alerts.");
    return;
  }
  alertEnabled = true;
  showToast("Alerts enabled. Click 'Center on me' to start nearby checks.", 4000);
});

document.getElementById('centerMe').addEventListener('click', () => {
  if (!navigator.geolocation) {
    alert("Geolocation not available.");
    return;
  }

  navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude, lon = pos.coords.longitude;
    userLocation = {lat, lon};

    map.setView([lat, lon], 8);

    // Remove old radius circle
    if (userRadiusCircle) userRadiusCircle.remove();

    const radiusKm = Number(document.getElementById('radiusSelect').value || 50);

    // Draw updated radius circle
    userRadiusCircle = L.circle([lat, lon], {
      radius: radiusKm * 1000,
      color: '#0077ff',
      fill: false
    }).addTo(map);

    checkNearbyAndNotify();

    if (alertEnabled) {
      if (window._nearbyInterval) clearInterval(window._nearbyInterval);
      window._nearbyInterval = setInterval(checkNearbyAndNotify, POLL_INTERVAL_MS);
    }

  }, err => {
    alert("Could not get location: " + err.message);
  });
});

async function checkNearbyAndNotify() {
  if (!userLocation) return;

  const radius = Number(document.getElementById('radiusSelect').value || 50);

  try {
    const resp = await fetch(`/api/nearby?lat=${userLocation.lat}&lon=${userLocation.lon}&radius_km=${radius}`);
    const nearby = await resp.json();

    if (nearby.length > 0) {
      const nearest = nearby[0];
      const body = `${nearest.title}\nConfidence: ${nearest.confidence}\nDist: ${nearest.distance_km} km`;
      showToast(`<strong>Nearby fire!</strong><br/>${body}`, 8000);

      if (Notification.permission === "granted") {
        new Notification("Firepoint nearby", {
          body,
          tag: 'wildfire-alert'
        });
      }

    } else {
      showToast("No fires within " + radius + " km", 3500);
    }

  } catch (e) {
    console.error("Nearby check failed", e);
  }
}

document.getElementById("radiusSelect").addEventListener("change", () => {
  const newRadius = Number(document.getElementById("radiusSelect").value);

  if (userLocation) {
    if (userRadiusCircle) userRadiusCircle.remove();

    userRadiusCircle = L.circle([userLocation.lat, userLocation.lon], {
      radius: newRadius * 1000,
      color: '#0077ff',
      fill: false
    }).addTo(map);
  }

  if (alertEnabled && userLocation) {
    if (window._nearbyInterval) clearInterval(window._nearbyInterval);
    window._nearbyInterval = setInterval(checkNearbyAndNotify, POLL_INTERVAL_MS);

    showToast("Radius updated to " + newRadius + " km", 3000);
  }
});
