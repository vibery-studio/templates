# Test Setup Command

Set up a testing framework for your project.

## What This Command Does

1. Detect project type (Node, Python, etc.)
2. Install appropriate testing framework
3. Create test configuration
4. Set up test directory structure
5. Create example test file

## Supported Frameworks

### JavaScript/TypeScript

- Jest (recommended)
- Vitest
- Mocha + Chai

### Python

- pytest (recommended)
- unittest

### Go

- Built-in testing package

## Directory Structure

```
project/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── jest.config.js (or equivalent)
└── package.json (updated scripts)
```

## Test Scripts Added

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Example Test

Creates a sample test file demonstrating:

- Test structure
- Assertions
- Mocking basics
- Async testing
