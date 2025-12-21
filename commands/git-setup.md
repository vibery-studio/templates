# Git Setup Command

Initialize and configure Git for a new project with best practices.

## What This Command Does
1. Initialize Git repository
2. Create .gitignore with common patterns
3. Set up commit message template
4. Configure branch protection recommendations
5. Create initial commit

## Usage
Run `/git-setup` in your project directory.

## Files Created

### .gitignore
- Node modules
- Build outputs
- Environment files
- IDE configurations
- OS-specific files

### .gitmessage
Commit message template following conventional commits:
```
type(scope): subject

body

footer
```

## Git Configuration Recommendations
- Enable `pull.rebase = true`
- Set `init.defaultBranch = main`
- Configure `core.autocrlf` based on OS

## Branch Strategy Suggestion
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `release/*` - Release preparation