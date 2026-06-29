# Kubernetes Node DiskPressure Incident Response Lab

## Overview

This project simulates a **real-world Kubernetes Node DiskPressure incident** and demonstrates how a DevOps Engineer or Site Reliability Engineer (SRE) investigates, diagnoses, and recovers a Kubernetes node affected by excessive disk usage caused by container logs.

Unlike application-level failures where only a single Pod crashes, this exercise focuses on **node-level failures**, where the Kubernetes worker node itself becomes unhealthy due to disk exhaustion.

The objective is to understand how Kubernetes stores container logs, how DiskPressure affects node health, how to investigate storage-related incidents, and how to safely recover the cluster.

> **Note**
>
> This lab was performed on **Minikube**. Since the Minikube node had approximately **40 GB of available free disk space**, completely filling the node to trigger an actual `DiskPressure=True` state would require generating tens of gigabytes of logs over an extended period.
>
> Therefore, this project focuses on the **complete investigation, diagnosis, recovery, and prevention workflow**, which is identical to the process followed in production Kubernetes environments.

---

# Problem Statement

A Kubernetes node suddenly becomes **NotReady**, preventing new workloads from being scheduled.

Developers report that deployments are stuck in a Pending state.

Upon investigation, the node reports:

* DiskPressure=True
* Node NotReady
* "No space left on device"

The suspected root cause is uncontrolled container log growth.

Your responsibility as the on-call DevOps Engineer is to:

* Investigate the issue
* Identify the root cause
* Recover the node safely
* Prevent future occurrences

---

# Objectives

This project demonstrates how to:

* Understand Kubernetes node health conditions
* Learn what DiskPressure means
* Investigate disk utilization using Linux commands
* Understand Kubernetes container log storage
* Trace log storage from application to filesystem
* Recover a node suffering from excessive log usage
* Apply production best practices to avoid similar incidents

---

# Technologies Used

* Kubernetes
* Minikube
* Docker Runtime
* Linux
* BusyBox
* kubectl

---

# Project Architecture

```
Application
      │
      ▼
stdout / stderr
      │
      ▼
Docker JSON Log Driver
      │
      ▼
/var/lib/docker/containers/
      │
      ▼
/var/log/pods/
      │
      ▼
/var/log/containers/
      │
      ▼
kubectl logs
```

---

# Why Does This Incident Happen?

Every container writes application logs to **stdout** and **stderr**.

The container runtime captures these logs and stores them on the Kubernetes node.

If an application continuously writes logs without rotation, these log files continue growing.

Eventually:

* Disk space becomes exhausted
* kubelet cannot write node state
* Container runtime cannot create new containers
* Kubernetes detects DiskPressure
* Node becomes NotReady

This is one of the most common infrastructure incidents in production Kubernetes clusters.

---

# Lab Workflow

## Step 1 – Create a Log-Generating Application

A BusyBox deployment was created that continuously writes logs to stdout.

Purpose:

* Simulate a noisy production application
* Generate continuous log files
* Understand Kubernetes logging behavior

---

## Step 2 – Verify Cluster Health

Before beginning the investigation, the cluster was confirmed to be healthy.

Commands used:

* Verify node status
* Verify system Pods
* Confirm application deployment

Purpose:

Ensure the environment is healthy before reproducing the incident.

---

## Step 3 – Investigate Disk Usage

The following Linux commands were used:

* `df -h`
* `du -sh`

Purpose:

* Check filesystem usage
* Identify which directories consume storage
* Locate excessive log usage

---

## Step 4 – Explore Kubernetes Log Storage

This exercise explored the relationship between:

```
/var/log/containers/

/var/log/pods/

/var/lib/docker/containers/
```

Understanding this relationship explains how:

```
kubectl logs
```

retrieves container logs.

---

## Step 5 – Identify Root Cause

The simulated application continuously generated logs.

These logs were traced through:

```
stdout

↓

Docker JSON Log

↓

/var/lib/docker/containers/

↓

/var/log/pods/

↓

/var/log/containers/
```

This demonstrates how excessive application logging can eventually consume node storage.

---

## Step 6 – Production Investigation Workflow

A typical production investigation follows:

1. Confirm node health.
2. Verify DiskPressure condition.
3. Check filesystem usage.
4. Identify largest directories.
5. Locate offending container logs.
6. Stop excessive log generation.
7. Recover disk space.
8. Verify node health.

This structured workflow prevents unnecessary data loss and minimizes downtime.

---

# Expected Production Symptoms

When DiskPressure occurs, Kubernetes may exhibit:

* Node NotReady
* Pods stuck in Pending
* Failed scheduling
* "No space left on device"
* DiskPressure=True
* kubelet failures
* Container runtime failures

---

# Recovery Procedure

The recovery process consists of:

1. Confirm the issue using `kubectl describe node`
2. Check disk utilization using `df`
3. Locate excessive log files using `du`
4. Stop the workload generating excessive logs
5. Remove or rotate oversized logs
6. Verify recovered disk space
7. Wait for kubelet to restore node health
8. Restart the application

This ensures recovery without immediately recreating the problem.

---

# Prevention Best Practices

Production Kubernetes clusters should implement:

## Log Rotation

Prevent unlimited log growth by configuring Docker or containerd log rotation.

---

## Centralized Logging

Forward logs to systems such as:

* Grafana Loki
* Elasticsearch
* CloudWatch
* Splunk

Avoid relying solely on local node storage.

---

## Reduce Log Verbosity

Avoid logging:

* Entire API payloads
* Large JSON responses
* Debug logs in production
* Sensitive information

---

## Monitor Disk Usage

Configure Prometheus alerts for:

* 80% Disk Usage (Warning)
* 90% Disk Usage (Critical)
* 95% Disk Usage (Immediate Action)

This enables proactive incident response.

---

# Key Learning Outcomes

After completing this project, you should understand:

* Kubernetes node health conditions
* DiskPressure
* Node NotReady
* Container log storage
* Linux storage investigation
* Production incident response
* Root cause analysis
* Safe recovery procedures
* Preventive operational practices

---

# Project Structure

```
.
├── README.md
├── commands.md
└── spam-logger.yaml
```

---

# Cleanup

Delete the workload:

```bash
kubectl delete deployment spam-logger
```

Delete the Minikube cluster:

```bash
minikube delete
```

This removes:

* Pods
* Deployments
* Container logs
* Docker/containerd data inside Minikube
* Cluster state

---

# Conclusion

This project demonstrates a realistic Kubernetes node-level incident where uncontrolled container log growth can eventually lead to DiskPressure and node instability.

Although the complete DiskPressure state was not physically reproduced due to the large amount of free storage available on the Minikube node, every stage of the production investigation, diagnosis, recovery, and prevention workflow was successfully demonstrated.

Understanding this workflow is an essential skill for Kubernetes administrators, DevOps Engineers, and Site Reliability Engineers responsible for maintaining healthy production clusters.
