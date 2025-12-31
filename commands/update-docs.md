# Update Docs

Automatically update documentation based on code changes, including README, API docs, and inline comments.

## Usage

Run after making code changes to keep documentation in sync.

## Process

1. Analyze changed files
2. Identify documentation impacts
3. Update relevant doc files
4. Generate missing documentation
5. Validate doc links and references

## Documentation Types

### README.md

- Update installation instructions
- Add new features to feature list
- Update configuration examples
- Refresh API usage examples

### API Documentation

- Update endpoint descriptions
- Refresh request/response examples
- Update authentication requirements
- Add new endpoints

### Code Comments

- Add JSDoc/TSDoc for new functions
- Update existing comments for changes
- Add inline comments for complex logic

## Commands

```bash
# Find files changed since last commit
git diff --name-only HEAD~1

# Generate TypeScript docs
npx typedoc --out docs src/

# Update README TOC
npx markdown-toc -i README.md

# Check for broken links
npx markdown-link-check README.md
```

## Documentation Templates

### Function JSDoc

```typescript
/**
 * Brief description of function.
 *
 * @param param1 - Description of param1
 * @param param2 - Description of param2
 * @returns Description of return value
 * @throws {ErrorType} When error condition occurs
 * @example
 * const result = myFunction('input');
 */
```

### API Endpoint

```markdown
## GET /api/users/:id

Retrieve a user by ID.

**Parameters**
| Name | Type | Description |
|------|------|-------------|
| id | string | User ID |

**Response**
\`\`\`json
{ "id": "123", "name": "John" }
\`\`\`
```
