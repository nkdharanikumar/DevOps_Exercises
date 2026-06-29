# commands.md

# Exercise 13 – Secret Rotation Outage

This file contains all the commands used during the project from setup to cleanup.

---

# 1. Start Minikube

```bash
minikube start
```

Verify cluster

```bash
kubectl get nodes
```

---

# 2. Create Project

```bash
mkdir exercise-13-secret-rotation-outage

cd exercise-13-secret-rotation-outage
```

---

# 3. Create Application

```bash
mkdir app

cd app

touch app.py requirements.txt Dockerfile
```

---

# 4. Build Docker Image

Switch Docker daemon to Minikube

```bash
eval $(minikube docker-env)
```

Build image

```bash
docker build -t payment-service:v1 .
```

Verify image

```bash
docker images
```

---

# 5. Create Kubernetes Manifests

```bash
cd ..

mkdir k8s

cd k8s

touch deployment.yaml

touch service.yaml

touch secret.yaml
```

---

# 6. Deploy Application

Create Secret

```bash
kubectl apply -f secret.yaml
```

Create Deployment

```bash
kubectl apply -f deployment.yaml
```

Create Service

```bash
kubectl apply -f service.yaml
```

---

# 7. Verify Resources

Pods

```bash
kubectl get pods
```

Deployments

```bash
kubectl get deployment
```

Services

```bash
kubectl get svc
```

Secrets

```bash
kubectl get secret
```

---

# 8. Port Forward

```bash
kubectl port-forward svc/payment-service 8082:80
```

---

# 9. Test Application

Home Page

```bash
curl http://localhost:8082/
```

Wrong Token

```bash
curl -H "Authorization: wrongtoken" http://localhost:8082/payment
```

Correct Token

```bash
curl -H "Authorization: payment123" http://localhost:8082/payment
```

---

# 10. Verify Secret

View Secret

```bash
kubectl get secret payment-secret -o yaml
```

Decode Secret

```bash
kubectl get secret payment-secret -o jsonpath="{.data.API_TOKEN}" | base64 -d
```

---

# 11. Rotate Secret

Generate Base64

```bash
echo -n "payment456" | base64
```

Edit Kubernetes Secret

```bash
kubectl edit secret payment-secret
```

OR

Modify secret.yaml

```yaml
stringData:
  API_TOKEN: payment456
```

Apply changes

```bash
kubectl apply -f secret.yaml
```

Verify Secret

```bash
kubectl get secret payment-secret -o jsonpath="{.data.API_TOKEN}" | base64 -d
```

---

# 12. Simulate Incident

New Token

```bash
curl -H "Authorization: payment456" http://localhost:8082/payment
```

Old Token

```bash
curl -H "Authorization: payment123" http://localhost:8082/payment
```

Expected Result

* New token → Unauthorized
* Old token → Payment Successful

---

# 13. Investigate Incident

Application Logs

```bash
kubectl logs -l app=payment-service
```

Check Secret

```bash
kubectl get secret payment-secret -o jsonpath="{.data.API_TOKEN}" | base64 -d
```

Check Pods

```bash
kubectl get pods
```

Describe Deployment

```bash
kubectl describe deployment payment-service
```

Check Environment Variable Inside Pod

```bash
kubectl exec -it <pod-name> -- printenv | grep API_TOKEN
```

Example

```bash
kubectl exec -it payment-service-6478c7db78-bhrlx -- printenv | grep API_TOKEN
```

---

# 14. Recover Service

Restart Deployment

```bash
kubectl rollout restart deployment payment-service
```

Monitor Rollout

```bash
kubectl rollout status deployment payment-service
```

Restart Port Forward

```bash
kubectl port-forward svc/payment-service 8082:80
```

Verify

```bash
curl -H "Authorization: payment456" http://localhost:8082/payment
```

```bash
curl -H "Authorization: payment123" http://localhost:8082/payment
```

Expected Result

* payment456 → Payment Successful
* payment123 → Unauthorized

---

# 15. Useful Debugging Commands

List All Resources

```bash
kubectl get all
```

Describe Pod

```bash
kubectl describe pod <pod-name>
```

Pod Logs

```bash
kubectl logs <pod-name>
```

Execute Shell

```bash
kubectl exec -it <pod-name> -- sh
```

Environment Variables

```bash
printenv
```

View Secret

```bash
kubectl get secret payment-secret -o yaml
```

Decode Secret

```bash
kubectl get secret payment-secret -o jsonpath="{.data.API_TOKEN}" | base64 -d
```

---

# 16. Cleanup

Delete Deployment

```bash
kubectl delete deployment payment-service
```

Delete Service

```bash
kubectl delete service payment-service
```

Delete Secret

```bash
kubectl delete secret payment-secret
```

Delete All Resources

```bash
kubectl delete all --all
```

Stop Minikube

```bash
minikube stop
```

Delete Minikube Cluster

```bash
minikube delete
```
