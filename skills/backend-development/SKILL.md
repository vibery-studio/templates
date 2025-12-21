---
name: backend-development
description: Build robust backend systems with modern technologies (Node.js, Python, Go, Rust), frameworks (NestJS, FastAPI, Django), databases (PostgreSQL, MongoDB, Redis), APIs (REST, GraphQL, gRPC), authentication (OAuth 2.1, JWT), testing strategies, security best practices (OWASP Top 10), performance optimization, scalability patterns, and DevOps practices.
license: MIT
version: 1.0.0
---

# Backend Development

Production-ready backend development with modern technologies and best practices.

## When to Use

- Designing RESTful, GraphQL, or gRPC APIs
- Building authentication/authorization systems
- Optimizing database queries and schemas
- Implementing caching and performance optimization
- OWASP Top 10 security mitigation
- Designing scalable microservices
- Testing strategies (unit, integration, E2E)
- CI/CD pipelines and deployment

## Quick Decision Matrix

| Need | Choose |
|------|--------|
| Fast development | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency | Go + Gin |
| Max performance | Rust + Axum |
| ACID transactions | PostgreSQL |
| Flexible schema | MongoDB |
| Caching | Redis |
| Internal services | gRPC |
| Public APIs | GraphQL/REST |
| Real-time events | Kafka |

## Key Best Practices (2025)

### Security
- Argon2id for passwords
- Parameterized queries (98% SQL injection reduction)
- OAuth 2.1 + PKCE
- Rate limiting
- Security headers

### Performance
- Redis caching (90% DB load reduction)
- Database indexing (30% I/O reduction)
- CDN (50%+ latency cut)
- Connection pooling

### Testing
- 70-20-10 pyramid (unit-integration-E2E)
- Vitest 50% faster than Jest
- Contract testing for microservices

### DevOps
- Blue-green/canary deployments
- Feature flags (90% fewer failures)
- Kubernetes 84% adoption
- Prometheus/Grafana monitoring

## Implementation Checklist

### API
- [ ] Choose style (REST/GraphQL/gRPC)
- [ ] Design schema
- [ ] Validate input
- [ ] Add auth
- [ ] Rate limiting
- [ ] Documentation
- [ ] Error handling

### Database
- [ ] Choose DB
- [ ] Design schema
- [ ] Create indexes
- [ ] Connection pooling
- [ ] Migration strategy
- [ ] Backup/restore

### Security
- [ ] OWASP Top 10 review
- [ ] Parameterized queries
- [ ] OAuth 2.1 + JWT
- [ ] Security headers
- [ ] Rate limiting
- [ ] Input validation

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
