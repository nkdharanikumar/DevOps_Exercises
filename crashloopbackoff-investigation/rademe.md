# 🚨 Kubernetes Incident Response Lab – CrashLoopBackOff Investigation

> **Project Type:** Kubernetes Troubleshooting Lab
> **Difficulty:** Intermediate
> **Category:** Kubernetes | DevOps | SRE | Production Debugging
> **Environment:** Minikube

---

# 📖 Project Overview

Modern cloud-native applications are built using multiple microservices that communicate with databases, APIs, caches, and other services. In production environments, failures are inevitable. A service may suddenly stop working because a dependency becomes unavailable, a secret is misconfigured, DNS fails, or networking breaks.

One of the most common Kubernetes incidents is a pod entering the **CrashLoopBackOff** state.

This project recreates a real-world production incident where a payment service continuously crashes because it cannot establish a connection with its PostgreSQL database.

Instead of simply deploying an application, this project focuses on **investigating the failure using Kubernetes debugging techniques**, identifying the root cause through evidence, and restoring the application.

The goal is to learn how Site Reliability Engineers (SREs) and DevOps Engineers troubleshoot production Kubernetes clusters.

---

# 🎯 Problem Statement

A payment service deployed on Kubernetes suddenly enters the **CrashLoopBackOff** state.

The application logs show:

```
panic:
connection to server at "postgres"
port 5432 failed:
Connection refused
```

As a DevOps Engineer, your responsibility is **not to guess the cause** but to investigate the incident systematically.

Possible causes include:

* Database failure
* Kubernetes DNS failure
* Secret misconfiguration
* Service routing issue
* Application configuration error

The challenge is to identify the exact root cause using Kubernetes debugging commands.

---

# 🎯 Objectives

By completing this project, you will learn how to:

* Build and containerize a Python Flask application
* Deploy applications to Kubernetes
* Create Kubernetes Secrets
* Deploy PostgreSQL
* Configure Kubernetes Services
* Understand Kubernetes Service Discovery
* Simulate a production outage
* Investigate CrashLoopBackOff incidents
* Read Kubernetes logs
* Interpret pod events
* Verify Kubernetes Services
* Inspect Endpoints
* Perform Root Cause Analysis (RCA)
* Recover failed applications

---

# 🏗 Architecture

```
                    User
                      │
                      ▼
             Payment Service
              (Flask API)
                      │
                      │
                      ▼
             Kubernetes Service
                (postgres)
                      │
                      ▼
                PostgreSQL Pod
```

---

# 📁 Project Structure

```
crashloopbackoff-investigation/

│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   ├── postgres.yaml
│   ├── secret.yaml
│   └── service.yaml
│
└── README.md
```

---

# 🛠 Technologies Used

* Kubernetes
* Minikube
* Docker
* Python
* Flask
* PostgreSQL
* kubectl

---

# ⚙ Prerequisites

Before starting, install the following:

* Docker
* Minikube
* kubectl
* Python 3
* Git

Verify the installation:

```bash
docker --version

kubectl version --client

minikube version
```

---

# 🚀 Step 1 – Create the Project

Create the project folders.

```bash
mkdir crashloopbackoff-investigation

cd crashloopbackoff-investigation

mkdir app

mkdir k8s
```

### Why?

Organizing the project improves maintainability and separates the application code from Kubernetes manifests.

---

# 🚀 Step 2 – Build the Flask Payment Service

The payment service attempts to connect to PostgreSQL **during application startup**.

If the database connection succeeds:

```
Application Starts
```

If the database connection fails:

```
Application Exits
```

The application intentionally exits with:

```python
exit(1)
```

This allows Kubernetes to detect the failure and restart the container.

Eventually Kubernetes marks the pod as:

```
CrashLoopBackOff
```

This behavior intentionally mimics real production applications that cannot function without their database.

---

# 🚀 Step 3 – Containerize the Application

Build a Docker image.

```bash
eval $(minikube docker-env)

cd app

docker build -t payment-service:v1 .
```

Verify:

```bash
docker image ls
```

You should see:

```
payment-service    v1
```

---

# 🚀 Step 4 – Create Kubernetes Resources

Deploy the following resources.

### Secret

Stores database credentials securely.

```
postgres-secret
```

Instead of hardcoding passwords inside the application, Kubernetes injects them as environment variables.

---

### PostgreSQL Deployment

Deploys the PostgreSQL database.

Responsibilities:

* Creates PostgreSQL Pod
* Runs database
* Accepts TCP connections

---

### PostgreSQL Service

Provides stable networking.

Without a Service:

```
Application cannot locate PostgreSQL.
```

The Service always has the DNS name:

```
postgres
```

---

### Payment Service Deployment

Deploys the Flask application.

Environment Variables:

```
DB_HOST

DB_PORT

DB_USER

DB_PASSWORD

DB_NAME
```

These values are supplied by Kubernetes.

---

# 🚀 Step 5 – Deploy Everything

```bash
kubectl apply -f k8s/
```

Verify:

```bash
kubectl get pods
```

