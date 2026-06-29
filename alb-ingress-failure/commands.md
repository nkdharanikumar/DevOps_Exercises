# Exercise 07 - Commands Used

This document contains all the commands used while completing **Exercise 07 - AWS ALB Ingress Failure**.

---

# 1. Verify Platform

Check all Helm releases.

```bash
helm list -A
```

Verify AWS Load Balancer Controller.

```bash
kubectl get deployment -A | grep aws-load-balancer
```

Verify controller Pods.

```bash
kubectl get pods -n kube-system | grep aws-load-balancer-controller
```

---

# 2. Verify OIDC Provider

Check the cluster OIDC issuer.

```bash
aws eks describe-cluster \
  --name devops-lab \
  --query "cluster.identity.oidc.issuer" \
  --output text
```

Associate IAM OIDC Provider (if required).

```bash
eksctl utils associate-iam-oidc-provider \
  --region ap-south-1 \
  --cluster devops-lab \
  --approve
```

---

# 3. Create IAM Policy

Download the AWS Load Balancer Controller IAM policy.

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
```

Create IAM Policy.

```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

If the policy already exists.

```bash
aws iam list-policies \
  --scope Local \
  --query "Policies[?PolicyName=='AWSLoadBalancerControllerIAMPolicy'].Arn" \
  --output text
```

---

# 4. Create IRSA Service Account

Create IAM Service Account.

```bash
eksctl create iamserviceaccount \
  --cluster devops-lab \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```

Verify Service Account.

```bash
kubectl get sa aws-load-balancer-controller -n kube-system
```

Describe Service Account.

```bash
kubectl describe sa aws-load-balancer-controller -n kube-system
```

---

# 5. Install AWS Load Balancer Controller

Add Helm repository.

```bash
helm repo add eks https://aws.github.io/eks-charts
```

Update repositories.

```bash
helm repo update
```

Retrieve VPC ID.

```bash
aws eks describe-cluster \
  --name devops-lab \
  --query "cluster.resourcesVpcConfig.vpcId" \
  --output text
```

Install controller.

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName=devops-lab \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=ap-south-1 \
  --set vpcId=<VPC_ID>
```

Verify installation.

```bash
helm list -A
```

```bash
kubectl get pods -n kube-system | grep aws-load-balancer-controller
```

---

# 6. Create Namespace

```bash
kubectl create namespace exercise-07
```

Verify namespace.

```bash
kubectl get ns
```

---

# 7. Deploy Application

Deploy NGINX.

```bash
kubectl apply -f deployment.yaml
```

Verify Deployment.

```bash
kubectl get deployment -n exercise-07
```

Verify ReplicaSet.

```bash
kubectl get rs -n exercise-07
```

Verify Pods.

```bash
kubectl get pods -n exercise-07
```

---

# 8. Create ClusterIP Service

Deploy Service.

```bash
kubectl apply -f service.yaml
```

Verify Service.

```bash
kubectl get svc -n exercise-07
```

Test Service locally.

```bash
kubectl port-forward svc/web-service 8080:80 -n exercise-07
```

Access:

```text
http://localhost:8080
```

---

# 9. Create Ingress

Deploy Ingress.

```bash
kubectl apply -f ingress.yaml
```

Watch ALB provisioning.

```bash
kubectl get ingress -n exercise-07 -w
```

Describe Ingress.

```bash
kubectl describe ingress web-ingress -n exercise-07
```

---

# 10. Verify AWS ALB

Check ALB state.

```bash
aws elbv2 describe-load-balancers \
  --query "LoadBalancers[].{Name:LoadBalancerName,DNS:DNSName,State:State.Code}" \
  --output table
```

Verify browser access.

```text
http://<ALB-DNS-NAME>
```

Expected:

```text
Welcome to nginx!
```

---

# 11. Simulate Production Failure

Modify Ingress backend.

Broken configuration.

```yaml
service:
  name: web-service-broken
```

Apply changes.

```bash
kubectl apply -f ingress.yaml
```

Inspect Ingress.

```bash
kubectl describe ingress web-ingress -n exercise-07
```

Expected:

```text
services "web-service-broken" not found
```

---

# 12. Investigate Failure

Describe Ingress.

```bash
kubectl describe ingress web-ingress -n exercise-07
```

View AWS Load Balancer Controller logs.

```bash
kubectl logs deployment/aws-load-balancer-controller \
-n kube-system --tail=100
```

Verify ALB state.

```bash
aws elbv2 describe-load-balancers \
  --query "LoadBalancers[].{Name:LoadBalancerName,DNS:DNSName,State:State.Code}" \
  --output table
```

---

# 13. Restore Application

Restore the correct backend.

```yaml
service:
  name: web-service
```

Apply configuration.

```bash
kubectl apply -f ingress.yaml
```

Verify Ingress.

```bash
kubectl describe ingress web-ingress -n exercise-07
```

Refresh browser.

Expected:

```text
Welcome to nginx!
```

---

# 14. Cleanup

Delete the exercise namespace.

```bash
kubectl delete namespace exercise-07
```

Verify namespace removal.

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
kubectl get ingress -n exercise-07

kubectl describe ingress web-ingress -n exercise-07

kubectl get svc -n exercise-07

kubectl get pods -n exercise-07

kubectl logs deployment/aws-load-balancer-controller -n kube-system --tail=100

aws elbv2 describe-load-balancers \
--query "LoadBalancers[].{Name:LoadBalancerName,DNS:DNSName,State:State.Code}" \
--output table

kubectl port-forward svc/web-service 8080:80 -n exercise-07
```

These commands provide a complete workflow for deploying, exposing, troubleshooting, and restoring an internet-facing application on Amazon EKS using the AWS Load Balancer Controller and Application Load Balancer (ALB).
