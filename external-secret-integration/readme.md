# AWS Secrets Manager Integration with Kubernetes using External Secrets Operator

## Project Overview

This project demonstrates secure secret management in Kubernetes using AWS Secrets Manager and External Secrets Operator (ESO).

Instead of hardcoding sensitive information such as database credentials, API keys, and JWT secrets inside application code or Kubernetes manifests, secrets are stored securely in AWS Secrets Manager and automatically synchronized into Kubernetes Secrets.

This approach follows modern DevOps and Cloud Security best practices by centralizing secret management and eliminating secret sprawl.

---

## Problem Statement

Applications require sensitive information such as:

* Database usernames
* Database passwords
* API keys
* JWT secrets
* Access tokens

A common but insecure approach is to hardcode these values inside source code or Kubernetes manifests.

Example:

```yaml
env:
  - name: DB_PASSWORD
    value: password123
```

This introduces security risks because:

* Secrets become visible in Git repositories.
* Secrets are difficult to rotate.
* Multiple applications may maintain duplicate copies.
* Unauthorized users may gain access to credentials.

---

## Solution

Store secrets securely in AWS Secrets Manager and use External Secrets Operator to automatically synchronize them into Kubernetes Secrets.

Architecture:

```text
AWS Secrets Manager
        │
        ▼
SecretStore
        │
        ▼
External Secrets Operator
        │
        ▼
ExternalSecret
        │
        ▼
Kubernetes Secret
        │
        ▼
Application Pod
```

---

## Objectives

* Learn centralized secret management.
* Understand Kubernetes Operators.
* Understand Custom Resource Definitions (CRDs).
* Integrate AWS Secrets Manager with Kubernetes.
* Automate secret synchronization.
* Eliminate hardcoded credentials.

---

## Technologies Used

* AWS Secrets Manager
* Kubernetes
* Minikube
* kubectl
* Helm
* External Secrets Operator
* AWS CLI

---

# Project Workflow

## Step 1: Start Kubernetes Cluster

Start Minikube:

```bash
minikube start
```

Verify cluster:

```bash
kubectl get nodes
```

Expected:

```text
NAME       STATUS
minikube   Ready
```

### Why?

External Secrets Operator runs inside Kubernetes. A cluster is required before deploying the operator.

---

## Step 2: Verify AWS Authentication

Check AWS CLI:

```bash
aws --version
```

Verify authenticated identity:

```bash
aws sts get-caller-identity
```

### Why?

External Secrets Operator must access AWS Secrets Manager using valid AWS credentials.

---

## Step 3: Create Secret in AWS Secrets Manager

Create a secret:

```bash
aws secretsmanager create-secret \
  --name app-secret \
  --secret-string '{
    "DB_USERNAME":"admin",
    "DB_PASSWORD":"supersecret123",
    "JWT_SECRET":"jwt-secret-key"
  }'
```

Verify:

```bash
aws secretsmanager get-secret-value \
  --secret-id app-secret
```

Expected Output:

```json
{
  "DB_USERNAME":"admin",
  "DB_PASSWORD":"supersecret123",
  "JWT_SECRET":"jwt-secret-key"
}
```

### Why?

AWS Secrets Manager becomes the central source of truth for application secrets.

---

## Step 4: Install External Secrets Operator

Add Helm repository:

```bash
helm repo add external-secrets https://charts.external-secrets.io
```

Update repositories:

```bash
helm repo update
```

Install External Secrets Operator:

```bash
helm install external-secrets \
external-secrets/external-secrets \
-n external-secrets \
--create-namespace
```

Verify:

```bash
kubectl get pods -n external-secrets
```

Expected:

```text
external-secrets-xxxxx Running
```

### Why?

External Secrets Operator acts as the bridge between Kubernetes and AWS Secrets Manager.

---

## Step 5: Create AWS Credentials Secret

Create Kubernetes Secret containing AWS credentials:

```bash
kubectl create secret generic awssm-secret \
--from-literal=access-key=<AWS_ACCESS_KEY_ID> \
--from-literal=secret-access-key=<AWS_SECRET_ACCESS_KEY>
```

Verify:

```bash
kubectl get secret
```

### Why?

