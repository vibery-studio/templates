# Test Coverage

Analyze and improve test coverage across the codebase with detailed reporting.

## Usage

Run to generate coverage reports and identify untested code paths.

## Process

1. Run test suite with coverage enabled
2. Generate coverage report (HTML, JSON, LCOV)
3. Analyze uncovered lines and branches
4. Identify critical paths needing tests
5. Report coverage metrics

## Commands by Framework

### Jest (JavaScript/TypeScript)
```bash
# Generate coverage report
npx jest --coverage

# With specific thresholds
npx jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80}}'

# Output formats
npx jest --coverage --coverageReporters=html --coverageReporters=lcov
```

### Vitest
```bash
npx vitest --coverage

# With UI
npx vitest --coverage --ui
```

### pytest (Python)
```bash
# Generate coverage
pytest --cov=src --cov-report=html

# With branch coverage
pytest --cov=src --cov-branch --cov-report=term-missing
```

### Go
```bash
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

## Coverage Metrics

| Metric | Description |
|--------|-------------|
| Line Coverage | % of lines executed |
| Branch Coverage | % of branches (if/else) taken |
| Function Coverage | % of functions called |
| Statement Coverage | % of statements executed |

## Coverage Targets

| Level | Coverage |
|-------|----------|
| Minimal | 60% |
| Good | 80% |
| Excellent | 90%+ |

## Output

```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   85.23 |    78.45 |   89.12 |   85.23 |
 src/auth/          |   92.00 |    88.00 |   95.00 |   92.00 |
 src/utils/         |   78.00 |    65.00 |   82.00 |   78.00 |
--------------------|---------|----------|---------|---------|
```