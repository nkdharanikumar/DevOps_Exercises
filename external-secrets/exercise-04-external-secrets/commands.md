# Exercise 04 - Commands Used

This document contains all the commands used while completing **Exercise 04 - External Secrets Failure**.

---

# 1. Verify AWS Configuration

Verify AWS credentials.

```bash
aws sts get-caller-identity
```

Check AWS CLI configuration.

```bash
aws configure list
```

List available secrets.

```bash
aws secretsmanager list-secrets --max-results 10
```

Retrieve the secret value.

```bash
aws secretsmanager get-secret-value \
  --secret-id app-secret
```

---

# 2. Verify Kubernetes Environment

Check worker nodes.

```bash
kubectl get nodes
```

Check all namespaces.

```bash
kubectl get ns
```

Verify existing Helm releases.

```bash
helm list -A
```

Check for existing External Secrets CRDs.

```bash
kubectl get crd | grep external-secrets
```

---

# 3. Install External Secrets Operator

Add the Helm repository.

```bash
helm repo add external-secrets https://charts.external-secrets.io
```

Update Helm repositories.

```bash
helm repo update
```

View available chart versions.

```bash
helm search repo external-secrets/external-secrets --versions | head -10
```

Install External Secrets Operator.

```bash
helm install external-secrets external-secrets/external-secrets \
  --version 2.7.0 \
  --namespace external-secrets \
  --create-namespace
```

Verify installation.

```bash
helm list -A
```

Verify pods.

```bash
kubectl get pods -n external-secrets
```

Verify CRDs.

```bash
kubectl get crd | grep external-secrets
```

---

# 4. Create AWS Credential Secret

Display AWS credentials.

```bash
cat ~/.aws/credentials
```

Create Kubernetes Secret containing AWS credentials.

```bash
kubectl create secret generic awssm-secret \
  --from-literal=access-key=<AWS_ACCESS_KEY_ID> \
  --from-literal=secret-access-key=<AWS_SECRET_ACCESS_KEY>
```

Verify Secret.

```bash
kubectl get secret
```

Describe Secret.

```bash
kubectl describe secret awssm-secret
```

---

# 5. Create SecretStore

Apply SecretStore configuration.

```bash
kubectl apply -f secretstore.yaml
```

Verify SecretStore.

```bash
kubectl get secretstore
```

Describe SecretStore.

```bash
kubectl describe secretstore aws-secret-store
```

Expected:

```text
Ready=True
```

---

# 6. Create ExternalSecret

Apply ExternalSecret.

```bash
kubectl apply -f externalsecret.yaml
```

Verify ExternalSecret.

```bash
kubectl get externalsecret
```

Describe ExternalSecret.

```bash
kubectl describe externalsecret app-secret
```

Expected:

```text
Ready=True

Reason=SecretSynced
```

---

# 7. Verify Kubernetes Secret

Verify Secret creation.

```bash
kubectl get secret
```

Describe Secret.

```bash
kubectl describe secret app-secret
```

Expected keys:

```text
DB_USERNAME

DB_PASSWORD

JWT_SECRET
```

---

# 8. Simulate Secret Synchronization Failure

Modify the ExternalSecret.

Change:

```yaml
key: app-secret
```

To:

```yaml
key: app-secret-broken
```

Apply the updated manifest.

```bash
kubectl apply -f externalsecret.yaml
```

Inspect the ExternalSecret.

```bash
kubectl describe externalsecret app-secret
```

Expected:

```text
Ready=False

Reason=SecretSyncedError

Message:
could not get secret data from provider
```

Events:

```text
Secret does not exist
```

---

# 9. Resolve the Incident

Restore the correct AWS secret name.

```yaml
key: app-secret
```

Apply the corrected manifest.

```bash
kubectl apply -f externalsecret.yaml
```

Verify recovery.

```bash
kubectl describe externalsecret app-secret
```

Expected:

```text
Ready=True

Reason=SecretSynced

Message:
secret synced
```

---

# 10. Useful Troubleshooting Commands

List all secrets.

```bash
kubectl get secret
```

List ExternalSecrets.

```bash
kubectl get externalsecret
```

Describe ExternalSecret.

```bash
kubectl describe externalsecret app-secret
```

List SecretStores.

```bash
kubectl get secretstore
```

Describe SecretStore.

```bash
kubectl describe secretstore aws-secret-store
```

Check External Secrets Operator pods.

```bash
kubectl get pods -n external-secrets
```

View External Secrets Operator logs.

```bash
kubectl logs deployment/external-secrets \
  -n external-secrets
```

View Kubernetes events.

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

# 11. Cleanup

Delete the ExternalSecret.

```bash
kubectl delete externalsecret app-secret
```

Delete the SecretStore.

```bash
kubectl delete secretstore aws-secret-store
```

Delete the synchronized Kubernetes Secret.

```bash
kubectl delete secret app-secret
```

Delete the AWS credential Secret.

```bash
kubectl delete secret awssm-secret
```

**Keep the External Secrets Operator installed** for future exercises.

Do **not** delete:

* external-secrets namespace
* External Secrets Operator
* ArgoCD
* EKS Cluster
