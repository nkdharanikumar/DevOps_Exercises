# Helm Chart Engineering for Kubernetes

## Project Overview

This project demonstrates how to build a reusable and production-ready Helm Chart for Kubernetes applications.

The goal is to avoid maintaining separate Kubernetes manifests for different environments (Development, QA, Production) and instead use Helm templates and environment-specific values files.

This project was built as part of a DevOps engineering exercise focused on:

* Helm Chart Engineering
* Kubernetes Application Packaging
* Environment-based Deployments
* ConfigMap Management
* Secret Management
* Horizontal Pod Autoscaling (HPA)
* Ingress Configuration
* Kubernetes Best Practices

---

# Problem Statement

In many organizations, Kubernetes manifests are duplicated across environments.

Example:

Development Deployment

```yaml
replicas: 1
```

QA Deployment

```yaml
replicas: 2
```

Production Deployment

```yaml
replicas: 5
```

Maintaining separate YAML files becomes difficult as applications grow.

Challenges:

* Duplicate manifests
* Configuration drift
* Difficult upgrades
* Error-prone deployments
* Hard to manage multiple environments

Helm solves this problem by introducing:

* Templates
* Variables
* Reusable Charts
* Environment-specific values

---

# What is Helm?

Helm is the package manager for Kubernetes.

Think of Helm as:

* apt for Ubuntu
* yum for RHEL
* npm for JavaScript
* pip for Python

but for Kubernetes applications.

Instead of managing many YAML files manually, Helm packages everything into a Chart.

---

# Project Architecture

```text
Developer
    │
    ▼
Helm Chart
    │
    ▼
Values File
(dev/qa/prod)
    │
    ▼
Rendered Kubernetes Manifests
    │
    ▼
Kubernetes Cluster
(Minikube)
```

---

# Technologies Used

* Kubernetes
* Helm 3
* Minikube
* YAML
* NGINX Container Image

---

# Learning Objectives

This project helps understand:

* Helm templating
* Helm values files
* ConfigMaps
* Secrets
* Kubernetes Services
* Kubernetes Deployments
* Horizontal Pod Autoscaling
* Ingress resources
* Multi-environment deployments
* Kubernetes application packaging

---

# Project Structure

```text
payment-service/

├── Chart.yaml
├── values.yaml

├── values-dev.yaml
├── values-qa.yaml
├── values-prod.yaml

├── README.md

├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── configmap.yaml
│   └── secret.yaml
│
└── charts/
```

---

# Why Multiple Values Files?

Different environments need different configurations.

Example:

Development

```yaml
replicaCount: 1
```

QA

```yaml
replicaCount: 2
```

Production

```yaml
replicaCount: 5
```

Using separate values files allows the same chart to be reused across environments.

Benefits:

* Single source of truth
* Easier maintenance
* Reduced duplication
* Consistent deployments

---

# Environment Configuration

## Development

File:

```text
values-dev.yaml
```

Purpose:

* Local testing
* Developer validation
* Minimal resource consumption

Configuration:

```yaml
replicaCount: 1
```

---

## QA

File:

```text
values-qa.yaml
```

Purpose:

* Functional testing
* Integration testing

Configuration:

```yaml
replicaCount: 2
```

---

## Production

File:

```text
values-prod.yaml
```

Purpose:

* Production deployment
* High availability

Configuration:

```yaml
replicaCount: 5

autoscaling:
  enabled: true
```

---

# ConfigMap Implementation

## Why ConfigMap?

Applications often require configuration data.

Examples:

* Environment names
* API URLs
* Feature flags
* Application settings

Instead of hardcoding values inside containers, Kubernetes stores them in ConfigMaps.

Example:

```yaml
apiVersion: v1
kind: ConfigMap

data:
  APP_ENV: production
```

Benefits:

* Decouples configuration from code
* Easier updates
* Better maintainability

---

# Secret Implementation

## Why Secrets?

Sensitive information should never be stored inside application code.

Examples:

* Database passwords
* API keys
* JWT secrets
* Access tokens

Kubernetes Secrets provide secure storage.

Example:

```yaml
apiVersion: v1
kind: Secret

stringData:
  DB_PASSWORD: mypassword
```

Benefits:

* Centralized secret management
* Reduced exposure
* Better security practices

---

# Deployment Integration

ConfigMap and Secret were injected into the application using:

```yaml
envFrom:
  - configMapRef:
      name: prod-payment-service-config

  - secretRef:
      name: prod-payment-service-secret
```

This allows containers to automatically consume configuration and secrets as environment variables.

---

# Ingress Support

Ingress provides HTTP routing to applications.

Benefits:

* Single entry point
* Host-based routing
* Path-based routing
* SSL/TLS termination

Example:

```yaml
ingress:
  enabled: true
```

---

# Horizontal Pod Autoscaler

## Problem

Traffic changes throughout the day.

A fixed number of pods can lead to:

* Performance issues
* Resource wastage

## Solution

HPA automatically scales pods based on CPU utilization.

Example:

```yaml
autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20
```

Benefits:

* Improved availability
* Better resource utilization
* Automatic scaling

---

# Validation Steps

## Lint Validation

Validate Helm Chart:

```bash
helm lint .
```

Result:

```text
1 chart(s) linted, 0 chart(s) failed
```

---

## Template Validation

Render Kubernetes manifests:

```bash
helm template prod . -f values-prod.yaml
```

Purpose:

* Verify templates
* Verify values
* Detect YAML issues

---

# Deployment on Minikube

## Start Minikube

```bash
minikube start
```

Verify:

```bash
kubectl get nodes
```

---

## Install Helm Release

Development:

```bash
helm install dev . -f values-dev.yaml
```

---

## Verify Resources

```bash
kubectl get all
```

Result:

```text
Deployment
ReplicaSet
Pod
Service
```

---

## Verify ConfigMap

```bash
kubectl get configmap
```

---

## Verify Secret

```bash
kubectl get secret
```

---

## Verify Application

```bash
kubectl port-forward service/dev-payment-service 8080:80
```

Open:

```text
http://localhost:8080
```

Expected:

```text
Welcome to nginx!
```

---

# Actual Deployment Result

Successfully deployed:

```text
Deployment
ReplicaSet
Pod
Service
ConfigMap
Secret
HPA
```

Pod Status:

```text
Running
```

This confirms that:

* Helm Chart is valid
* Kubernetes manifests are valid
* Deployment works correctly
* ConfigMap integration works
* Secret integration works

---

# Key Concepts Learned

Through this project I learned:

* Helm Architecture
* Helm Chart Structure
* Helm Templates
* values.yaml
* Multi-environment Deployments
* ConfigMap Management
* Secret Management
* Kubernetes Deployments
* Kubernetes Services
* Horizontal Pod Autoscaling
* Helm Linting
* Helm Rendering
* Minikube Validation
* Production Deployment Practices

---

# Resume Description

Built a reusable Helm Chart for Kubernetes applications supporting multi-environment deployments (Dev, QA, and Production) with ConfigMaps, Secrets, Services, Ingress, Service Accounts, and Horizontal Pod Autoscaling. Validated deployments on a Kubernetes cluster using Minikube and Helm-managed releases.

---

# Future Improvements

Potential enhancements:

* External Secrets Operator
* AWS Secrets Manager Integration
* ArgoCD GitOps Deployment
* Prometheus Monitoring
* Grafana Dashboards
* CI/CD Integration with GitHub Actions
* ALB Ingress Controller
* Production EKS Deployment

---

# Author

DK

DevOps Engineer | Kubernetes | AWS | Terraform | Helm | GitOps
