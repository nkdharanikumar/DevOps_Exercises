# 📜 commands.md

# Kubernetes Incident Response Lab – CrashLoopBackOff Investigation

This document contains all the commands used throughout the project, along with their purpose.

---

# 1. Create Project Directory

```bash
mkdir crashloopbackoff-investigation

cd crashloopbackoff-investigation

mkdir app

mkdir k8s
```

Purpose:

* Creates the project structure.

---

# 2. Start Minikube

```bash
minikube start
```

Purpose:

* Starts the local Kubernetes cluster.

---

# 3. Verify Minikube

```bash
minikube status
```

Purpose:

* Confirms that Minikube is running properly.

---

# 4. Configure Docker to Use Minikube

```bash
eval $(minikube docker-env)
```

Purpose:

* Ensures Docker builds images inside Minikube so Kubernetes can access them without pushing to Docker Hub.

---

# 5. Build Docker Image

```bash
cd app

docker build -t payment-service:v1 .
```

Purpose:

* Builds the Flask application image.

---

# 6. Verify Docker Image

```bash
docker image ls
```

Purpose:

* Checks whether the Docker image was successfully created.

---

# 7. Deploy Kubernetes Resources

```bash
kubectl apply -f k8s/
```

Purpose:

* Creates all Kubernetes resources defined in the manifest files.

---

# 8. View Pods

```bash
kubectl get pods
```

Purpose:

* Displays the status of all running pods.

---

# 9. View Deployments

```bash
kubectl get deployment
```

Purpose:

* Displays deployment status and replica counts.

---

# 10. View Services

```bash
kubectl get svc
```

Purpose:

* Lists Kubernetes Services.

---

# 11. View Endpoints

```bash
kubectl get endpoints
```

Purpose:

* Shows backend Pods attached to each Service.

---

# 12. Scale PostgreSQL Down

```bash
kubectl scale deployment postgres --replicas=0
```

Purpose:

* Simulates a database outage by removing all PostgreSQL Pods.

---

# 13. Restart Payment Service

```bash
kubectl rollout restart deployment payment-service
```

Purpose:

* Forces the application to restart so it attempts to reconnect to PostgreSQL.

---

# 14. Watch Pods

```bash
kubectl get pods -w
```

Purpose:

* Continuously watches pod status changes.

---

# 15. Read Application Logs

```bash
kubectl logs <pod-name>
```

Example:

```bash
kubectl logs payment-service-79b85dc7c4-6mzcq
```

Purpose:

* Displays container logs to identify application errors.

---

# 16. Read Previous Container Logs

```bash
kubectl logs --previous <pod-name>
```

Purpose:

* Shows logs from the previous crashed container instance.

---

# 17. Describe Pod

```bash
kubectl describe pod <pod-name>
```

Example:

```bash
kubectl describe pod payment-service-79b85dc7c4-6mzcq
```

Purpose:

* Displays detailed pod information including:

  * Events
  * Restart Count
  * Exit Code
  * Environment Variables
  * Container State

---

# 18. Describe Deployment

```bash
kubectl describe deployment payment-service
```

Purpose:

* Displays deployment configuration and rollout history.

---

# 19. Scale PostgreSQL Back Up

```bash
kubectl scale deployment postgres --replicas=1
```

Purpose:

* Restores the PostgreSQL database.

---

# 20. Restart Payment Service After Recovery

```bash
kubectl rollout restart deployment payment-service
```

Purpose:

* Restarts the application after PostgreSQL becomes available.

---

# 21. Verify Recovery

```bash
kubectl get pods
```

Expected Output:

```text
payment-service    Running

postgres           Running
```

Purpose:

* Confirms the application has recovered successfully.

---

# 22. Delete All Resources

```bash
kubectl delete -f k8s/
```

Purpose:

* Deletes all Kubernetes resources created for this project.

---

# 23. Stop Minikube

```bash
minikube stop
```

Purpose:

* Stops the local Kubernetes cluster.

---

# 24. Delete Minikube Cluster

```bash
minikube delete
```

Purpose:

* Completely removes the Minikube cluster and frees local resources.

---

# Debugging Commands Reference

## View Pods

```bash
kubectl get pods
```

---

## View Deployments

```bash
kubectl get deployment
```

---

## View Services

```bash
kubectl get svc
```

---

## View Endpoints

```bash
kubectl get endpoints
```

---

## View Secrets

```bash
kubectl get secrets
```

---

## Describe Pod

```bash
kubectl describe pod <pod-name>
```

---

## Read Logs

```bash
kubectl logs <pod-name>
```

---

## Previous Logs

```bash
kubectl logs --previous <pod-name>
```

---

## Restart Deployment

```bash
kubectl rollout restart deployment <deployment-name>
```

---

## Scale Deployment

```bash
kubectl scale deployment <deployment-name> --replicas=<number>
```

---

# Cleanup Commands

```bash
kubectl delete -f k8s/

minikube stop

minikube delete
```

These commands remove all project resources and clean up the local Kubernetes environment.
