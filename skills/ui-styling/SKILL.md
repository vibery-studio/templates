---
name: ui-styling
description: Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Use when building UIs, implementing design systems, creating responsive layouts, or customizing themes.
license: MIT
---

# UI Styling

Build accessible, beautiful interfaces with shadcn/ui, Tailwind CSS, and Radix UI.

## Core Components

1. **shadcn/ui**: Pre-built accessible components via Radix UI primitives
2. **Tailwind CSS**: Utility-first CSS with zero runtime overhead
3. **Radix UI**: Headless UI primitives for accessibility

## When to Use

- Building React-based UIs (Next.js, Vite, Remix, Astro)
- Implementing accessible components
- Creating responsive, mobile-first layouts
- Establishing dark mode and theme customization
- Rapid prototyping with visual feedback
- Complex UI patterns (data tables, command palettes)

## Quick Start

### Initialize shadcn/ui
```bash
npx shadcn@latest init
```

### Add Components
```bash
npx shadcn@latest add button card dialog form
```

### Tailwind Only (Vite)
```bash
npm install -D tailwindcss @tailwindcss/vite
```

## Component Usage

```typescript
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="default">Click me</Button>
      </CardContent>
    </Card>
  )
}
```

## Tailwind Patterns

```html
<!-- Responsive layout -->
<div class="flex flex-col md:flex-row gap-4">

<!-- Dark mode -->
<div class="bg-white dark:bg-slate-900">

<!-- Hover states -->
<button class="bg-blue-500 hover:bg-blue-600 transition-colors">

<!-- Grid layout -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

## Best Practices

1. Compose components from primitives
2. Utility-first styling
3. Mobile-first responsive design
4. Accessibility-first implementation
5. Consistent design tokens
6. Dark mode consistency
7. Performance optimization
8. TypeScript for type safety

## Theming

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}
```

## Resources

- shadcn/ui: https://ui.shadcn.com
- Tailwind CSS: https://tailwindcss.com
- Radix UI: https://radix-ui.com

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
