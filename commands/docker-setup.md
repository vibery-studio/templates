# Docker Setup Command

Create Docker configuration for containerizing your application.

## What This Command Does
1. Detect project type and framework
2. Create optimized Dockerfile
3. Generate docker-compose.yml
4. Add .dockerignore
5. Create development and production configurations

## Files Created

### Dockerfile
- Multi-stage build (when applicable)
- Optimized layer caching
- Security best practices
- Non-root user

### docker-compose.yml
- Application service
- Database service (if needed)
- Volume mounts
- Network configuration
- Environment variables

### .dockerignore
- node_modules
- .git
- Build artifacts
- Local configuration

## Usage Examples

### Development
```bash
docker-compose up -d
docker-compose logs -f app
```

### Production Build
```bash
docker build -t myapp:latest .
docker run -p 3000:3000 myapp:latest
```

## Best Practices Applied
- Minimal base images (alpine when possible)
- Layer optimization
- Build caching
- Health checks
- Graceful shutdown handling