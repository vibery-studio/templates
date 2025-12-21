# Fix GitHub Issue

Analyze a GitHub issue and implement the fix with proper branching and PR creation.

## Usage

```
/fix-github-issue <issue-number>
```

## Process

1. Fetch issue details from GitHub
2. Analyze issue description and comments
3. Create feature branch: `fix/issue-<number>-<slug>`
4. Implement the fix based on issue context
5. Commit with issue reference
6. Create PR linked to issue

## Commands

```bash
# Fetch issue details
gh issue view <number> --json title,body,labels,comments

# Create branch
git checkout -b fix/issue-123-login-error

# After implementing fix, commit with reference
git commit -m "fix: Resolve login timeout error

Fixes #123"

# Create PR that closes issue
gh pr create --title "fix: Resolve login timeout error" \
  --body "Fixes #123" \
  --assignee @me
```

## Commit Message Format

```
fix: <short description>

<detailed explanation if needed>

Fixes #<issue-number>
```

## Linking Keywords

These keywords auto-close issues when PR merges:
- `Fixes #123`
- `Closes #123`
- `Resolves #123`

## Labels Mapping

| Issue Label | Branch Prefix |
|-------------|---------------|
| bug | fix/ |
| enhancement | feat/ |
| documentation | docs/ |
| performance | perf/ |