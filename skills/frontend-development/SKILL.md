---
name: frontend-development
description: Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices.
license: MIT
---

# Frontend Development Guidelines

Modern React/TypeScript development with Suspense-based patterns and performance optimization.

## Key Principles

- Implement lazy loading for heavy components (DataGrid, charts, editors)
- Use Suspense boundaries with SuspenseLoader
- Adopt useSuspenseQuery as primary data fetching pattern
- Organize features with api/, components/, hooks/, helpers/, types/ subdirectories
- Apply inline styles for <100 lines, separate files for >100 lines
- Use import aliases: @/, ~types, ~components, ~features
- Prevent layout shift by avoiding conditional loading states
- Use useMuiSnackbar for notifications

## Component Development

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

export const MyComponent: React.FC = () => (
  <Suspense fallback={<SuspenseLoader />}>
    <HeavyComponent />
  </Suspense>
);
```

## Data Fetching

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
  });

  return <div>{user.name}</div>;
}
```

## File Organization

```
src/
├── features/
│   └── users/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── helpers/
│       └── types/
├── components/  # Truly reusable
└── hooks/       # Shared hooks
```

## MUI v7 Styling

```typescript
<Box sx={{ display: 'flex', gap: 2, p: 3 }}>
  <Grid container spacing={2}>
    <Grid size={{ xs: 12, md: 6 }}>Content</Grid>
  </Grid>
</Box>
```

## Performance Patterns

```typescript
// Memoize expensive calculations
const expensiveValue = useMemo(() => compute(data), [data]);

// Memoize callbacks
const handleClick = useCallback(() => action(), []);

// Memoize components
const MemoizedComponent = React.memo(Component);
```

## TypeScript Best Practices

```typescript
// Explicit return types
function getUser(id: string): User { ... }

// Type imports
import type { User } from '~types';

// Strict mode enabled
```

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
