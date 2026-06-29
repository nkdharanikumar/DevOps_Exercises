# Exercise 07 – AWS ALB Ingress Failure

## Overview

This exercise demonstrates how applications running on Amazon EKS are exposed to the internet using the **AWS Load Balancer Controller** and **Kubernetes Ingress**.

A production-ready environment was created using **IRSA (IAM Roles for Service Accounts)**, the AWS Load Balancer Controller, and an Application Load Balancer (ALB). After verifying the application was accessible, a production incident was intentionally introduced by misconfiguring the Ingress backend service.

The issue was investigated using Kubernetes resources and AWS components, the root cause was identified, and the configuration was restored.

---

# Objectives

* Understand Kubernetes Ingress.
* Learn how the AWS Load Balancer Controller works.
* Deploy an internet-facing Application Load Balancer.
* Configure Kubernetes Services and Ingress resources.
* Investigate ALB routing failures.
* Perform Root Cause Analysis (RCA).
* Restore application availability.

---

# Technologies Used

* Amazon EKS
* Kubernetes
* AWS Load Balancer Controller
* IAM Roles for Service Accounts (IRSA)
* Application Load Balancer (ALB)
* Helm
* kubectl
* AWS CLI
* NGINX

---

# Architecture

```text
                     Internet
                         │
                         ▼
          AWS Application Load Balancer
                         │
                         ▼
                Kubernetes Ingress
                         │
                         ▼
                ClusterIP Service
                         │
                         ▼
                    NGINX Pods
```

---

# Platform Components

Before beginning the exercise, the following platform components were available:

* Amazon EKS Cluster
* Metrics Server
* ArgoCD
* External Secrets Operator
* AWS Load Balancer Controller (Installed using IRSA)

---

# Environment

* Kubernetes Cluster: Amazon EKS
* Worker Nodes: 2
* Instance Type: t3.medium
* AWS Region: ap-south-1

---

# Phase 1 – Deploy Application

A simple NGINX Deployment was created.

Deployment:

* 2 Replicas
* NGINX 1.27
* Namespace: exercise-07

All Pods entered the Running state.

---

# Phase 2 – Create ClusterIP Service

A ClusterIP Service exposed the Deployment internally.

Service Name:

```text
web-service
```

The Service was verified using:

```bash
kubectl port-forward svc/web-service 8080:80 -n exercise-07
```

Opening:

```text
http://localhost:8080
```

displayed the default NGINX Welcome page.

This confirmed the application and Service layers were functioning correctly before introducing the Ingress.

---

# Phase 3 – Create Internet-Facing Ingress

An Ingress resource was created using:

* ingressClassName: alb
* internet-facing ALB
* IP target mode

The AWS Load Balancer Controller automatically created:

* Application Load Balancer
* Target Group
* Listener
* Listener Rules

Initially the ALB remained in the **Provisioning** state.

After provisioning completed, AWS assigned an external DNS name and the application became accessible through the browser.

---

# Production Incident

After confirming the application was working through the ALB, a configuration error was intentionally introduced.

The backend Service in the Ingress was changed from:

```yaml
service:
  name: web-service
```

to

```yaml
service:
  name: web-service-broken
```

The Service **web-service-broken** did not exist inside the cluster.

---

# Symptoms

Observed:

* ALB remained available.
* Pods continued Running.
* Deployment remained healthy.
* Browser requests failed.
* Kubernetes reported an invalid backend Service.

---

# Investigation

The first step was to inspect the Ingress.

```bash
kubectl describe ingress web-ingress -n exercise-07
```

Output:

```text
web-service-broken:80

(error: services "web-service-broken" not found)
```

This immediately identified the configuration problem.

---

# Root Cause Analysis (RCA)

## Incident

Application became unreachable through the Application Load Balancer.

---

## Investigation

### Step 1

Verified Pods.

Result:

```text
Running
Running
```

Pods were healthy.

---

### Step 2

Verified Deployment.

Deployment was Available.

---

### Step 3

Verified Service.

The expected Service:

```text
web-service
```

existed.

However, the Ingress referenced:

```text
web-service-broken
```

which did not exist.

---

### Step 4

Reviewed Ingress.

The backend displayed:

```text
services "web-service-broken" not found
```

---

# Root Cause

The Kubernetes Ingress referenced a Service name that did not exist.

Because the AWS Load Balancer Controller could not associate the Ingress with a valid Kubernetes Service, traffic could not be forwarded to the application Pods.

The infrastructure remained healthy, but the application routing configuration was incorrect.

---

# Resolution

The Ingress backend was restored.

Previous (broken):

```yaml
service:
  name: web-service-broken
```

Updated:

```yaml
service:
  name: web-service
```

The updated configuration was applied.

Within a short period, the AWS Load Balancer Controller reconciled the changes and traffic was successfully routed back to the application.

The NGINX Welcome page became accessible again through the ALB.

---

# Request Flow

Working configuration:

```text
Internet
     │
     ▼
Application Load Balancer
     │
     ▼
Ingress
     │
     ▼
web-service
     │
     ▼
NGINX Pods
```

Broken configuration:

```text
Internet
     │
     ▼
Application Load Balancer
     │
     ▼
Ingress
     │
     ▼
web-service-broken
     │
     ▼
Service Not Found
```

---

# AWS Components Automatically Created

The AWS Load Balancer Controller created:

* Application Load Balancer
* Target Group
* Listener
* Listener Rules
* Security Group Configuration
* Target Registration

No AWS resources were manually created.

---

# Production Best Practices

* Use IRSA instead of static AWS credentials.
* Validate Service names before modifying Ingress resources.
* Test the Service layer before exposing applications externally.
* Monitor AWS Load Balancer Controller logs.
* Use `kubectl describe ingress` to verify backend configuration.
* Apply infrastructure changes gradually and validate each layer.

---

# Key Learnings

* Installed AWS Load Balancer Controller using IRSA.
* Understood Kubernetes Ingress architecture.
* Learned how ALBs are provisioned automatically.
* Verified internal Service communication.
* Investigated ALB provisioning.
* Diagnosed Ingress backend failures.
* Performed Root Cause Analysis.
* Restored application availability by correcting the backend Service.

---

# Interview Questions

## What is the AWS Load Balancer Controller?

It is a Kubernetes controller that watches Ingress resources and automatically provisions AWS Application Load Balancers and related networking resources.

---

## Why is IRSA recommended?

IRSA allows Kubernetes Pods to assume IAM Roles without storing AWS Access Keys inside the cluster.

---

## Why was the application unavailable?

The Ingress referenced a Kubernetes Service that did not exist.

Although the Pods, Deployment, and ALB were healthy, the controller could not route traffic because the backend Service name was incorrect.

---

## How do you troubleshoot ALB Ingress issues?

1. Verify Pods.
2. Verify Deployment.
3. Verify Service.
4. Describe the Ingress.
5. Check backend Service.
6. Inspect AWS Load Balancer Controller logs.
7. Verify ALB Target Groups.

---

## Why did `Successfully reconciled` appear even when the application was unavailable?

The controller successfully processed the Ingress resource itself. However, the referenced backend Service was invalid, preventing successful traffic routing.

---

# Outcome

Successfully deployed an internet-facing application on Amazon EKS using the AWS Load Balancer Controller and IRSA. Reproduced a real-world ALB routing failure caused by an invalid backend Service reference, identified the root cause through Kubernetes Ingress inspection, restored the correct Service configuration, and successfully recovered application availability.
