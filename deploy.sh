#!/bin/bash

# Exit immediately if any command fails
set -e

echo "🚀 Step 1: Navigating to Terraform directory..."
cd terraform

echo "🏗️ Step 2: Initializing and provisioning AWS EKS Cluster..."
terraform init
terraform apply -auto-approve # -auto-approve skips the manual "yes" prompt!

echo "🔑 Step 3: Updating local Kubernetes configuration..."
aws eks update-kubeconfig --region eu-central-1 --name uptime-monitor-cluster

echo "📦 Step 4: Deploying Redis and API manifests to the cluster..."
cd ..
kubectl apply -f k8s/api.yaml

echo "🌐 Step 5: Fetching your fresh AWS LoadBalancer URL..."
echo "--------------------------------------------------------"
kubectl get svc uptime-monitor-service
echo "--------------------------------------------------------"
echo "🎉 Done! Copy the EXTERNAL-IP above and add /status to view your app."