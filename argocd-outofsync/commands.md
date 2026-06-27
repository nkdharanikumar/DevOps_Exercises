# Exercise 03 – ArgoCD OutOfSync (GitOps Configuration Drift)

## Overview

This exercise demonstrates one of the most common GitOps incidents in Kubernetes environments: **configuration drift**.

An application was successfully deployed to an Amazon EKS cluster using ArgoCD. The desired state was stored in a Git repository. A manual modification was later made directly to the Kubernetes cluster using `kubectl scale`, causing the live state to differ from the desired state stored in Git.

ArgoCD detected this difference and marked the application as **OutOfSync** while reporting the application as **Healthy**.

This lab reproduces a real-world GitOps incident, explains why it occurred, how ArgoCD detected it, and how GitOps restores consistency.

---

# Objective

* Install and configure ArgoCD.
* Deploy an application using GitOps.
* Understand the GitOps workflow.
* Create configuration drift.
* Investigate the OutOfSync state.
* Perform Root Cause Analysis (RCA).
* Restore synchronization using ArgoCD.

---

# Technologies Used

* Amazon EKS
* Kubernetes
* ArgoCD
* GitHub
* Git
* kubectl
* Helm
* NGINX

---

# GitOps Architecture

```text
                GitHub Repository
                        │
                        │
                        ▼
                  ArgoCD Server
                        │
                        ▼
               Application Controller
                        │
                        ▼
                 Amazon EKS Cluster
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
     Deployment                     Service
        │
        ▼
      ReplicaSet
        │
   ┌────┴────┐
   ▼         ▼
 Pod 1     Pod 2     Pod 3
```

---

# Environment

* Kubernetes Cluster: Amazon EKS
* GitOps Tool: ArgoCD
* Repository: gitops-outage-sync
* Namespace: exercise-03
* Application: payment-service
* Container Image: nginx:1.27

---

# Initial Deployment

The application was deployed through ArgoCD using the manifests stored inside the Git repository.

Git repository configuration:

```yaml
spec:
  replicas: 3
```

Deployment Result:

* 3 Running Pods
* ClusterIP Service
* ArgoCD Status: Synced
* Application Health: Healthy

At this stage the live cluster and Git repository contained identical configurations.

---

# Production Incident

A manual scaling operation was performed directly against the Kubernetes cluster.

Command executed:

```bash
kubectl scale deployment payment-service \
  --replicas=5 \
  -n exercise-03
```

This bypassed Git entirely and modified the Deployment directly inside Kubernetes.

---

# Observed Behavior

ArgoCD reported:

```text
Status : OutOfSync

Health : Healthy
```

The application continued serving traffic successfully because all Pods were running correctly.

However, the live configuration no longer matched the desired configuration stored in Git.

---

# Root Cause Analysis (RCA)

## Desired State (Git)

```yaml
replicas: 3
```

## Live Cluster

```yaml
replicas: 5
```

The Deployment was modified manually using `kubectl scale`.

Because Git was not updated, ArgoCD detected configuration drift.

---

# Why was the Application Healthy?

Health and Sync Status measure different things.

## Health

Health answers:

> Is the application functioning correctly?

Since all Pods were running successfully, the application remained Healthy.

---

## Sync Status

Sync Status answers:

> Does the live cluster match Git?

Because the Deployment replicas differed from Git, ArgoCD reported the application as OutOfSync.

---

# Configuration Drift

Configuration Drift occurs when the live Kubernetes cluster differs from the desired configuration stored inside Git.

Example:

Git:

```yaml
replicas: 3
```

Cluster:

```yaml
replicas: 5
```

This mismatch is automatically detected by ArgoCD.

---

# Resolution

The application was restored using the ArgoCD **Sync** operation.

ArgoCD compared:

Desired State:

```yaml
replicas: 3
```

Live State:

```yaml
replicas: 5
```

It reconciled the Deployment back to:

```yaml
replicas: 3
```

Application Status after synchronization:

```text
Status : Synced

Health : Healthy
```

---

# Production Best Practices

* Never modify Kubernetes resources manually when using GitOps.
* Treat Git as the single source of truth.
* Perform all configuration changes through Pull Requests.
* Enable automatic synchronization where appropriate.
* Enable Self Heal to automatically correct configuration drift.
* Monitor ArgoCD applications for OutOfSync status.

---

# Key Learnings

* Understood GitOps architecture.
* Installed ArgoCD using Helm.
* Connected GitHub repository with ArgoCD.
* Deployed applications directly from Git.
* Learned how ArgoCD continuously compares Git and the live cluster.
* Reproduced a real-world configuration drift incident.
* Investigated the OutOfSync state.
* Performed Root Cause Analysis.
* Restored synchronization using ArgoCD.

---

# Interview Questions

## What is GitOps?

GitOps is an operational model where Git acts as the single source of truth for infrastructure and application configurations. Changes are made through Git, and tools like ArgoCD continuously reconcile the live cluster with the desired state.

---

## What is Configuration Drift?

Configuration Drift occurs when the live Kubernetes resources differ from the desired configuration stored inside Git.

---

## Why was the application Healthy but OutOfSync?

The application was Healthy because all Pods and Services were functioning correctly.

It was OutOfSync because the Deployment configuration inside Kubernetes differed from the desired configuration stored in Git.

---

## How does ArgoCD detect OutOfSync?

ArgoCD continuously compares the desired manifests stored in Git with the live Kubernetes resources.

Any difference between them results in an OutOfSync status.

---

## What is Self Heal?

Self Heal is an ArgoCD feature that automatically restores Kubernetes resources back to the desired state stored in Git whenever configuration drift is detected.

---

# Outcome

Successfully reproduced a real GitOps configuration drift scenario, investigated why ArgoCD reported the application as **OutOfSync** while remaining **Healthy**, performed Root Cause Analysis, and restored the application to the desired state using GitOps synchronization.

