from fastapi import FastAPI
import requests
import redis
import datetime
import asyncio # הספרייה שתאפשר לנו להריץ דברים ברקע
from prometheus_client import make_asgi_app, Gauge
from zoneinfo import ZoneInfo

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

cache = redis.Redis(host='redis', port=6379, decode_responses=True)

SITES_TO_MONITOR = [
    "https://www.google.com",
    "https://github.com",
    "https://www.hit.ac.il",
    "https://www.this-shouldnt-work.com",
    "https://www.youtube.com"
    # Add more sites here
]

SITE_STATUS_GAUGE = Gauge('site_status', '1 if site is up, 0 if down', ['url'])

def perform_health_checks():
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
                cache.set(f"{site}_status", "UP")
                
            SITE_STATUS_GAUGE.labels(url=site).set(1.0 if is_up else 0.0)
            
        except requests.RequestException:
            SITE_STATUS_GAUGE.labels(url=site).set(0.0)
            cache.set(f"{site}_status", "DOWN")

async def background_monitor_loop():
    while True:
        await asyncio.to_thread(perform_health_checks)
        await asyncio.sleep(15)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_monitor_loop())

@app.get("/status")
def check_status():
    results = []
    for site in SITES_TO_MONITOR:
        last_seen = cache.get(site)
        current_status = cache.get(f"{site}_status")
        
        results.append({
            "url": site,
            "is_up": current_status == "UP",
            "last_seen_up": last_seen or "Never"
        })
        
    return {"status_checks": results}