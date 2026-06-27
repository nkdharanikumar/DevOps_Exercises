# Exercise 05 – Helm Upgrade Failure (Immutable Selector)

## Overview

This exercise demonstrates one of the most common Kubernetes deployment failures encountered in production environments: **attempting to modify an immutable Deployment selector during a Helm upgrade**.

A Helm chart was initially deployed successfully to an Amazon EKS cluster. During a later upgrade, the application's label was changed from `payment` to `payment-v2`. Since the Deployment selector also changed, Kubernetes rejected the update because `spec.selector` is an immutable field.

This lab reproduces the exact production scenario and explains the root cause, investigation process, and production-safe solutions.

---

# Objective

* Understand how Helm renders Kubernetes manifests.
* Deploy an application using Helm.
* Learn the relationship between Deployment selectors and Pod labels.
* Reproduce the immutable selector error.
* Perform Root Cause Analysis (RCA).
* Learn production best practices for Helm upgrades.

---

# Technologies Used

* Amazon EKS
* Kubernetes
* Helm
* kubectl
* NGINX

---

# Architecture

```text
                 Helm
                   │
                   ▼
            Deployment
                   │
      selector: app=payment
                   │
                   ▼
          ReplicaSet
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
     Pod 1               Pod 2
 app=payment         app=payment
                   ▲
                   │
              Service
```

---

# Initial Deployment

The Helm chart was configured with:

```yaml
labels:
  app: payment
```

Deployment selector:

```yaml
selector:
  matchLabels:
    app: payment
```

Pod labels:

```yaml
template:
  metadata:
    labels:
      app: payment
```

The selector and Pod labels matched correctly, allowing Kubernetes to manage the Pods successfully.

Deployment Status:

* 2 Running Pods
* ClusterIP Service
* Successful Helm installation

---

# Production Change

A developer decided to rename the application by changing:

```yaml
labels:
  app: payment
```

to

```yaml
labels:
  app: payment-v2
```

Since the Deployment template used this value in multiple places, Helm generated:

```yaml
selector:
  matchLabels:
    app: payment-v2
```

---

# Error Encountered

Running:

```bash
helm upgrade payment-service . --namespace exercise-05
```

produced:

```text
Error: UPGRADE FAILED:
cannot patch "payment-service" with kind Deployment:
Deployment.apps "payment-service" is invalid:
spec.selector:
Invalid value:
{"matchLabels":{"app":"payment-v2"}}
field is immutable
```

---

# Root Cause Analysis (RCA)

## What happened?

Helm rendered a new Deployment manifest using the updated label value.

The Deployment selector changed from:

```yaml
app: payment
```

to

```yaml
app: payment-v2
```

When Kubernetes compared the existing Deployment with the updated manifest, it detected that `spec.selector.matchLabels` had changed.

Since Deployment selectors are immutable, Kubernetes rejected the update.

---

# Why is the Selector Immutable?

The Deployment selector defines which Pods belong to the Deployment.

Example:

```text
Deployment
      │
      ▼
selector

app=payment

      │
      ▼

Pods

app=payment
```

If Kubernetes allowed the selector to change after creation:

* Existing Pods could become orphaned.
* The Deployment might accidentally adopt unrelated Pods.
* Application state could become inconsistent.
* Rolling updates would become unsafe.

To prevent these issues, Kubernetes marks `spec.selector` as immutable.

---

# Investigation Steps

The following commands were used during the investigation:

```bash
kubectl get deployment payment-service -n exercise-05 -o yaml

helm template payment-service .

helm upgrade payment-service . --namespace exercise-05
```

The Deployment YAML confirmed:

```yaml
selector:
  matchLabels:
    app: payment
```

The Helm template preview showed:

```yaml
selector:
  matchLabels:
    app: payment-v2
```

This confirmed that the selector modification caused the failure.

---

# Resolution

The immediate resolution was to restore the original label:

```yaml
labels:
  app: payment
```

and perform the Helm upgrade again.

Since the selector no longer changed, Kubernetes accepted the update.

---

# Production Best Practices

* Never modify `spec.selector.matchLabels` after Deployment creation.
* Keep Deployment selectors stable throughout the application's lifecycle.
* Use `helm template` before every production deployment to preview generated manifests.
* Use `helm lint` to validate charts before deployment.
* Modify images, replicas, environment variables, resources, or ConfigMaps instead of changing selectors.
* If a selector change is absolutely required, create a new Deployment instead of modifying the existing one.

---

# Key Learnings

* Understood Helm chart structure.
* Learned how Helm renders templates.
* Deployed a Helm application to Amazon EKS.
* Investigated Kubernetes Deployment resources.
* Learned the relationship between selectors and labels.
* Reproduced a real production incident.
* Performed Root Cause Analysis.
* Understood immutable Kubernetes fields.
* Learned production-safe deployment practices.

---

# Interview Questions

### Why did Helm upgrade fail?

Helm successfully rendered the updated Deployment manifest and sent it to the Kubernetes API. Kubernetes rejected the update because `spec.selector.matchLabels` is an immutable field in a Deployment.

---

### Why is `spec.selector` immutable?

Deployment selectors determine which Pods belong to a Deployment. Changing them after creation could orphan existing Pods or cause the Deployment to adopt unintended Pods, leading to inconsistent application state. Kubernetes prevents this by making the selector immutable.

---

### What is the difference between `helm template` and `helm install`?

| helm template                        | helm install                         |
| ------------------------------------ | ------------------------------------ |
| Renders Kubernetes manifests locally | Deploys resources to Kubernetes      |
| Does not contact the cluster         | Creates resources inside the cluster |
| Used for validation and debugging    | Used for actual deployment           |

---

# Outcome

Successfully reproduced the Helm Upgrade Failure scenario, identified the root cause, explained why Kubernetes rejected the update, and documented the production-safe approach for handling immutable Deployment selectors.
