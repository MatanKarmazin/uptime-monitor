# 🚀 Uptime Monitor

A lightweight, containerized microservice built to monitor the availability of web applications and track their historical uptime. Designed with a "DevOps-first" approach, emphasizing containerization, statefulness, and automation.

## ✨ Features

* **Active Health Checking:** Periodically pings configured URLs to verify HTTP `200 OK` responses.
* **Anti-Bot Evasion:** Utilizes custom `User-Agent` headers to successfully bypass standard bot-protection firewalls.
* **Stateful Tracking:** Integrates with **Redis** to maintain an in-memory cache of the last known time a service was healthy.
* **Fully Containerized:** Packaged cleanly using **Docker** and orchestrated via **Docker Compose** for a seamless, one-click developer experience.
* **Live Reloading:** Configured with Docker volumes for instant feedback during local development.

## 🛠️ Tech Stack

* **Backend API:** Python 3.11, FastAPI, Requests
* **Database / Cache:** Redis (Alpine)
* **Infrastructure:** Docker, Docker Compose

## 🚀 Getting Started

### Prerequisites
* Docker Desktop installed and running.
* Git installed.

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MatanKarmazin/uptime-monitor.git
   cd uptime-monitor
    ```
2. **Launch the stack:**
    ```bash
    docker compose up -d --build
    ```
3. **View the results:**
    Open your browser and navigate to the API endpoint:
    ```text
    http://127.0.0.1:8000/status
    ```



### Shutting Down

To gracefully stop the containers and clean up the networking:

```bash
docker compose down
```

## 🏗️ Future Roadmap (In Progress)

* [ ] Implement CI/CD pipelines using GitHub Actions for automated testing and image building.
* [ ] Deploy cloud infrastructure via Terraform (IaC).
* [ ] Add Observability metrics (Prometheus) and visualization dashboards (Grafana).

---

*Created by Matan Karmazin*
