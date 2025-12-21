---
name: web-frameworks
description: Modern full-stack web development using Next.js, Turborepo, and RemixIcon. Use when building SSR/SSG applications, monorepos, or full-stack TypeScript projects.
license: MIT
---

# Web Frameworks

Comprehensive guide for modern full-stack web development using Next.js, Turborepo, and RemixIcon.

## Components

- **Next.js**: React framework with SSR, SSG, RSC, and optimization
- **Turborepo**: Build system for monorepos with intelligent caching
- **RemixIcon**: 3,100+ outlined and filled style icons

## When to Use

- Standalone applications (e-commerce, SaaS, docs)
- Multi-package monorepos with shared components
- Full-stack TypeScript projects
- Teams needing remote caching and collaborative builds

## Quick Start

### Next.js App
```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

### Turborepo Monorepo
```bash
npx create-turbo@latest my-monorepo
cd my-monorepo
npm run dev
```

## Next.js Patterns

### Server Components (Default)
```typescript
// app/page.tsx - Server Component by default
async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}
```

### Client Components
```typescript
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### Data Fetching
```typescript
// Server-side fetch with caching
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // Revalidate every hour
})
```

## Turborepo Structure

```
my-monorepo/
├── apps/
│   ├── web/          # Next.js app
│   └── docs/         # Documentation site
├── packages/
│   ├── ui/           # Shared components
│   ├── config/       # Shared configs
│   └── utils/        # Shared utilities
└── turbo.json
```

### turbo.json
```json
{
  "pipeline": {
    "build": { "dependsOn": ["^build"] },
    "dev": { "cache": false },
    "lint": {}
  }
}
```

## RemixIcon Usage

```bash
npm install remixicon
```

```typescript
import 'remixicon/fonts/remixicon.css'

// In component
<i className="ri-home-line" />
<i className="ri-home-fill" />
```

## Best Practices

- Default to Server Components in Next.js
- Structure monorepos with clear app/packages separation
- Use RemixIcon with accessibility (aria-label)
- Enable Turborepo remote caching for teams
- Implement proper error boundaries

## Resources

- Next.js: https://nextjs.org/docs
- Turborepo: https://turbo.build/repo
- RemixIcon: https://remixicon.com

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