Expected:

```
payment-service     Running

postgres            Running
```

At this point the application is healthy.

---

# 🚀 Step 6 – Simulate a Production Failure

A real engineer must know how to investigate failures.

Instead of waiting for production incidents, we intentionally create one.

Scale PostgreSQL to zero replicas.

```bash
kubectl scale deployment postgres --replicas=0
```

This removes the PostgreSQL Pod.

Notice that the Service still exists.

---

# 🚀 Step 7 – Force the Application to Restart

Restart the payment service.

```bash
kubectl rollout restart deployment payment-service
```

Now the application starts again.

During startup it attempts:

```
Connect to PostgreSQL
```

But PostgreSQL no longer exists.

The application exits.

Kubernetes restarts it repeatedly.

Eventually:

```
CrashLoopBackOff
```

---

# 🔍 Investigation Process

A professional engineer never guesses.

Always investigate using evidence.

---

## 1. Check Pod Status

```bash
kubectl get pods
```

Result:

```
CrashLoopBackOff
```

---

## 2. Read Logs

```bash
kubectl logs <pod-name>
```

Result:

```
Connection refused
```

Logs provide the first clue.

---

## 3. Describe the Pod

```bash
kubectl describe pod <pod-name>
```

Look for:

* Exit Code
* Restart Count
* Events
* Container State

This explains why Kubernetes is restarting the container.

---

## 4. Check Deployments

```bash
kubectl get deployment
```

Result:

```
postgres

0/0
```

Database is not running.

---

## 5. Check Services

```bash
kubectl get svc
```

Result:

```
postgres
```

The Service still exists.

---

## 6. Check Endpoints

```bash
kubectl get endpoints
```

Result:

```
postgres

<none>
```

This is the most important observation.

The Service has no backend Pods.

Traffic has nowhere to go.

---

# 🧠 Root Cause Analysis

## Was it DNS?

No.

DNS resolved the hostname correctly.

```
postgres

↓

10.x.x.x
```

DNS was functioning normally.

---

## Was it a Secret issue?

No.

Secrets were loaded successfully.

Authentication never occurred because the application could not establish a TCP connection.

---

## Was it a Service issue?

No.

The Service existed correctly.

---

## Was it a Database issue?

Yes.

The PostgreSQL Deployment had zero running Pods.

The Service had no Endpoints.

The application could not connect during startup.

The container exited with Exit Code 1.

Kubernetes restarted it repeatedly.

Finally:

```
CrashLoopBackOff
```

---

# ✅ Recovery

Restore PostgreSQL.

```bash
kubectl scale deployment postgres --replicas=1
```

Verify:

```bash
kubectl get pods
```

Restart payment service.

```bash
kubectl rollout restart deployment payment-service
```

Everything returns to normal.

---

# 🎓 Key Concepts Learned

* Kubernetes Deployments
* Pods
* Services
* Secrets
* Environment Variables
* Service Discovery
* DNS Resolution
* Endpoints
* CrashLoopBackOff
* Pod Lifecycle
* Container Exit Codes
* Kubernetes Events
* Root Cause Analysis
* Incident Response
* Production Debugging

---

# 💡 Interview Questions

### What is CrashLoopBackOff?

A Kubernetes pod state indicating that a container repeatedly starts, crashes, and Kubernetes backs off before attempting another restart.

---

### What causes CrashLoopBackOff?

* Application crash
* Missing dependency
* Database unavailable
* Invalid configuration
* Secret errors
* Startup failures

---

### What is the difference between a Service and an Endpoint?

A Service provides a stable virtual IP and DNS name.

Endpoints represent the actual backend Pods that receive traffic.

A Service without Endpoints cannot forward requests.

---

### Why did DNS work in this project?

The hostname `postgres` successfully resolved to the Service IP.

The failure occurred after DNS resolution because there was no backend database Pod listening on port 5432.

---

### Why was the root cause not a Secret issue?

Secrets were injected successfully.

The application failed before authentication because the TCP connection itself could not be established.

---

# 📚 Skills Demonstrated

* Docker Image Creation
* Kubernetes Application Deployment
* Secret Management
* PostgreSQL Deployment
* Kubernetes Networking
* Service Discovery
* Incident Simulation
* CrashLoopBackOff Investigation
* Root Cause Analysis
* Production Troubleshooting
* Kubernetes Recovery Procedures

---

# 🏁 Conclusion

This project demonstrates how to investigate a real Kubernetes production incident rather than simply deploying an application. By intentionally recreating a `CrashLoopBackOff` scenario and following a structured troubleshooting process, you learn to identify failures using logs, pod descriptions, services, deployments, and endpoints instead of relying on assumptions.

The investigation concludes that the failure is caused by the PostgreSQL deployment being unavailable, leaving the Service with no endpoints. Restoring the database and restarting the application returns the system to a healthy state.

The techniques practiced in this lab closely resemble the workflow followed by DevOps Engineers and Site Reliability Engineers (SREs) when diagnosing and resolving production Kubernetes incidents.
