# Exercise 05 - Commands Used

This document contains all the commands used while completing **Exercise 05 - Helm Upgrade Failure (Immutable Selector)**.

---

# 1. Verify Kubernetes Cluster

Check the current Kubernetes context.

```bash
kubectl config current-context
```

List all worker nodes.

```bash
kubectl get nodes
```

Verify all system pods are healthy.

```bash
kubectl get pods -A
```

---

# 2. Create Namespace

Create a dedicated namespace for the exercise.

```bash
kubectl create namespace exercise-05
```

Verify the namespace.

```bash
kubectl get ns
```

---

# 3. Verify Helm Installation

Check the installed Helm version.

```bash
helm version
```

---

# 4. Create Helm Chart

Create a project directory.

```bash
mkdir helm
cd helm
```

Generate a Helm chart.

```bash
helm create payment-service
```

Verify the generated chart.

```bash
tree payment-service
```

---

# 5. Clean the Default Helm Chart

Remove unnecessary templates.

```bash
rm templates/hpa.yaml
rm templates/httproute.yaml
rm templates/ingress.yaml
rm templates/serviceaccount.yaml
rm -rf templates/tests
rm templates/NOTES.txt
```

Verify the remaining files.

```bash
tree
```

---

# 6. Preview Helm Templates

Render Kubernetes manifests without deploying.

```bash
helm template payment-service .
```

---

# 7. Install the Helm Chart

Deploy the application into Kubernetes.

```bash
helm install payment-service . \
  --namespace exercise-05
```

---

# 8. Verify Deployment

List installed Helm releases.

```bash
helm list -n exercise-05
```

View all Kubernetes resources.

```bash
kubectl get all -n exercise-05
```

View running Pods.

```bash
kubectl get pods -n exercise-05
```

---

# 9. Inspect the Deployment

Display the complete Deployment manifest stored in Kubernetes.

```bash
kubectl get deployment payment-service \
  -n exercise-05 \
  -o yaml
```

---

# 10. Simulate Production Change

Modify the application label inside:

```
values.yaml
```

From:

```yaml
labels:
  app: payment
```

To:

```yaml
labels:
  app: payment-v2
```

---

# 11. Preview Updated Templates

Render the updated manifests.

```bash
helm template payment-service .
```

---

# 12. Trigger the Immutable Selector Error

Attempt to upgrade the Helm release.

```bash
helm upgrade payment-service . \
  --namespace exercise-05
```

Expected Error:

```text
UPGRADE FAILED:
cannot patch "payment-service" with kind Deployment:
Deployment.apps "payment-service" is invalid:
spec.selector:
Invalid value:
field is immutable
```

---

# 13. Restore the Deployment

Revert the label in `values.yaml`.

```yaml
labels:
  app: payment
```

Upgrade the release again.

```bash
helm upgrade payment-service . \
  --namespace exercise-05
```

---

# Useful Troubleshooting Commands

View Deployments.

```bash
kubectl get deployments -n exercise-05
```

Describe Deployment.

```bash
kubectl describe deployment payment-service \
  -n exercise-05
```

View Services.

```bash
kubectl get svc -n exercise-05
```

View Pods.

```bash
kubectl get pods -n exercise-05
```

Describe a Pod.

```bash
kubectl describe pod <pod-name> \
  -n exercise-05
```

View Pod logs.

```bash
kubectl logs <pod-name> \
  -n exercise-05
```

Delete the Helm release.

```bash
helm uninstall payment-service \
  -n exercise-05
```

Delete the namespace.

```bash
kubectl delete namespace exercise-05
```
