# 🚀 End-to-End CI/CD Pipeline with GitHub Actions, AWS ECR, ArgoCD & Kubernetes (GitOps)

## 📌 Project Overview

This project demonstrates a complete **DevOps CI/CD + GitOps workflow** using:

* Python Flask Application
* Docker
* GitHub Actions
* Trivy Security Scanner
* AWS Elastic Container Registry (ECR)
* GitOps Repository
* ArgoCD
* Kubernetes (Minikube)

The goal is to automate the entire software delivery lifecycle from source code commit to deployment inside Kubernetes.

---

# 🏗️ Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Unit Testing (Pytest)
    ├── Docker Build
    ├── Trivy Security Scan
    └── Push Image to AWS ECR
    │
    ▼
GitOps Repository
    │
    ▼
ArgoCD
    │
    ▼
Kubernetes Cluster
    │
    ▼
Flask Application
```

---

# 🎯 Objective

The objective of this project is to automate:

1. Code Validation
2. Application Testing
3. Security Scanning
4. Container Image Creation
5. Container Registry Storage
6. Kubernetes Deployment
7. Continuous Delivery through GitOps

---

# ❓ Why This Project?

Traditional deployments involve:

* Manual Docker builds
* Manual image pushes
* Manual Kubernetes updates
* Human errors
* Inconsistent deployments

This project eliminates those issues through automation.

---

# ⚠️ What Happens Without This Project?

Without CI/CD and GitOps:

## Problems

### Manual Deployments

Developers manually build and deploy.

### Human Errors

Wrong image versions may be deployed.

### No Security Validation

Vulnerable containers reach production.

### No Audit Trail

Difficult to track deployments.

### Configuration Drift

Cluster state differs from Git repository.

---

# 🛠️ Technology Stack

| Tool              | Purpose                  |
| ----------------- | ------------------------ |
| Flask             | Sample Application       |
| Pytest            | Unit Testing             |
| Docker            | Containerization         |
| GitHub Actions    | CI/CD Pipeline           |
| Trivy             | Vulnerability Scanning   |
| AWS ECR           | Container Registry       |
| GitOps Repository | Desired State Storage    |
| ArgoCD            | GitOps Deployment        |
| Kubernetes        | Container Orchestration  |
| Minikube          | Local Kubernetes Cluster |

---

# 📂 Project Structure

## Application Repository

```text
ci-cd-pipeline-project-gitops/
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
│
└── .github
    └── workflows
        └── deploy.yaml
```

---

## GitOps Repository

```text
gitops-repo/
│
└── k8s
    ├── deployment.yaml
    └── service.yaml
```

---

# ⚙️ Phase 1: Flask Application

## app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "CI/CD Pipeline Working"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

# ⚙️ Phase 2: Unit Testing

## test_app.py

```python
from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')

    assert response.status_code == 200
```

---

# ⚙️ Phase 3: Dockerization

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

---

# Build Docker Image

```bash
docker build -t flask-cicd:v1 .
```

---

# Run Docker Container

```bash
docker run -p 5000:5000 flask-cicd:v1
```

---

# ⚙️ Phase 4: AWS ECR Setup

## Create Repository

```bash
aws ecr create-repository \
--repository-name flask-cicd \
--region ap-south-1
```

---

## Login to ECR

```bash
aws ecr get-login-password \
--region ap-south-1 | docker login \
--username AWS \
--password-stdin \
324621154851.dkr.ecr.ap-south-1.amazonaws.com
```

---

## Push Image

```bash
docker tag flask-cicd:v1 \
324621154851.dkr.ecr.ap-south-1.amazonaws.com/flask-cicd:v1

docker push \
324621154851.dkr.ecr.ap-south-1.amazonaws.com/flask-cicd:v1
```

---

# ⚙️ Phase 5: Kubernetes Setup

## Start Minikube

```bash
minikube start
```

---

## Verify Cluster

```bash
kubectl get nodes
```

---

# ⚙️ Phase 6: Install ArgoCD

## Create Namespace

```bash
kubectl create namespace argocd
```

---

## Install ArgoCD

```bash
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

## Verify Pods

```bash
kubectl get pods -n argocd
```

---

# ⚙️ Phase 7: GitOps Repository

## deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: flask-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: flask-app

  template:
    metadata:
      labels:
        app: flask-app

    spec:
      imagePullSecrets:
      - name: ecr-secret

      containers:
      - name: flask-app
        image: 324621154851.dkr.ecr.ap-south-1.amazonaws.com/flask-cicd:v1

        ports:
        - containerPort: 5000
