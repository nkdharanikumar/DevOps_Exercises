# Exercise 06 - Commands Used

This document contains all the commands used while completing **Exercise 06 - Node Scale Failure**.

---

# 1. Verify Cluster

Check worker nodes.

```bash
kubectl get nodes
```

Display node labels.

```bash
kubectl get nodes --show-labels
```

View node resource allocation.

```bash
kubectl describe nodes
```

View allocatable resources for a specific node.

```bash
kubectl describe node ip-192-168-20-99.ap-south-1.compute.internal | grep -A5 "Allocatable"
```

Display current CPU and memory usage.

```bash
kubectl top nodes
```

---

# 2. Create Exercise Namespace

Create a namespace for the lab.

```bash
kubectl create namespace exercise-06
```

Verify namespace.

```bash
kubectl get ns
```

---

# 3. Deploy Application

Deploy the application.

```bash
kubectl apply -f deployment.yaml
```

Verify deployment.

```bash
kubectl get deployment -n exercise-06
```

View ReplicaSet.

```bash
kubectl get rs -n exercise-06
```

View Pods.

```bash
kubectl get pods -n exercise-06
```

---

# 4. Observe Scheduling Failure

Check Pod status.

```bash
kubectl get pods -n exercise-06
```

Describe a Pending Pod.

```bash
kubectl describe pod <pod-name> -n exercise-06
```

Example:

```bash
kubectl describe pod cpu-stress-68644cbdd4-pnhsq -n exercise-06
```

Expected scheduler event:

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

# 5. Verify Cluster Capacity

Display allocatable CPU and memory.

```bash
kubectl describe nodes
```

Display live resource usage.

```bash
kubectl top nodes
```

Compare:

* Pod CPU Request
* Node Allocatable CPU

---

# 6. Fix the Deployment

Modify the Deployment resource requests.

Previous configuration:

```yaml
resources:
  requests:
    cpu: "2500m"
    memory: "512Mi"

  limits:
    cpu: "2500m"
    memory: "512Mi"
```

Updated configuration:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"

  limits:
    cpu: "1000m"
    memory: "512Mi"
```

Apply the updated Deployment.

```bash
kubectl apply -f deployment.yaml
```

---

# 7. Verify Recovery

Watch Pods.

```bash
kubectl get pods -n exercise-06 -w
```

Verify Pods.

```bash
kubectl get pods -n exercise-06
```

Expected:

```text
Running
Running
```

Verify Deployment.

```bash
kubectl get deployment -n exercise-06
```

---

# 8. Useful Troubleshooting Commands

View all Pods.

```bash
kubectl get pods -A
```

Describe Deployment.

```bash
kubectl describe deployment cpu-stress -n exercise-06
```

Describe ReplicaSet.

```bash
kubectl describe rs -n exercise-06
```

Describe Pod.

```bash
kubectl describe pod <pod-name> -n exercise-06
```

Display node utilization.

```bash
kubectl top nodes
```

Display node information.

```bash
kubectl describe nodes
```

View Kubernetes events.

```bash
kubectl get events -n exercise-06 --sort-by=.metadata.creationTimestamp
```

---

# 9. Cleanup

Delete the exercise namespace.

```bash
kubectl delete namespace exercise-06
```

Verify cleanup.

```bash
kubectl get ns
```

Verify remaining Pods.

```bash
kubectl get pods -A
```

Expected remaining namespaces:

* kube-system
* argocd
* external-secrets

---

# Key Troubleshooting Commands

```bash
kubectl get pods -n exercise-06

kubectl describe pod <pod-name> -n exercise-06

kubectl describe nodes

kubectl top nodes

kubectl get events -n exercise-06 --sort-by=.metadata.creationTimestamp

kubectl get deployment -n exercise-06

kubectl get rs -n exercise-06
```

These commands are the primary tools for diagnosing Kubernetes scheduling failures and investigating Pods stuck in the **Pending** state.
