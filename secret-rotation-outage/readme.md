# Exercise 13 – Secret Rotation Outage (Kubernetes Incident Response)

## Overview

In modern cloud-native applications, secrets such as database passwords, API keys, authentication tokens, and certificates should never be hardcoded inside application code or container images. Instead, they are stored securely using Kubernetes Secrets or external secret management systems like AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault.

Organizations periodically rotate secrets to reduce the risk of credential compromise. However, many production incidents occur because applications continue using old credentials after the secret has been rotated.

This project simulates one of those real-world incidents.

A payment service reads an API token from a Kubernetes Secret during startup. The secret is later rotated, but the running pods are not restarted immediately. As a result, the application continues using the old token, causing authentication failures until the deployment is restarted.

This exercise demonstrates how Kubernetes Secrets behave, why secret rotation can cause outages, and how to investigate and recover from the issue.

---

# Objectives

After completing this project, you will understand how to:

* Create and manage Kubernetes Secrets
* Inject Secrets into containers as environment variables
* Deploy applications using Kubernetes Deployments
* Simulate secret rotation
* Investigate authentication failures
* Identify why updated Secrets are not immediately reflected inside running Pods
* Recover applications using a Rolling Restart
* Perform structured Kubernetes incident response

---

# Real-World Scenario

Your company follows a security policy that automatically rotates API tokens every 30 days.

Yesterday, the security team rotated the payment service authentication token.

Soon after the rotation, customers began reporting payment failures.

Monitoring dashboards showed an increase in HTTP 401 Unauthorized responses.

Application logs indicated repeated authentication failures.

During the investigation, engineers discovered that the Kubernetes Secret contained the new token, but the running application Pods were still using the previous value.

Your responsibility as the DevOps Engineer is to identify the root cause, restore the service, and document the incident.

---

# Architecture

```
                     Client
                        │
                        ▼
               Payment Service
                        │
                        ▼
               Kubernetes Deployment
                        │
                        ▼
              Environment Variable
                        │
                        ▼
               Kubernetes Secret
                        │
                        ▼
         (Simulated Secret Rotation)
```

---

# Technologies Used

* Kubernetes
* Minikube
* Docker
* Python
* Flask
* kubectl
* Linux

---

# Prerequisites

Before starting this project, you should understand:

* Kubernetes Pods
* Deployments
* Services
* Secrets
* Docker Images
* Basic Linux Commands
* kubectl
* Python (Basic)

---

# Project Structure

```
exercise-13-secret-rotation-outage/

│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── secret.yaml
│
├── docs/
│
├── README.md
└── commands.md
```

---

# Project Workflow

## Phase 1 – Build the Application

A simple Flask payment service was created.

The application reads an API token from a Kubernetes Secret during startup.

```
API_TOKEN = payment123
```

The service validates incoming Authorization headers.

Correct token:

```
Payment Successful
```

Incorrect token:

```
401 Unauthorized
```

---

## Phase 2 – Deploy to Kubernetes

The application was containerized using Docker.

The Docker image was built inside the Minikube Docker environment.

A Kubernetes Secret stored the API token.

The Deployment injected the Secret as an environment variable.

The Service exposed the application inside the cluster.

The application was verified using curl requests.

---

## Phase 3 – Simulate Secret Rotation

The API token stored inside the Kubernetes Secret was changed.

Old Token

```
payment123
```

↓

New Token

```
payment456
```

However, the Deployment was intentionally left running without restarting the Pods.

---

# Incident Symptoms

After rotating the secret:

Users started receiving

```
401 Unauthorized
```

The new authentication token failed.

Surprisingly, the old authentication token still worked.

This indicated that the application had not loaded the updated Secret.

---

# Investigation Process

The following investigation steps were performed:

### Step 1

Verified application logs.

Observed repeated authentication failures.

---

### Step 2

Verified the Kubernetes Secret.

```
kubectl get secret payment-secret \
-o jsonpath="{.data.API_TOKEN}" | base64 -d
```

Result

```
payment456
```

The Secret had been updated successfully.

---

### Step 3

Verified the Deployment.

Pods were still running using environment variables loaded during startup.

No automatic refresh had occurred.

---

### Step 4

Confirmed the behaviour.

```
Authorization: payment456
```

↓

```
401 Unauthorized
```

Old token

```
Authorization: payment123
```

↓

```
Payment Successful
```

This confirmed that the running Pods were still using the old Secret.

---

# Root Cause Analysis

The application reads the API token from an environment variable only once during container startup.

Although the Kubernetes Secret was updated successfully, Kubernetes does not automatically update environment variables inside already-running containers.

Since the Pods were never restarted after the Secret rotation, the application continued using the old API token.

This resulted in authentication failures for clients using the newly rotated credentials.

---

# Resolution

A rolling restart of the Deployment was performed.

```
kubectl rollout restart deployment payment-service
```

New Pods were created.

Each new Pod loaded the updated Kubernetes Secret during startup.

The application successfully authenticated using the new token.

---

# Why Does This Happen?

Kubernetes Secrets behave differently depending on how they are consumed.

Secrets injected as environment variables are loaded only when a container starts.

Updating the Secret object does not automatically refresh environment variables inside running containers.

Applications must be restarted to read the updated values.

This behavior frequently causes production incidents after password or token rotation.

---

# Lessons Learned

This project demonstrates several important Kubernetes concepts:

* Kubernetes Secrets are not automatically refreshed inside environment variables.
* Updating a Secret does not restart Pods.
* Rolling restarts are required after secret rotation.
* Authentication failures should always include verification of Secret values.
* Proper incident investigation should verify both the Secret object and the running application.
* Understanding Kubernetes Secret behavior is critical for production reliability.

---

# Challenges Faced

During this project, several practical issues were encountered and resolved:

* Port forwarding stopped after the Deployment rollout because the old Pods were terminated.
* The application continued using the old token until the Pods were restarted.
* Verifying environment variables inside running Pods helped confirm the root cause.
* Understanding how Kubernetes injects Secrets into containers clarified why the issue occurred.

These troubleshooting steps closely resemble real-world Kubernetes production debugging.

---

# Skills Gained

By completing this exercise, I gained practical experience with:

* Kubernetes Secrets
* Secret Rotation
* Kubernetes Deployments
* Environment Variables
* Docker
* Minikube
* Incident Response
* Root Cause Analysis
* Rolling Restart Strategy
* Kubernetes Troubleshooting
* Production Debugging
* Authentication Failure Analysis

---

# Key Takeaways

One of the most important lessons from this project is that updating a Kubernetes Secret does not automatically update environment variables inside running containers.

Applications that depend on Secrets loaded during startup require a Pod restart or rolling deployment after secret rotation.

Understanding this behavior is essential for designing reliable Kubernetes applications and responding effectively to authentication-related production incidents.

This exercise closely mirrors real-world DevOps and Site Reliability Engineering (SRE) scenarios where secret rotation, security compliance, and application availability must all be managed carefully.

---

# Cleanup

```
kubectl delete deployment payment-service

kubectl delete service payment-service

kubectl delete secret payment-secret

minikube stop

minikube delete
```

---

# Conclusion

This project simulated a real production incident involving Kubernetes Secret rotation.

By intentionally reproducing the outage, investigating the symptoms, identifying the root cause, and recovering the application through a rolling restart, this exercise provided hands-on experience with one of the most common Kubernetes operational issues.

The knowledge gained from this project directly applies to enterprise Kubernetes environments where secure secret management and incident response are critical components of modern DevOps practices.
