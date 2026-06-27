# Exercise 04 – External Secrets Failure

## Overview

This exercise demonstrates how Kubernetes securely retrieves secrets from **AWS Secrets Manager** using the **External Secrets Operator (ESO)**.

Instead of storing sensitive credentials inside Kubernetes manifests or Git repositories, External Secrets synchronizes secrets from AWS Secrets Manager into Kubernetes Secrets.

A production failure was intentionally reproduced by referencing a non-existent secret in AWS Secrets Manager. This caused the External Secrets Operator to fail synchronization, resulting in a `SecretSyncedError`.

The incident was investigated, the root cause was identified, and the synchronization was successfully restored.

---

# Objective

* Install External Secrets Operator using Helm.
* Configure AWS Secrets Manager integration.
* Create a SecretStore.
* Synchronize secrets into Kubernetes.
* Understand the External Secrets workflow.
* Reproduce a secret synchronization failure.
* Investigate the failure.
* Perform Root Cause Analysis (RCA).
* Restore secret synchronization.

---

# Technologies Used

* Amazon EKS
* Kubernetes
* AWS Secrets Manager
* External Secrets Operator
* Helm
* kubectl
* AWS CLI

---

# Architecture

```text
                AWS Secrets Manager
                        │
                        ▼
                 SecretStore (AWS)
                        │
                        ▼
              External Secrets Operator
                        │
                        ▼
                 ExternalSecret Resource
                        │
                        ▼
                 Kubernetes Secret
                        │
                        ▼
                    Application
```

---

# Environment

* Kubernetes Cluster : Amazon EKS
* Cloud Provider : AWS
* Region : ap-south-1
* Secret Store : AWS Secrets Manager
* Secret Name : app-secret
* Namespace : default

---

# Initial Working Configuration

AWS Secrets Manager contained the following secret:

```json
{
  "DB_USERNAME": "admin",
  "DB_PASSWORD": "supersecret123",
  "JWT_SECRET": "jwt-secret-key"
}
```

A SecretStore was configured to authenticate with AWS Secrets Manager.

An ExternalSecret referenced the AWS secret and synchronized it into Kubernetes.

Synchronization status:

```text
Ready = True

Reason = SecretSynced
```

The Kubernetes Secret was created automatically by the External Secrets Operator.

---

# Production Incident

The ExternalSecret configuration was intentionally modified.

Original configuration:

```yaml
remoteRef:
  key: app-secret
```

Modified configuration:

```yaml
remoteRef:
  key: app-secret-broken
```

Since the secret `app-secret-broken` did not exist in AWS Secrets Manager, synchronization failed.

---

# Observed Behavior

The ExternalSecret reported:

```text
Ready = False

Reason = SecretSyncedError

Message:
could not get secret data from provider
```

Events:

```text
error processing spec.data[0]

Secret does not exist
```

The Kubernetes Secret could not be synchronized because the requested AWS secret was unavailable.

---

# Root Cause Analysis (RCA)

## Incident

Application secrets could not be synchronized from AWS Secrets Manager.

---

## Investigation

### Step 1

Verified External Secrets Operator.

Status:

* Running

---

### Step 2

Verified SecretStore.

Status:

* Healthy

---

### Step 3

Inspected ExternalSecret.

Observed:

```text
Ready=False

Reason=SecretSyncedError
```

---

### Step 4

Reviewed Kubernetes Events.

Observed:

```text
Secret does not exist
```

---

### Step 5

Verified AWS Secrets Manager.

Existing secret:

```text
app-secret
```

Referenced secret:

```text
app-secret-broken
```

The referenced secret did not exist.

---

# Root Cause

The ExternalSecret referenced a non-existent AWS Secrets Manager secret (`app-secret-broken`).

The External Secrets Operator failed to retrieve the requested secret and therefore could not synchronize the Kubernetes Secret.

---

# Resolution

The ExternalSecret configuration was corrected.

Changed:

```yaml
key: app-secret-broken
```

Back to:

```yaml
key: app-secret
```

After applying the corrected configuration:

```text
Ready=True

Reason=SecretSynced

Message=secret synced
```

The Kubernetes Secret was successfully synchronized again.

---

# External Secrets Workflow

```text
AWS Secrets Manager

        │

        ▼

SecretStore

        │

        ▼

ExternalSecret

        │

        ▼

External Secrets Operator

        │

        ▼

Kubernetes Secret

        │

        ▼

Application
```

---

# Security Benefits

Using External Secrets provides several advantages:

* Secrets are not stored in Git repositories.
* Secrets are not hardcoded inside Kubernetes manifests.
* Centralized secret management using AWS Secrets Manager.
* Automatic synchronization.
* Supports secret rotation.
* Reduces the risk of credential exposure.

---

# Production Best Practices

* Store all application secrets inside AWS Secrets Manager.
* Never commit secrets into Git.
* Use External Secrets Operator for synchronization.
* Monitor ExternalSecret status regularly.
* Investigate `SecretSyncedError` immediately.
* Prefer IAM Roles for Service Accounts (IRSA) over static AWS credentials in production.

---

# Key Learnings

* Installed External Secrets Operator using Helm.
* Connected Kubernetes with AWS Secrets Manager.
* Created a SecretStore.
* Created an ExternalSecret.
* Understood automatic Kubernetes Secret creation.
* Learned the complete External Secrets synchronization workflow.
* Reproduced a real production synchronization failure.
* Performed Root Cause Analysis.
* Restored successful synchronization.

---

# Interview Questions

## What is External Secrets Operator?

External Secrets Operator synchronizes secrets from external secret management systems such as AWS Secrets Manager into Kubernetes Secrets.

---

## Why use AWS Secrets Manager?

AWS Secrets Manager securely stores sensitive information such as passwords, API keys, database credentials and supports automatic secret rotation.

---

## What is a SecretStore?

A SecretStore defines how External Secrets authenticates and connects to an external secret provider.

---

## What is an ExternalSecret?

An ExternalSecret tells the External Secrets Operator which external secret to retrieve and how it should be converted into a Kubernetes Secret.

---

## What caused the SecretSyncedError?

The ExternalSecret referenced a secret that did not exist in AWS Secrets Manager, preventing synchronization.

---

## How was the issue resolved?

The incorrect secret name was replaced with the correct AWS Secrets Manager secret (`app-secret`), allowing the External Secrets Operator to synchronize successfully.

---

# Outcome

Successfully built a production-style External Secrets architecture using AWS Secrets Manager, reproduced a real synchronization failure, investigated the root cause using Kubernetes resources and events, restored synchronization, and verified successful secret creation inside Kubernetes.
