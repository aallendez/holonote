# Holonote – Summary Report

## Overview

Holonote has evolved from an early prototype into a more stable, production-ready system. I focused on correctness, automation, deployment reliability, and observability.

### Fixed Issues from Assignment 1

I fixed the following issues from Assignment 1:
- Added an .env.example file to root folder and frontend/ folder.
- I added package-lock.json to the repo to avoid regeneration.

## Integration Tests

End-to-end integration tests now validate system behavior using an isolated environment, in-memory SQLite, and a mock authenticated user. These tests ensure workflows function correctly across components.

## Pre-Commit Automation

A comprehensive pre-commit workflow enforces code quality and security. It runs:

* Safety checks, secret scanning, and formatting (Terraform, Python, frontend)
* ESLint + TypeScript checks
* Unit tests with a minimum of 70% coverage

Commits failing these checks are blocked, ensuring consistent standards.

## CI Pipelines

**Backend CI** validates formatting and runs pytest with coverage.

**Frontend CI** runs formatter validation, ESLint, and type checking.

**Release Pipeline** automates semantic versioning, Git tagging, Docker image builds for backend + nginx, and pushes artifacts to GHCR.

## CD Pipeline

Deployment is triggered via a production version variable. The pipeline:

* Checks out the matching release tag
* Builds and uploads the frontend to S3
* Applies Terraform changes

This creates a controlled versioned deployment mechanism with simple rollbacks.

## Infrastructure

Fully defined in Terraform, allowing reproducible infra with a single `terraform apply`.

Resources used:

* S3 for frontend hosting
* ECS (Fargate) for backend
* RDS for PostgreSQL
* Secrets Manager for sensitive config
* AWS Prometheus + Grafana for monitoring

Rollbacks are simple by adjusting the production version.

## Telemetry & Monitoring

A Grafana dashboard now tracks:

* Request rate, latency (p95/p99), status codes, payload sizes
* Total requests, error rate, average latency, and RPS

It refreshes every 30 seconds and queries metrics exported by the backend. For now it's AWS-managed; future iterations will move Grafana + Prometheus into ECS to reduce cost.

## Nginx Setup

An nginx reverse proxy serves the frontend and routes API calls to the backend. It supports:

* Static file hosting with client-side routing
* Proxying `/api/` and `/short/`
* Health checks via `/nginx-health`

## Load Balancer

An ALB routes traffic to ECS tasks with:

* Public ALB security group
* Private ECS security group restricted to ALB
* Health checks on nginx
* Zero-downtime deployments via target group registration

## Future Improvements

* Add HTTPS via CloudFront + ACM
* Use CloudFront as a global CDN for lower latency, caching, and DDoS protection

This would replace the current direct S3 hosting and improve security and performance.
