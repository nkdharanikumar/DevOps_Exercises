# Commands Used - Kubernetes Node DiskPressure Incident Response Lab

This document contains all the commands used during the project.

---

# Start Minikube

```bash
minikube start
```

---

# Verify Cluster

```bash
kubectl get nodes
```

```bash
kubectl get pods -A
```

```bash
kubectl get pods
```

---

# Deploy the Log Generator

```bash
kubectl apply -f spam-logger.yaml
```

Verify deployment:

```bash
kubectl get pods
```

View application logs:

```bash
kubectl logs -f <pod-name>
```

---

# Access the Minikube Node

```bash
minikube ssh
```

---

# Check Filesystem Usage

```bash
df -h
```

---

# View Kubernetes Container Log Links

```bash
sudo ls -lh /var/log/containers/
```

---

# Check Log Directory Size

```bash
sudo du -sh /var/log/containers/*
```

---

# Locate Pod Log Directory

```bash
sudo find /var/log/pods | grep spam
```

---

# Inspect Actual Pod Log

```bash
sudo ls -lh /var/log/pods/default_spam-logger-*/logger/0.log
```

---

# Check Pod Log Directory Size

```bash
sudo du -sh /var/log/pods/default_spam-logger-*
```

---

# Observe Disk Usage (Optional)

```bash
watch -n 2 df -h
```

---

# Simulated Production Investigation Commands

Describe node:

```bash
kubectl describe node minikube
```

Check filesystem usage:

```bash
df -h
```

Find large directories:

```bash
sudo du -sh /var/*
```

Investigate log directory:

```bash
sudo du -sh /var/log/*
```

Find large container logs:

```bash
sudo du -sh /var/log/containers/*
```

---

# Simulated Recovery Commands

Stop the application:

```bash
kubectl scale deployment spam-logger --replicas=0
```

Verify pods:

```bash
kubectl get pods
```

Check disk space:

```bash
df -h
```

Verify node health:

```bash
kubectl get nodes
```

```bash
kubectl describe node minikube
```

Restart the application:

```bash
kubectl scale deployment spam-logger --replicas=1
```

---

# Cleanup

Delete the deployment:

```bash
kubectl delete deployment spam-logger
```

Exit Minikube:

```bash
exit
```

Delete the Minikube cluster:

```bash
minikube delete
```

---

# Optional Docker Cleanup

Remove unused Docker resources:

```bash
docker system prune -a
```

> **Warning:** This removes all unused Docker images and stopped containers on the host machine.

---

# Verification

Check cluster status:

```bash
kubectl get nodes
```

Check all resources:

```bash
kubectl get all
```

Expected output:

```text
No resources found in default namespace.
```