The External Secrets Operator pod requires AWS credentials to access Secrets Manager.

---

## Step 6: Create SecretStore

Create:

### secretstore.yaml

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: aws-secret-store
spec:
  provider:
    aws:
      service: SecretsManager
      region: ap-south-1
      auth:
        secretRef:
          accessKeyIDSecretRef:
            name: awssm-secret
            key: access-key
          secretAccessKeySecretRef:
            name: awssm-secret
            key: secret-access-key
```

Apply:

```bash
kubectl apply -f secretstore.yaml
```

Verify:

```bash
kubectl describe secretstore aws-secret-store
```

Expected:

```text
store validated
```

### Why?

A SecretStore tells External Secrets Operator:

* Which provider to use
* Which region to access
* Which credentials to use

---

## Step 7: Create ExternalSecret

Create:

### externalsecret.yaml

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: app-secret-sync
spec:
  refreshInterval: 1m

  secretStoreRef:
    name: aws-secret-store
    kind: SecretStore

  target:
    name: app-secret-k8s

  data:
    - secretKey: DB_USERNAME
      remoteRef:
        key: app-secret
        property: DB_USERNAME

    - secretKey: DB_PASSWORD
      remoteRef:
        key: app-secret
        property: DB_PASSWORD

    - secretKey: JWT_SECRET
      remoteRef:
        key: app-secret
        property: JWT_SECRET
```

Apply:

```bash
kubectl apply -f externalsecret.yaml
```

Verify:

```bash
kubectl get externalsecret
```

Expected:

```text
NAME              READY
app-secret-sync   True
```

### Why?

ExternalSecret defines:

* Which AWS Secret to fetch
* Which properties to extract
* Which Kubernetes Secret to create

---

## Step 8: Verify Secret Synchronization

List secrets:

```bash
kubectl get secret
```

Expected:

```text
app-secret-k8s
```

Describe secret:

```bash
kubectl describe secret app-secret-k8s
```

Expected:

```text
DB_USERNAME
DB_PASSWORD
JWT_SECRET
```

---

## Step 9: Verify Secret Values

Decode values:

```bash
kubectl get secret app-secret-k8s \
-o jsonpath='{.data.DB_USERNAME}' | base64 -d
```

Output:

```text
admin
```

Verify password:

```bash
kubectl get secret app-secret-k8s \
-o jsonpath='{.data.DB_PASSWORD}' | base64 -d
```

Verify JWT secret:

```bash
kubectl get secret app-secret-k8s \
-o jsonpath='{.data.JWT_SECRET}' | base64 -d
```

---

# Key Concepts Learned

## AWS Secrets Manager

A fully managed AWS service for securely storing and retrieving secrets.

Benefits:

* Encryption at rest
* IAM-based access control
* Secret rotation
* Audit logging

---

## Kubernetes Secret

Stores sensitive information inside Kubernetes.

Examples:

* Passwords
* API Keys
* Tokens

---

## SecretStore

Defines the connection between Kubernetes and AWS Secrets Manager.

---

## ExternalSecret

Defines:

* Which external secret to retrieve
* Which fields to synchronize
* Which Kubernetes Secret to create

---

## External Secrets Operator

A Kubernetes Operator that continuously synchronizes secrets from external providers into Kubernetes.

---

## Reconciliation Loop

The operator continuously checks:

```text
AWS Secret Changed?
        │
        ▼
Update Kubernetes Secret
```

This automatic synchronization process is called reconciliation.

---

# Project Outcome

Successfully integrated AWS Secrets Manager with Kubernetes using External Secrets Operator.

Implemented:

* Secure secret storage
* Automatic secret synchronization
* Centralized secret management
* Kubernetes-native secret consumption

---

# Cleanup

Delete External Secret:

```bash
kubectl delete externalsecret app-secret-sync
```

Delete SecretStore:

```bash
kubectl delete secretstore aws-secret-store
```

Delete Kubernetes Secrets:

```bash
kubectl delete secret app-secret-k8s
kubectl delete secret awssm-secret
```

Delete External Secrets Operator:

```bash
helm uninstall external-secrets -n external-secrets
```

Delete Minikube Cluster:

```bash
minikube delete
```

---


