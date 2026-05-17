from fastapi import FastAPI
import requests
import redis
import datetime
import asyncio 
import os ## NEW: Needed for environment variables
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
    "https://www.youtube.com",
    "https://www.completely-new-broken-site.com"
]

SITE_STATUS_GAUGE = Gauge('site_status', '1 if site is up, 0 if down', ['url'])

## NEW: The Slack Alert Function
def send_slack_alert(service_url: str, error_msg: str, is_recovery: bool = False):
    """Sends a formatted alert to a Slack channel via Webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    if not webhook_url:
        print(f"⚠️ SLACK_WEBHOOK_URL not set. Missed alert for {service_url}")
        return

    if is_recovery:
        text = f"✅ *RESOLVED* ✅\n*URL:* {service_url}\n*Status:* Back Online!"
    else:
        text = f"🚨 *CRITICAL ALERT* 🚨\n*URL:* {service_url}\n*Error:* {error_msg}"

    payload = {"text": text}

    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        print(f"❌ Failed to send Slack alert: {e}")

def perform_health_checks():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for site in SITES_TO_MONITOR:
        ## NEW: Fetch the previous state before we check the current state
        previous_status = cache.get(f"{site}_status")

        try:
            response = requests.get(site, headers=headers, timeout=5)
            is_up = response.status_code == 200
            
            if is_up:
                current_time = datetime.datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")
                cache.set(site, current_time)
                cache.set(f"{site}_status", "UP")
                
                ## NEW: If it was DOWN and is now UP, send a recovery alert
                if previous_status == "DOWN":
                    send_slack_alert(site, "", is_recovery=True)
                    
            else:
                ## NEW: Handle non-200 HTTP responses (like 500 or 404)
                cache.set(f"{site}_status", "DOWN")
                if previous_status != "DOWN": # Only alert once!
                    send_slack_alert(site, f"HTTP Error {response.status_code}")
                
            SITE_STATUS_GAUGE.labels(url=site).set(1.0 if is_up else 0.0)
            
        except requests.RequestException as e:
            cache.set(f"{site}_status", "DOWN")
            SITE_STATUS_GAUGE.labels(url=site).set(0.0)
            
            ## NEW: Handle total connection failures (timeouts, DNS issues)
            if previous_status != "DOWN": # Only alert once!
                send_slack_alert(site, "Connection Failed or Timeout")

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

@app.get("/")
async def read_root():
    return {
        "status": "Success", 
        "message": "Hello from the automated CI/CD pipeline!"
    }