# Weather App Deployment on EKS Cluster

This README provides step-by-step instructions to deploy the Weather App on an AWS EKS cluster.

---

## Prerequisites

Ensure you have the following installed:
- AWS CLI
- kubectl
- eksctl
- Docker
- OpenWeather API Key (stored securely, e.g., in AWS Secrets Manager)
- An EKS cluster created and running

---

## Steps to Deploy

### 1. Clone the Repository

```bash
# Clone the weather app repository
git clone https://github.com/<your-forked-repo>/python-weather-app.git
cd python-weather-app
```

### 2. Build and Push Docker Image

1. Build the Docker image:
   ```bash
   docker build -t <dockerhub-username>/weather-app:latest .
   ```

2. Push the image to Docker Hub:
   ```bash
   docker push <dockerhub-username>/weather-app:latest
   ```

---

### 3. Configure AWS Secrets Manager for API Key

Store the OpenWeather API key in AWS Secrets Manager:
```bash
aws secretsmanager create-secret \
    --name OWM_API_KEY \
    --description "OpenWeather API Key" \
    --secret-string '<your-api-key>'
```

Retrieve the secret in your Kubernetes deployment using `aws-sdk` (already integrated in the app).

---

### 4. Update Kubernetes Manifests

Edit the Kubernetes manifests in the `k8s-eks/` folder:

1. **Deployment (deployment.yaml)**
   Replace `<dockerhub-username>` with your Docker Hub username in the `image` field.

2. **Secrets**
   Create a Kubernetes secret to access the AWS API:
   ```bash
   kubectl create secret generic aws-secret \
       --from-literal=aws-access-key-id=<your-aws-access-key> \
       --from-literal=aws-secret-access-key=<your-aws-secret-key>
   ```

---

### 5. Apply Kubernetes Manifests

Deploy the application on EKS:

```bash
# Switch to the appropriate namespace
kubectl create namespace weather-app
kubectl config set-context --current --namespace=weather-app

# Apply manifests
kubectl apply -f k8s-eks/
```

---

### 6. Verify Deployment

Check the status of the pods and services:
```bash
kubectl get pods
kubectl get services
```

Retrieve the external LoadBalancer URL:
```bash
kubectl get service weather-app-service
```
Access the application at the provided URL.

---

## Cleanup

To clean up resources:

```bash
kubectl delete namespace weather-app
aws secretsmanager delete-secret --secret-id OWM_API_KEY
```

---

## Notes

- Ensure your EKS cluster has proper IAM permissions for Secrets Manager.
- Use a LoadBalancer or Ingress to expose the service.
- Monitor pod logs for troubleshooting:
  ```bash
  kubectl logs <pod-name>
  

