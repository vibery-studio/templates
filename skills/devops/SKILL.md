---
name: devops
description: Deploy and manage cloud infrastructure on Cloudflare (Workers, R2, D1, KV, Pages), Docker containers, and Google Cloud Platform (Compute Engine, GKE, Cloud Run). Use when deploying serverless functions, managing Docker containers, setting up CI/CD pipelines, or working with cloud infrastructure.
license: MIT
version: 1.0.0
---

# DevOps Skill

Comprehensive guidance for deploying cloud infrastructure across Cloudflare, Docker, and Google Cloud Platform.

## Platform Selection

| Need | Platform |
|------|----------|
| Ultra-low latency (<50ms) | Cloudflare Workers |
| Zero egress costs | Cloudflare R2 |
| Containerized workloads | Docker + Cloud Run |
| ML pipelines | GCP Vertex AI |
| Static sites | Cloudflare Pages |
| Stateful edge compute | Cloudflare Durable Objects |

## Cloudflare

### Workers (Serverless Edge)
```bash
npm create cloudflare@latest
npx wrangler deploy
```

**Use for:** API endpoints, edge processing, A/B testing

### R2 (Object Storage)
```bash
npx wrangler r2 bucket create my-bucket
```

**Use for:** Media storage, backups (zero egress)

### D1 (SQLite at Edge)
```bash
npx wrangler d1 create my-db
```

### Pages (Static Sites)
```bash
npx wrangler pages deploy ./dist
```

## Docker

### Basic Workflow
```bash
# Build
docker build -t myapp:latest .

# Run
docker run -p 3000:3000 myapp:latest

# Push to registry
docker push myimage:tag
```

### Multi-stage Build
```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-slim
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## Google Cloud Platform

### Cloud Run
```bash
gcloud run deploy myapp \
  --image gcr.io/project/myapp \
  --platform managed \
  --region us-central1
```

### GKE (Kubernetes)
```bash
gcloud container clusters create my-cluster
kubectl apply -f deployment.yaml
```

## CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: npx wrangler deploy
```

## Best Practices

- Use environment variables for secrets
- Implement health checks
- Set up monitoring (Prometheus/Grafana)
- Use blue-green or canary deployments
- Enable auto-scaling

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
