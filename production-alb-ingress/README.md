# 🚀 Exercise 21 - Production ALB Ingress Setup on Amazon EKS

## 📌 Project Overview

This project demonstrates how to deploy multiple applications on an
Amazon EKS cluster and expose them through a single AWS Application Load
Balancer (ALB) using Kubernetes Ingress with path-based routing.

The AWS Load Balancer Controller automatically provisions an
internet-facing ALB and configures routing rules to forward incoming
traffic to the appropriate Kubernetes services.

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                 Internet
                     │
                     ▼
      AWS Application Load Balancer (ALB)
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
      /api        /admin     /dashboard
        │            │            │
        ▼            ▼            ▼
   api-service  admin-service  dashboard-service
        │            │            │
        ▼            ▼            ▼
     API Pod     Admin Pod    Dashboard Pod
                 (Amazon EKS)
```

## 🛠️ Technologies Used

-   Amazon EKS
-   Kubernetes
-   AWS Load Balancer Controller
-   AWS Application Load Balancer (ALB)
-   IAM Roles for Service Accounts (IRSA)
-   eksctl
-   kubectl
-   Helm
-   NGINX

## 📂 Project Structure

``` text
exercise-21-production-alb/
├── kubernetes/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   ├── namespace.yaml
│   └── nginx-config.yaml
├── docs/
├── screenshots/
├── .gitignore
└── README.md
```

## 🎯 Objectives

-   Create an Amazon EKS Cluster
-   Install AWS Load Balancer Controller
-   Deploy multiple applications
-   Create Kubernetes Services
-   Configure an AWS Application Load Balancer
-   Implement Path-Based Routing
-   Configure ALB Health Checks

## ⚙️ Prerequisites

-   AWS Account
-   AWS CLI configured
-   kubectl
-   eksctl
-   Helm

## 🚀 Deployment Steps

### 1. Create EKS Cluster

``` bash
eksctl create cluster \
  --name production-alb \
  --region ap-south-1 \
  --nodegroup-name production-workers \
  --node-type t3.medium \
  --nodes 2 \
  --managed
```

### 2. Associate IAM OIDC Provider

``` bash
eksctl utils associate-iam-oidc-provider \
  --region ap-south-1 \
  --cluster production-alb \
  --approve
```

### 3. Install AWS Load Balancer Controller

-   Create IAM Policy
-   Create IAM Service Account (IRSA)
-   Install the controller using Helm

### 4. Deploy Resources

``` bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployments/
kubectl apply -f kubernetes/services/
kubectl apply -f kubernetes/nginx-config.yaml
kubectl apply -f kubernetes/ingress/alb-ingress.yaml
```

### 5. Restart Deployments

``` bash
kubectl rollout restart deployment api -n production
kubectl rollout restart deployment admin -n production
kubectl rollout restart deployment dashboard -n production
```

## 🌐 Endpoints

``` text
http://<ALB-DNS>/api
http://<ALB-DNS>/admin
http://<ALB-DNS>/dashboard
```

## 🔍 Verification

``` bash
kubectl get pods -n production
kubectl get svc -n production
kubectl get ingress -n production
```

Expected responses:

``` text
API Service
Admin Service
Dashboard Service
```

## ❤️ Health Check

Configured using:

``` yaml
alb.ingress.kubernetes.io/healthcheck-path: /
```

## 📸 Screenshots

Add screenshots for:

-   EKS Cluster
-   Load Balancer
-   Target Groups
-   Pods
-   Services
-   Ingress
-   API
-   Admin
-   Dashboard

## ⚠️ SSL Note

SSL/TLS and HTTP → HTTPS redirection were **not configured** because AWS
ACM public certificates require ownership of a domain for validation.

The project is ready for HTTPS by attaching an ACM certificate and
updating the Ingress annotations.

## 📚 Concepts Covered

-   Amazon EKS
-   Kubernetes Deployments
-   Services
-   Ingress
-   AWS Load Balancer Controller
-   Application Load Balancer
-   IRSA
-   Path-Based Routing
-   Health Checks
-   Helm

## 🚀 Future Improvements

-   Route53
-   ACM SSL Certificate
-   HTTPS
-   HTTP → HTTPS Redirect
-   CI/CD Pipeline
-   Monitoring with Prometheus & Grafana

## 🧹 Cleanup

``` bash
kubectl delete namespace production

eksctl delete cluster \
  --name production-alb \
  --region ap-south-1
```

## 👨‍💻 Author

**Dharani Kumar N K**

B.E. Electronics and Communication Engineering

Cloud \| DevOps \| AWS \| Kubernetes \| Docker
