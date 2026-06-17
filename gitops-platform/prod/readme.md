# GitOps Platform using ArgoCD and Kubernetes

## Project Overview

This project demonstrates the implementation of a GitOps platform using ArgoCD and Kubernetes.

The objective is to automate Kubernetes deployments by using Git as the single source of truth.

Instead of manually deploying applications using kubectl commands, ArgoCD continuously monitors a Git repository and automatically synchronizes Kubernetes resources with the desired state defined in Git.

This project was deployed and validated on a local Kubernetes cluster using Minikube.

---

# Problem Statement

Traditional Kubernetes deployments often rely on manual operations.

Example:

```bash
kubectl apply -f deployment.yaml
kubectl scale deployment nginx --replicas=5
kubectl delete service nginx
```

Problems with this approach:

* Manual deployments are error-prone
* Configuration drift occurs over time
* Different environments become inconsistent
* No centralized source of truth
* Difficult to audit changes
* Rollbacks become complicated
* Engineers can accidentally modify production resources

As teams grow, managing Kubernetes manually becomes difficult.

---

# Solution: GitOps

GitOps is an operational framework that uses Git repositories as the source of truth for infrastructure and application deployments.

Instead of manually modifying the cluster:

```text
Developer
     ↓
Git Commit
     ↓
Git Repository
     ↓
ArgoCD
     ↓
Kubernetes Cluster
```

The desired state always lives inside Git.

If Git changes, the cluster changes.

If the cluster drifts from Git, ArgoCD automatically corrects it.

---

# What is ArgoCD?

ArgoCD is a Kubernetes-native GitOps continuous delivery tool.

It continuously watches a Git repository and ensures the Kubernetes cluster matches the manifests stored in Git.

Key Features:

* GitOps Deployment
* Continuous Synchronization
* Drift Detection
* Self Healing
* Automated Rollbacks
* Multi-Environment Management
* Kubernetes Native

---

# Project Objectives

The main objectives of this project were:

* Install and configure ArgoCD
* Connect ArgoCD to a Git repository
* Deploy an application using GitOps principles
* Enable Auto Sync
* Validate Self Heal functionality
* Validate Pruning functionality
* Understand Kubernetes drift management

---

# Architecture

```text
                    Git Push
                       │
                       ▼
                GitHub Repository
                       │
                       ▼
                    ArgoCD
                       │
             Monitors Repository
                       │
                       ▼
                 Kubernetes
                  (Minikube)
                       │
                       ▼
               Deployment / Pod
```

---

# Technology Stack

* Kubernetes
* Minikube
* ArgoCD
* GitHub
* YAML
* GitOps

---

# Repository Structure

```text
gitops-platform/

├── dev/
│   ├── nginx-deployment.yaml
│   └── nginx-service.yaml
│
├── qa/
│
└── prod/
```

Purpose:

* dev → Development environment
* qa → Testing environment
* prod → Production environment

This structure allows environment-specific deployments.

---

# Why Git as Source of Truth?

Traditionally:

```text
Git
  ❌

Cluster
  ✅
```

With GitOps:

```text
Git
  ✅ Source of Truth

Cluster
  ✅ Desired State
```

Benefits:

* Complete audit history
* Easy rollbacks
* Better collaboration
* Infrastructure versioning
* Improved reliability

---

# Environment Setup

## Step 1: Start Minikube

Command:

```bash
minikube start
```

Purpose:

Creates a local Kubernetes cluster for testing and development.

Verification:

```bash
kubectl get nodes
```

Expected Output:

```text
minikube   Ready
```

---

## Step 2: Install ArgoCD

Create Namespace:

```bash
kubectl create namespace argocd
```

Purpose:

Creates a dedicated namespace for ArgoCD components.

Install ArgoCD:

