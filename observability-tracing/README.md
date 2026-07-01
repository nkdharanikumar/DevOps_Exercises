# Kubernetes Observability Platform

## Overview

A production-inspired observability platform built on Kubernetes using
three Flask-based microservices. The project demonstrates application
deployment, service-to-service communication, metrics collection with
Prometheus, visualization with Grafana, and distributed tracing
readiness with Tempo.

## Architecture

``` text
                User
                  |
                  v
        Checkout Service
                  |
                  v
       Inventory Service
                  |
                  v
        Payment Service
                  |
        -------------------
        |                 |
        v                 v
   Prometheus         OpenTelemetry
        |                 |
        v                 v
     Grafana ----------> Tempo
```

## Features

-   Dockerized Python Flask microservices
-   Kubernetes Deployments and Services
-   Health probes (Readiness & Liveness)
-   Prometheus metrics endpoint (`/metrics`)
-   Prometheus Operator + ServiceMonitor
-   Grafana dashboards
-   Tempo deployment for distributed tracing
-   Service-to-service REST communication
-   Minikube-based local Kubernetes environment

## Tech Stack

-   Kubernetes (Minikube)
-   Docker
-   Python 3.11
-   Flask
-   Prometheus
-   Prometheus Operator
-   Grafana
-   Tempo
-   OpenTelemetry (instrumentation)
-   Git

## Project Structure

``` text
observability-tracing/
├── services/
│   ├── checkout-service/
│   ├── inventory-service/
│   └── payment-service/
├── kubernetes/
│   ├── checkout/
│   ├── inventory/
│   ├── payment/
│   └── monitoring/
└── README.md
```

## Prerequisites

-   Docker
-   Minikube
-   kubectl
-   Git

## Deployment

### Start Minikube

``` bash
minikube start
```

### Deploy Monitoring Stack

``` bash
kubectl apply -f kubernetes/monitoring/
```

### Build Images

``` bash
docker build -t payment-service:v1 ./services/payment-service
docker build -t inventory-service:v1 ./services/inventory-service
docker build -t checkout-service:v1 ./services/checkout-service
```

### Deploy Applications

``` bash
kubectl apply -f kubernetes/payment/
kubectl apply -f kubernetes/inventory/
kubectl apply -f kubernetes/checkout/
```

## Verify

``` bash
kubectl get pods -n observability
kubectl get pods -n observability-app
```

## Port Forwarding

### Grafana

``` bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n observability
```

### Prometheus

``` bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n observability
```

### Services

``` bash
kubectl port-forward svc/checkout-service 6000:5000 -n observability-app
kubectl port-forward svc/inventory-service 6001:5001 -n observability-app
kubectl port-forward svc/payment-service 6002:5002 -n observability-app
```

## Prometheus Metrics

Example queries:

``` promql
checkout_requests_total
inventory_requests_total
payment_requests_total
up
```

## Future Enhancements

-   Complete distributed tracing across all services
-   OpenTelemetry Collector integration
-   Loki for centralized logging
-   Alertmanager notifications
-   CI/CD pipeline with GitHub Actions
-   Helm packaging

## Resume Highlights

-   Built a Kubernetes-based observability platform with three
    containerized microservices.
-   Implemented Prometheus monitoring and custom application metrics.
-   Configured Grafana dashboards and Prometheus Operator
    ServiceMonitors.
-   Deployed Tempo to support distributed tracing.
-   Managed Kubernetes deployments, services, health probes, and
    networking in Minikube.

## License

MIT License
