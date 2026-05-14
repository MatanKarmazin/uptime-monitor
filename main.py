from fastapi import FastAPI
import requests
import redis
import datetime

app = FastAPI()

# DevOps Magic: Notice the host is simply "redis". 
# Docker Compose automatically creates an internal network where containers can resolve each other by their service names!
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

SITES_TO_MONITOR = [
    "https://www.google.com",
    "https://github.com",
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.hit.ac.il"
]

@app.get("/status")
def check_status():
    results = []
    
    # We add a fake browser User-Agent so websites don't block us
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for site in SITES_TO_MONITOR:
        try:
            # Pass the headers into the request
            response = requests.get(site, headers=headers, timeout=5)
            is_up = response.status_code == 200
            
            if is_up:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cache.set(site, current_time)
                
            last_seen = cache.get(site)
            
            results.append({
                "url": site,
                "is_up": is_up,
                "last_seen_up": last_seen or "Never",
                "status_code": response.status_code # Added this so we can see the exact error if it fails!
            })
            
        except requests.RequestException as e:
            last_seen = cache.get(site)
            results.append({
                "url": site,
                "is_up": False,
                "last_seen_up": last_seen or "Never",
                "status_code": "Network Error"
            })
            
    return {"status_checks": results}