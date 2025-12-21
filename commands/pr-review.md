# PR Review

Perform comprehensive code review on a pull request with security, performance, and best practices checks.

## Usage

```
/pr-review <pr-number>
```

## Process

1. Fetch PR diff and metadata
2. Analyze changes for issues
3. Check for security vulnerabilities
4. Review code style and patterns
5. Generate review comments

## Commands

```bash
# Get PR details
gh pr view <number> --json files,additions,deletions,commits

# Get diff
gh pr diff <number>

# Add review comment
gh pr review <number> --comment --body "Review feedback here"

# Approve or request changes
gh pr review <number> --approve
gh pr review <number> --request-changes --body "Issues found"
```

## Review Checklist

### Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on user data
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication/authorization checks

### Code Quality
- [ ] Functions are single-purpose
- [ ] No duplicate code
- [ ] Proper error handling
- [ ] Meaningful variable names
- [ ] Comments for complex logic

### Performance
- [ ] No N+1 queries
- [ ] Efficient algorithms
- [ ] Proper caching considerations
- [ ] No memory leaks

### Testing
- [ ] Unit tests for new code
- [ ] Edge cases covered
- [ ] Integration tests if needed

## Review Comment Format

```markdown
**Category**: Security/Performance/Style/Bug

**File**: src/auth/login.ts:42

**Issue**: Description of the problem

**Suggestion**: 
\`\`\`typescript
// Recommended fix
\`\`\`
```