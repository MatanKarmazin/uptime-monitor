from fastapi import FastAPI
import requests
import redis
import datetime
from prometheus_client import make_asgi_app, Gauge
from zoneinfo import ZoneInfo

app = FastAPI()

# Mount the Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

cache = redis.Redis(host='redis', port=6379, decode_responses=True)

SITES_TO_MONITOR = [
    "https://www.google.com",
    "https://github.com",
    "https://www.hit.ac.il",
    "https://www.linkedin.com"
]

# Define a Prometheus Gauge metric
SITE_STATUS_GAUGE = Gauge('site_status', '1 if site is up, 0 if down', ['url'])

@app.get("/status")
def check_status():
    results = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for site in SITES_TO_MONITOR:
        try:
            response = requests.get(site, headers=headers, timeout=5)
            is_up = response.status_code == 200
            
            if is_up:
                current_time = datetime.datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")
                cache.set(site, current_time)
                
            last_seen = cache.get(site)
            
            # Update the Prometheus metric: 1.0 for up, 0.0 for down
            SITE_STATUS_GAUGE.labels(url=site).set(1.0 if is_up else 0.0)
            
            results.append({
                "url": site,
                "is_up": is_up,
                "last_seen_up": last_seen or "Never",
                "status_code": response.status_code
            })
            
        except requests.RequestException:
            last_seen = cache.get(site)
            
            # Site is down, set metric to 0
            SITE_STATUS_GAUGE.labels(url=site).set(0.0)
            
            results.append({
                "url": site,
                "is_up": False,
                "last_seen_up": last_seen or "Never",
                "status_code": "Network Error"
            })
            
    return {"status_checks": results}