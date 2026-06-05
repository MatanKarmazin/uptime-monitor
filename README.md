# 🚀 Uptime Monitor & Alerting Platform

![CI/CD Status](https://github.com/MatanKarmazin/uptime-monitor/actions/workflows/ci.yml/badge.svg)
![Deployment Status](https://github.com/MatanKarmazin/uptime-monitor/actions/workflows/deploy.yml/badge.svg)

A containerized uptime monitoring and observability platform designed to monitor web application availability in real time.

Built with a DevOps-focused approach, the project demonstrates infrastructure automation, monitoring, alerting, container orchestration with Docker Compose, Infrastructure as Code (IaC), and CI/CD automation on AWS.

---

# ✨ Features

* **Asynchronous Monitoring Engine:**  
  Uses Python `asyncio` background workers to continuously perform non-blocking health checks independently from API traffic.

* **Stateful Alerting:**  
  Redis is used as an in-memory state store to track the current availability status of monitored targets. Slack alerts are triggered only on state transitions (UP → DOWN / DOWN → UP) to reduce alert fatigue.

* **Observability Stack:**  
  Prometheus collects uptime metrics exposed by the FastAPI application, while Grafana provides real-time dashboards and uptime visualization.

* **Containerized Architecture:**  
  All services run in isolated Docker containers managed through Docker Compose for simplified local development and cloud deployment consistency.

* **Infrastructure as Code (IaC):**  
  AWS infrastructure provisioning is automated using Terraform, including EC2 instances, networking rules, and security groups.

* **CI/CD Automation:**  
  GitHub Actions pipelines automatically validate the application, build Docker images, and support deployment workflows.

---

# 📊 System Observability

![Grafana Dashboard showing Uptime Metrics](docs/grafana-dashboard.png)

---

# 🚨 Incident Response & Alerting

![Slack Webhook Critical Alerts](docs/slack-alerts.png)

---

# 🛠️ Tech Stack

* **Backend API:** Python 3.11, FastAPI, Asyncio, Requests
* **State Management / Cache:** Redis
* **Observability:** Prometheus, Grafana
* **Containerization:** Docker, Docker Compose
* **Cloud & Infrastructure:** AWS EC2, Terraform
* **CI/CD & Automation:** GitHub Actions
* **Alerting:** Slack Webhooks

---

# 🏗️ Architecture Overview

The monitoring workflow is built around asynchronous health checks, centralized state management, and observability tooling:

```text
                    ┌────────────────────┐
                    │   FastAPI Service  │
                    │  (Monitoring API)  │
                    └─────────┬──────────┘
                              │
               Background Async Health Checks
                              │
                              ▼
                    ┌────────────────────┐
                    │    Monitored URLs  │
                    └────────────────────┘

                              │
                              ▼

                    ┌────────────────────┐
                    │       Redis        │
                    │   Stateful Cache   │
                    └────────────────────┘

                              │
                              ▼

                    ┌────────────────────┐
                    │    Prometheus      │
                    │  Metrics Scraping  │
                    └────────────────────┘

                              │
                              ▼

                    ┌────────────────────┐
                    │      Grafana       │
                    │    Dashboards      │
                    └────────────────────┘

                              │
                              ▼

                    ┌────────────────────┐
                    │   Slack Webhooks   │
                    │   Incident Alerts  │
                    └────────────────────┘
```

---

# 🚀 Getting Started

## Prerequisites

* Docker Desktop installed and running
* Git installed
* Terraform installed
* AWS CLI configured with valid IAM credentials

---

# 💻 Local Development

## 1. Clone the Repository

```bash
git clone https://github.com/MatanKarmazin/uptime-monitor.git
cd uptime-monitor
```

---

## 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## 3. Launch the Stack

```bash
docker compose up -d --build
```

---

# 🌐 Access the Services

| Service | URL |
|---|---|
| API | `http://localhost:8000/status` |
| Metrics | `http://localhost:8000/metrics` |
| Grafana | `http://localhost:3000` |
| Prometheus | `http://localhost:9090` |

---

# ☁️ AWS Deployment (EC2 + Docker Compose)

The project can be deployed to AWS EC2 using Terraform for infrastructure provisioning.

## Provision Infrastructure

```bash
cd terraform
terraform init
terraform apply
```

Terraform provisions:
- EC2 instance
- Security Group
- SSH access rules
- Networking configuration

---

## Deploy the Application

SSH into the EC2 instance:

```bash
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

Clone the repository and start the services:

```bash
git clone https://github.com/MatanKarmazin/uptime-monitor.git
cd uptime-monitor

docker compose up -d --build
```

---

# 🧹 Infrastructure Cleanup

To destroy all provisioned AWS infrastructure:

```bash
terraform destroy
```

---

# 📌 Design Decisions

* Redis is used to persist monitoring state between health checks.
* Slack alerts are triggered only on status changes to avoid duplicate notifications.
* Docker Compose was selected for simplicity and deployment consistency.
* Prometheus + Grafana provide lightweight but production-style observability.
* Terraform enables reproducible infrastructure provisioning without manual AWS Console setup.

---

## 🧠 What I Learned

This project helped me gain hands-on experience with:

* Infrastructure as Code using Terraform
* Container orchestration with Docker Compose
* Cloud deployment on AWS EC2
* Monitoring and observability using Prometheus and Grafana
* Stateful alerting patterns using Redis
* CI/CD automation with GitHub Actions
* Managing multi-service applications in production-style environments

---

## 🏗️ Future Improvements
### Completed

* [x] Implement CI/CD pipelines using GitHub Actions
* [x] Add Prometheus metrics collection and Grafana dashboards
* [x] Configure Slack webhook alerting for downtime events
* [x] Containerize the entire stack using Docker Compose
* [x] Provision AWS infrastructure using Terraform
* [x] Deploy the monitoring platform to AWS EC2

### Planned Improvements
* [ ] Replace synchronous HTTP requests with fully async `httpx`
* [ ] Add persistent Docker volumes for Grafana and Prometheus data
* [ ] Add authentication for Grafana dashboards
* [ ] Implement healthcheck and restart policies for all containers
* [ ] Add automated integration testing for monitoring workflows
* [ ] Move monitored URLs to external configuration instead of hardcoded values
* [ ] Add HTTPS support using Nginx reverse proxy and Let's Encrypt
* [ ] Add Discord and Email alert integrations
* [ ] Add historical uptime reporting and SLA calculations
* [ ] Add container resource monitoring (CPU / Memory usage)