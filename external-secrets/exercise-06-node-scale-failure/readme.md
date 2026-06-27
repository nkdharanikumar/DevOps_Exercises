# Exercise 06 – Node Scale Failure

## Overview

This exercise demonstrates one of the most common Kubernetes scheduling failures encountered in production environments.

A deployment was intentionally configured with CPU resource requests that exceeded the allocatable CPU available on every worker node in the Amazon EKS cluster. As a result, Kubernetes could not schedule the Pods, leaving them permanently in the **Pending** state.

The issue was investigated using Kubernetes scheduling events, the root cause was identified, and the deployment was corrected by adjusting the CPU resource requests.

---

# Objective

* Understand Kubernetes scheduling.
* Learn how resource requests affect Pod placement.
* Investigate Pods stuck in the Pending state.
* Analyze scheduler events.
* Identify insufficient cluster resources.
* Perform Root Cause Analysis (RCA).
* Resolve scheduling failures by correcting resource requests.

---

# Technologies Used

* Amazon EKS
* Kubernetes
* kubectl
* AWS
* NGINX Container

---

# Architecture

```text
             Deployment
                  │
                  ▼
             ReplicaSet
                  │
                  ▼
                 Pods
                  │
                  ▼
         Kubernetes Scheduler
                  │
                  ▼
             Worker Nodes
```

---

# Environment

* Kubernetes Cluster : Amazon EKS
* Worker Nodes : 2
* Instance Type : t3.medium
* Kubernetes Version : v1.34.x

Each worker node contained approximately:

```text
Allocatable CPU    : 1930m
Allocatable Memory : 3.2 GiB
```

---

# Initial Deployment

The application was deployed with the following CPU request:

```yaml
resources:
  requests:
    cpu: "2500m"
    memory: "512Mi"

  limits:
    cpu: "2500m"
    memory: "512Mi"
```

Two replicas were created.

---

# Production Incident

Both Pods remained in the **Pending** state.

Deployment Status:

```text
Pending
Pending
```

No containers were started.

---

# Investigation

The first troubleshooting step was to inspect one of the Pods.

```bash
kubectl describe pod <pod-name> -n exercise-06
```

The scheduler events reported:

```text
Warning  FailedScheduling

0/2 nodes are available:

2 Insufficient cpu
```

Additional scheduler message:

```text
Preemption is not helpful for scheduling
```

---

# Root Cause Analysis (RCA)

## Incident

Application Pods could not be scheduled onto any worker node.

---

## Investigation

### Step 1

Verified Pod status.

Result:

```text
Pending
```

---

### Step 2

Checked Pod conditions.

Observed:

```text
PodScheduled = False
```

The scheduler had not assigned the Pod to any node.

---

### Step 3

Reviewed resource requests.

Pod requested:

```text
CPU : 2500m
Memory : 512Mi
```

---

### Step 4

Inspected worker node capacity.

Each node provided:

```text
CPU : 1930m
```

---

### Step 5

Compared Pod requests with node capacity.

```text
Requested CPU : 2500m

Available CPU : 1930m
```

Since the requested CPU exceeded the allocatable CPU on every node, Kubernetes could not place the Pod.

---

# Root Cause

The Deployment requested **2500m CPU**, while every worker node had only **1930m allocatable CPU**.

Because no node could satisfy the CPU requirement, the Kubernetes Scheduler rejected scheduling and left the Pods in the **Pending** state.

---

# Resolution

The Deployment was updated.

Previous configuration:

```yaml
requests:
  cpu: "2500m"

limits:
  cpu: "2500m"
```

Updated configuration:

```yaml
requests:
  cpu: "500m"
  memory: "512Mi"

limits:
  cpu: "1000m"
  memory: "512Mi"
```

After applying the updated Deployment, the scheduler successfully placed the Pods onto the worker nodes.

Deployment Status:

```text
Running
Running
```

---

# Kubernetes Scheduling Workflow

```text
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pod
      │
      ▼
Scheduler
      │
      ▼
Check Available Resources
      │
      ├───────────────┐
      │               │
Enough CPU?        Insufficient CPU
      │               │
      ▼               ▼
 Running          Pending
```

---

# Understanding Resource Requests

Kubernetes schedules Pods using **resource requests**, not limits.

Example:

```yaml
resources:
  requests:
    cpu: "500m"

  limits:
    cpu: "1000m"
```

The scheduler guarantees the requested CPU before assigning a Pod to a node.

If no node can satisfy the request, scheduling fails.

---

# Understanding Preemption

During scheduling, Kubernetes also evaluated whether existing Pods could be evicted.

Scheduler output:

```text
Preemption is not helpful for scheduling
```

This means that even if lower-priority Pods were removed, the node still would not have enough CPU to satisfy a request of **2500m**.

---

# Production Best Practices

* Always define realistic resource requests.
* Monitor node utilization.
* Avoid overestimating CPU requirements.
* Use Horizontal Pod Autoscaler when appropriate.
* Scale worker nodes if applications require additional capacity.
* Monitor scheduler events for Pending Pods.

---

# Key Learnings

* Learned how Kubernetes schedules Pods.
* Understood allocatable CPU and memory.
* Investigated Pods stuck in the Pending state.
* Used `kubectl describe pod` to inspect scheduler events.
* Identified insufficient CPU resources.
* Performed Root Cause Analysis.
* Corrected Deployment resource requests.
* Successfully restored Pod scheduling.

---

# Interview Questions

## Why does a Pod remain in the Pending state?

A Pod remains Pending when Kubernetes cannot schedule it onto any available worker node due to insufficient resources, scheduling constraints, node selectors, taints, or affinity rules.

---

## How do you troubleshoot a Pending Pod?

1. Check Pod status.
2. Describe the Pod.
3. Review scheduler events.
4. Inspect node capacity.
5. Compare resource requests with allocatable resources.
6. Adjust requests or increase cluster capacity.

---

## What is the difference between resource requests and limits?

Resource requests determine scheduling decisions.

Resource limits define the maximum resources a running container can consume.

---

## What does "Insufficient cpu" mean?

It indicates that no worker node has enough allocatable CPU available to satisfy the Pod's requested CPU resources.

---

## Why was "Preemption is not helpful" displayed?

Even removing lower-priority Pods would not provide enough CPU because each node's allocatable CPU (1930m) was still lower than the Pod's requested CPU (2500m).

---

# Outcome

Successfully reproduced a real Kubernetes scheduling failure by requesting more CPU than the worker nodes could provide. Investigated scheduler events, identified insufficient CPU resources as the root cause, updated the Deployment with appropriate resource requests, and restored successful Pod scheduling.