```bash
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Purpose:

Deploys all required ArgoCD components.

Installed Components:

* ArgoCD Server
* ArgoCD Repository Server
* Application Controller
* Redis
* Dex

Verification:

```bash
kubectl get pods -n argocd
```

Expected:

```text
All pods should be Running
```

---

# Accessing ArgoCD UI

Port Forward:

```bash
kubectl port-forward svc/argocd-server \
-n argocd 8080:443
```

Purpose:

Exposes the ArgoCD web interface locally.

Access:

```text
https://localhost:8080
```

---

# Creating the GitOps Application

Application Name:

```text
nginx-dev
```

Repository:

```text
https://github.com/nkdharanikumar/gitops-platform
```

Path:

```text
dev
```

Destination:

```text
https://kubernetes.default.svc
```

Namespace:

```text
default
```

---

# Sync Policy Configuration

The following options were enabled:

## Auto Sync

Purpose:

Automatically synchronizes cluster resources whenever Git changes.

Enabled:

```text
✔ Enable Auto Sync
```

---

## Self Heal

Purpose:

Automatically restores resources if someone manually modifies them inside the cluster.

Enabled:

```text
✔ Self Heal
```

---

## Pruning

Purpose:

Automatically removes Kubernetes resources that are deleted from Git.

Enabled:

```text
✔ Prune Resources
```

---

# Deployment Validation

After creating the ArgoCD application:

Verification:

```bash
kubectl get deploy,pods,svc
```

Output:

```text
deployment.apps/nginx
pod/nginx-xxxxx
service/nginx
```

This confirmed:

* Deployment created
* Pod running
* Service created
* ArgoCD synchronization successful

---

# Auto Sync Validation

## Goal

Verify that ArgoCD automatically deploys Git changes.

### Original Configuration

```yaml
replicas: 1
```

### Modified Configuration

```yaml
replicas: 3
```

Push Changes:

```bash
git add .
git commit -m "Scale nginx to 3 replicas"
git push
```

Result:

ArgoCD automatically detected the change and scaled the deployment.

Verification:

```bash
kubectl get pods
```

Result:

```text
3 running nginx pods
```

No manual kubectl apply command was used.

---

# Self Heal Validation

## Goal

Verify that ArgoCD can detect and correct configuration drift.

Manual Change:

```bash
kubectl scale deployment nginx --replicas=10
```

Result:

Cluster state differed from Git.

Git State:

```yaml
replicas: 3
```

Cluster State:

```text
replicas: 10
```

ArgoCD detected the drift and automatically restored:

```text
replicas: 3
```

Verification:

```bash
kubectl get deploy nginx
```

This proves Self Heal functionality.

---

# Pruning Validation

## Goal

Verify that deleted Git resources are removed from Kubernetes.

Deleted:

```text
dev/nginx-service.yaml
```

Push Changes:

```bash
git add .
git commit -m "Remove nginx service"
git push
```

Result:

ArgoCD automatically deleted the Service resource from Kubernetes.

Verification:

```bash
kubectl get svc
```

The nginx service no longer existed.

This confirms Pruning functionality.

---

# Key GitOps Concepts Learned

## Desired State

The configuration stored in Git.

Example:

```yaml
replicas: 3
```

---

## Actual State

The configuration currently running in Kubernetes.

Example:

```yaml
replicas: 10
```

---

## Drift

Difference between Desired State and Actual State.

Example:

```text
Git      -> 3 replicas
Cluster  -> 10 replicas
```

---

## Reconciliation

The process of making Actual State match Desired State.

ArgoCD continuously performs reconciliation.

---

# Benefits of GitOps

* Declarative Deployments
* Automated Synchronization
* Improved Security
* Easier Rollbacks
* Better Auditing
* Reduced Human Error
* Infrastructure Version Control
* Faster Disaster Recovery

---

# Skills Learned

Through this project I learned:

* GitOps Fundamentals
* ArgoCD Architecture
* Kubernetes Deployments
* Kubernetes Services
* Git-based Continuous Delivery
* Auto Sync
* Self Heal
* Pruning
* Drift Detection
* Reconciliation Loops
* Kubernetes Resource Management

---

# Real-World Use Cases

GitOps is commonly used in:

* Kubernetes Platforms
* Cloud Native Applications
* Multi-Environment Deployments
* DevOps Teams
* Platform Engineering Teams
* Production Kubernetes Clusters

Organizations use GitOps to manage:

* Application Deployments
* Infrastructure
* Security Policies
* Monitoring Stacks
* Kubernetes Add-ons

---

# Resume Description

Implemented a GitOps platform using ArgoCD and Kubernetes. Configured automated application deployment from GitHub repositories with Auto Sync, Self Heal, and Pruning enabled. Validated drift detection and reconciliation workflows on a Kubernetes cluster running in Minikube.

---

# Future Improvements

Possible enhancements:

* Helm-based GitOps Deployments
* Multi-Environment Applications
* ApplicationSets
* External Secrets Integration
* Argo Rollouts
* Progressive Delivery
* GitHub Actions Integration
* EKS Deployment
* Multi-Cluster Management

---

# Conclusion

This project successfully demonstrated a complete GitOps workflow using ArgoCD.

The Kubernetes cluster continuously synchronized with Git, automatically corrected configuration drift, and removed obsolete resources.

The implementation validated the three core GitOps principles:

* Auto Sync
* Self Heal
* Pruning

This project provides a strong foundation for advanced GitOps, Platform Engineering, and Cloud Native deployment practices.
