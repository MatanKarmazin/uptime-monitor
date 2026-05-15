# 🚀 Uptime Monitor Fleet

A containerized microservices architecture built to monitor web application availability. Designed with a "DevOps-first" mindset, featuring automated CI/CD pipelines, stateful caching, an asynchronous monitoring engine, a fully provisioned observability stack, and Cloud Infrastructure as Code.

## ✨ Features

* **Asynchronous Monitoring Engine:** Utilizes Python's `asyncio` to run non-blocking background workers, ensuring continuous 24/7 health checks completely decoupled from API traffic.
* **Active Health Checking:** Periodically pings configured URLs and bypasses bot-protection using custom headers.
* **Stateful Tracking:** Integrates with **Redis** to maintain an in-memory cache of the exact timestamp a service was last healthy (Timezone: Asia/Jerusalem).
* **Time-Series Metrics:** Exposes a `/metrics` endpoint scraped by **Prometheus** for real-time tracking.
* **Dashboards as Code:** Utilizes **Grafana Provisioning** to automatically load pre-configured State Timeline dashboards directly from Git—no manual UI setup required.
* **Automated CI/CD:** A GitHub Actions workflow automatically builds the Docker environment and runs integration tests on every push.
* **Infrastructure as Code (IaC):** AWS cloud infrastructure (EC2, Security Groups) is provisioned automatically and reproducibly using **Terraform**.

## 🛠️ Tech Stack

* **Backend API:** Python 3.11, FastAPI, Requests, Asyncio
* **Database / Cache:** Redis (Alpine)
* **Observability:** Prometheus, Grafana
* **Infrastructure:** Docker, Docker Compose, GitHub Actions, Terraform, AWS (EC2)

## 🚀 Getting Started

### Prerequisites

* Docker Desktop installed and running.
* Git installed.
* *For Cloud Deployment:* AWS CLI configured and Terraform installed.

### 💻 Local Development

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MatanKarmazin/uptime-monitor.git](https://github.com/MatanKarmazin/uptime-monitor.git)
   cd uptime-monitor
   ```

2. **Launch the stack:**
   ```bash
   docker compose up -d --build
   ```


3. **Access the Services:**
* **API JSON Status:** `http://127.0.0.1:8000/status`
* **Prometheus Metrics:** `http://127.0.0.1:8000/metrics`
* **Grafana Dashboard:** `http://127.0.0.1:3000` *(Default login: admin / admin)*



### ☁️ Cloud Deployment (AWS)

1. **Provision Infrastructure:**
```bash
cd terraform
terraform init
terraform apply
```


*(Note the `server_public_ip` output upon completion).*
2. **Deploy the Application:**
SSH into the newly created EC2 instance:
```bash
ssh -i ~/.ssh/uptime_key ubuntu@<server_public_ip>
```


Inside the server, clone the repo and run Docker Compose:
```bash
git clone https://github.com/MatanKarmazin/uptime-monitor.git
cd uptime-monitor
sudo docker compose up -d --build
```



### Shutting Down

* **Stop Local Containers:** `docker compose down`
* **Destroy Cloud Infrastructure:** `cd terraform && terraform destroy`

## 🏗️ Future Roadmap

* [x] Implement CI/CD pipelines using GitHub Actions for automated testing.
* [x] Add Observability metrics (Prometheus) and visualization dashboards (Grafana).
* [x] Implement "Dashboards as Code" for zero-touch Grafana provisioning.
* [x] Refactor architecture to use asynchronous background workers.
* [x] Deploy cloud infrastructure via Terraform (IaC).
* [ ] Configure automated Alerting (Slack/Discord Webhooks) for downtime events.
* [ ] Secure the application with a domain name, HTTPS, and Let's Encrypt.
* [ ] Automate Terraform deployments (GitOps) within GitHub Actions.

---

*Created by Matan Karmazin*