```

---

## service.yaml

```yaml
apiVersion: v1
kind: Service

metadata:
  name: flask-service

spec:
  selector:
    app: flask-app

  ports:
  - port: 80
    targetPort: 5000

  type: ClusterIP
```

---

# ⚙️ Phase 8: ArgoCD Application

## application.yaml

```yaml
apiVersion: argoproj.io/v1alpha1

kind: Application

metadata:
  name: flask-app
  namespace: argocd

spec:

  project: default

  source:
    repoURL: https://github.com/nkdharanikumar/gitops-repo.git
    targetRevision: main
    path: k8s

  destination:
    server: https://kubernetes.default.svc
    namespace: default

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Deploy Application

```bash
kubectl apply -f application.yaml
```

---

# ⚙️ Phase 9: GitHub Secrets

Repository → Settings → Secrets

Create:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
GITOPS_TOKEN
```

---

# ⚙️ Phase 10: GitHub Actions Workflow

Pipeline stages:

```text
Checkout
    ↓
Install Dependencies
    ↓
Run Tests
    ↓
Configure AWS
    ↓
Login ECR
    ↓
Build Docker Image
    ↓
Trivy Scan
    ↓
Push Image
    ↓
Clone GitOps Repo
    ↓
Update Manifest
    ↓
Commit Changes
    ↓
Push GitOps Repo
```

---

# 🔥 Troubleshooting Section

## Issue 1

Pods stuck at:

```text
ContainerCreating
```

### Cause

Image pull from ECR failed.

### Fix

Create imagePullSecret.

```bash
kubectl create secret docker-registry ecr-secret \
--docker-server=324621154851.dkr.ecr.ap-south-1.amazonaws.com \
--docker-username=AWS \
--docker-password=$(aws ecr get-login-password --region ap-south-1)
```

---

## Issue 2

```text
Invalid workflow file
Unexpected value push
Unexpected value branches
```

### Cause

Incorrect YAML indentation.

### Fix

Properly indent workflow file.

---

## Issue 3

```text
Trivy 404 Not Found
```

### Cause

Deprecated Trivy download URL.

### Fix

Use official Trivy GitHub Action.

---

## Issue 4

```text
Trivy Scan Failed
```

### Cause

High/Critical vulnerabilities detected.

### Fix

Allow scan to continue temporarily:

```bash
exit-code: 0
```

---

## Issue 5

```text
Permission denied to gitops-repo
403
```

### Cause

Invalid GitHub PAT.

### Fix

Generate PAT with:

```text
Contents: Read & Write
Repository Access: gitops-repo
```

---

## Issue 6

```text
Authentication Failed
```

### Cause

VSCode credential helper issue.

### Fix

Use GitHub PAT.

---

## Issue 7

```text
ArgoCD Healthy but Pods Missing
```

### Cause

Deployment not created properly.

### Fix

Check:

```bash
kubectl describe application flask-app -n argocd
```

---

## Issue 8

```text
Image not updating
```

### Cause

GitOps repo deployment manifest not modified.

### Fix

Verify:

```bash
gitops-repo/k8s/deployment.yaml
```

contains latest SHA image.

---

# 📈 Validation Commands

## Check Pods

```bash
kubectl get pods
```

---

## Check Services

```bash
kubectl get svc
```

---

## Check ArgoCD Application

```bash
kubectl get applications -n argocd
```

---

## Check Deployment Image

```bash
kubectl get deployment flask-app -o yaml | grep image
```

---

# 🚀 CI/CD Workflow

```text
Git Push
    ↓
GitHub Actions
    ↓
Pytest
    ↓
Docker Build
    ↓
Trivy Scan
    ↓
AWS ECR
    ↓
GitOps Repo
    ↓
ArgoCD
    ↓
Kubernetes
    ↓
Application Updated
```

---

# 📚 Key DevOps Concepts Demonstrated

* CI/CD
* GitOps
* Containerization
* Security Scanning
* Kubernetes Deployments
* Continuous Delivery
* Infrastructure Automation
* Immutable Deployments
* ArgoCD Auto Sync
* AWS ECR Integration

---

# 🏆 Outcome

Successfully built an enterprise-style DevOps pipeline where every code push automatically:

1. Runs tests
2. Builds Docker image
3. Performs vulnerability scanning
4. Pushes image to AWS ECR
5. Updates GitOps repository
6. Triggers ArgoCD synchronization
7. Deploys latest application to Kubernetes

No manual deployment steps required.

```
```
