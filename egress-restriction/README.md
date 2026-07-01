# 🚀 Exercise 08 -- Egress Restriction Incident Investigation on Amazon EKS

## 📌 Project Overview

This project demonstrates how to investigate an egress connectivity
incident in an Amazon EKS cluster.

The exercise simulates an application attempting to access Amazon
DynamoDB while investigating the following networking components:

-   Kubernetes Network Policies
-   AWS Security Groups
-   Route Tables
-   VPC Endpoints

During the investigation, a default deny egress NetworkPolicy was
created. Although the policy was applied successfully, outbound traffic
was **not blocked** because the EKS cluster was not configured to
enforce Kubernetes NetworkPolicies.

------------------------------------------------------------------------

# 🎯 Incident

> **Application cannot access Amazon DynamoDB**

Goal:

-   Reproduce the incident
-   Investigate the networking stack
-   Identify the root cause
-   Document findings

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                 Amazon EKS Cluster
                        │
                Test Application Pod
                        │
              curl https://dynamodb...
                        │
                        ▼
               Amazon DynamoDB Endpoint
```

------------------------------------------------------------------------

# 🛠️ Technologies Used

-   Amazon EKS
-   Kubernetes
-   Amazon VPC
-   Amazon DynamoDB
-   AWS CLI
-   kubectl
-   eksctl

------------------------------------------------------------------------

# 📂 Project Structure

``` text
exercise-08-egress-restriction/
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── test-pod.yaml
│   └── network-policy.yaml
│
├── docs/
├── screenshots/
└── README.md
```

------------------------------------------------------------------------

# 🎯 Objectives

-   Create a test namespace
-   Deploy a network testing pod
-   Verify connectivity to DynamoDB
-   Apply a default deny egress NetworkPolicy
-   Investigate Security Groups
-   Investigate Route Tables
-   Investigate VPC Endpoints
-   Identify why traffic was still allowed

------------------------------------------------------------------------

# ⚙️ Prerequisites

-   AWS Account
-   Amazon EKS Cluster
-   kubectl
-   AWS CLI
-   eksctl

------------------------------------------------------------------------

# 🚀 Deployment Steps

## 1. Create Namespace

``` bash
kubectl apply -f kubernetes/namespace.yaml
```

------------------------------------------------------------------------

## 2. Deploy Test Pod

``` bash
kubectl apply -f kubernetes/test-pod.yaml
```

Verify:

``` bash
kubectl get pods -n egress-lab
```

------------------------------------------------------------------------

## 3. Test Connectivity

``` bash
kubectl exec -it -n egress-lab network-test -- sh
```

Inside the pod:

``` sh
curl https://dynamodb.ap-south-1.amazonaws.com
```

Observed output:

``` text
healthy: dynamodb.ap-south-1.amazonaws.com
```

------------------------------------------------------------------------

## 4. Apply Default Deny Egress Policy

``` bash
kubectl apply -f kubernetes/network-policy.yaml
```

Verify:

``` bash
kubectl get networkpolicy -n egress-lab
kubectl describe networkpolicy deny-egress -n egress-lab
```

------------------------------------------------------------------------

## 5. Test Again

``` sh
curl -m 5 https://dynamodb.ap-south-1.amazonaws.com
```

Observed result:

``` text
healthy: dynamodb.ap-south-1.amazonaws.com
```

Traffic was still allowed.

------------------------------------------------------------------------

# 🔎 Investigation

## 1. Network Policy

The following policy was applied:

``` yaml
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress: []
```

Expected:

-   Block all outbound traffic.

Actual:

-   Traffic was still permitted.

------------------------------------------------------------------------

## 2. Security Groups

Result:

-   Outbound HTTPS traffic allowed.
-   No restrictive egress rules found.

Status: ✅ Healthy

------------------------------------------------------------------------

## 3. Route Tables

Result:

-   Valid routes available.
-   Outbound connectivity present.

Status: ✅ Healthy

------------------------------------------------------------------------

## 4. VPC Endpoints

Result:

-   No DynamoDB VPC Endpoint configured.
-   Application successfully reached the public DynamoDB endpoint.

Status: ✅ Not the cause of the issue.

------------------------------------------------------------------------

## 5. Network Policy Enforcement

Checked installed DaemonSets:

``` bash
kubectl get daemonset -A
```

Observed:

``` text
aws-node
kube-proxy
```

No NetworkPolicy enforcement component (such as Calico, Cilium, or
Amazon VPC CNI Network Policy support) was present.

------------------------------------------------------------------------

# 📌 Root Cause Analysis

The Kubernetes NetworkPolicy object was created successfully but was
**not enforced**.

A default Amazon EKS cluster does not enforce NetworkPolicies unless a
supported implementation is installed or enabled.

Because NetworkPolicy enforcement was unavailable, the application
continued to access Amazon DynamoDB successfully.

------------------------------------------------------------------------

# ✅ Resolution

To enforce egress restrictions in Amazon EKS:

-   Enable Amazon VPC CNI Network Policy support, or
-   Install a supported NetworkPolicy implementation such as Calico or
    Cilium.

Once enabled, the same default deny egress policy would block outbound
traffic as expected.

------------------------------------------------------------------------

# 📷 Suggested Screenshots

-   EKS Cluster
-   Test Pod Running
-   NetworkPolicy
-   curl Output
-   DaemonSets
-   AWS Security Groups
-   Route Tables

------------------------------------------------------------------------

# 📚 Key Learnings

-   Amazon EKS networking
-   Kubernetes NetworkPolicy
-   Egress traffic investigation
-   Security Groups
-   Route Tables
-   VPC Endpoints
-   NetworkPolicy enforcement in EKS

------------------------------------------------------------------------

# 🧹 Cleanup

``` bash
kubectl delete namespace egress-lab
```

Delete the cluster if no longer required:

``` bash
eksctl delete cluster \
  --name production-alb \
  --region ap-south-1
```

------------------------------------------------------------------------

# 👨‍💻 Author

**Dharani Kumar N K**

B.E. Electronics and Communication Engineering

Cloud \| DevOps \| AWS \| Kubernetes
