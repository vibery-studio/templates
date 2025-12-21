# Add Changelog

Generate or update CHANGELOG.md based on git commits using conventional commits format.

## Usage

Run this command to update the changelog before a release.

## Process

1. Read existing CHANGELOG.md (or create new)
2. Parse git log since last release tag
3. Group commits by type (feat, fix, docs, etc.)
4. Generate formatted changelog entries
5. Add new version section at top

## Output Format

```markdown
# Changelog

## [1.2.0] - 2025-01-15

### Added
- New user authentication flow (#123)
- Dark mode support (#145)

### Fixed
- Memory leak in dashboard component (#156)
- API timeout handling (#162)

### Changed
- Upgraded dependencies to latest versions
```

## Commit Type Mapping

| Prefix | Section |
|--------|---------|
| feat | Added |
| fix | Fixed |
| docs | Documentation |
| refactor | Changed |
| perf | Performance |
| test | Tests |
| chore | Maintenance |
| BREAKING | Breaking Changes |

## Instructions

1. Find the last release tag: `git describe --tags --abbrev=0`
2. Get commits since tag: `git log <tag>..HEAD --oneline`
3. Parse conventional commit messages
4. Group by type and generate markdown
5. Prepend to CHANGELOG.md with new version header