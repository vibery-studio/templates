# Create PR

Create a GitHub pull request with auto-generated description from commits and changes.

## Usage

Run after completing a feature branch to create a well-documented PR.

## Process

1. Ensure branch is pushed to remote
2. Analyze commits on branch
3. Generate PR title from branch name or commits
4. Create description with changes summary
5. Open PR using GitHub CLI

## Commands

```bash
# Push branch if needed
git push -u origin $(git branch --show-current)

# Create PR with generated description
gh pr create --title "feat: Add user authentication" --body "$(cat <<'BODY'
## Summary
Brief description of changes.

## Changes
- Added login component
- Implemented JWT authentication
- Added user session management

## Testing
- [ ] Unit tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed

## Screenshots
(if applicable)
BODY
)"
```

## Auto-Generated Sections

1. **Summary**: First commit message or branch description
2. **Changes**: Bullet list from commit messages
3. **Files Changed**: Key files modified
4. **Testing**: Checklist template
5. **Related Issues**: Extracted from commit messages (#123)

## Branch Name Parsing

| Branch | PR Title |
|--------|----------|
| feat/user-auth | feat: User auth |
| fix/login-bug | fix: Login bug |
| feature/JIRA-123-auth | JIRA-123: Auth |