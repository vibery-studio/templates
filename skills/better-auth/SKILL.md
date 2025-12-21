---
name: better-auth
description: Implement authentication and authorization with Better Auth - a framework-agnostic TypeScript authentication framework. Features include email/password, OAuth providers, two-factor auth, passkeys/WebAuthn, session management, and RBAC.
license: MIT
version: 2.0.0
---

# Better Auth

Framework-agnostic TypeScript authentication framework with comprehensive features.

## When to Use

- Implementing auth in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up 2FA, passkeys, magic links
- Building multi-tenant apps with organization support
- Managing sessions and user lifecycle
- Working with Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express

## Quick Start

### Installation
```bash
npm install better-auth
```

### Environment Setup
```env
BETTER_AUTH_SECRET=<32-char-secret>
BETTER_AUTH_URL=http://localhost:3000
```

### Basic Server Setup
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { /* config */ },
  emailAndPassword: { enabled: true, autoSignIn: true },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }
  }
});
```

### Database Schema
```bash
npx @better-auth/cli generate  # Generate schema
npx @better-auth/cli migrate   # Apply migrations
```

### Client Setup
```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: "http://localhost:3000"
});

// Sign up
await authClient.signUp.email({ email, password, name });

// Sign in
await authClient.signIn.email({ email, password });

// OAuth
await authClient.signIn.social({ provider: "github" });
```

## Feature Selection

| Feature | Plugin Required | Description |
|---------|----------------|-------------|
| Email/Password | No | Basic auth |
| OAuth | No | Social login |
| Email Verification | No | Verify emails |
| Two-Factor Auth | Yes (`twoFactor`) | TOTP/SMS |
| Passkeys | Yes (`passkey`) | WebAuthn |
| Magic Link | Yes (`magicLink`) | Email login |
| Organizations | Yes (`organization`) | Multi-tenant |

## Auth Method Guide

- **Email/Password**: Traditional web apps
- **OAuth**: Quick signup, social integration
- **Passkeys**: Modern, passwordless, secure
- **Magic Link**: Passwordless without WebAuthn

## Implementation Checklist

- [ ] Install `better-auth`
- [ ] Set environment variables
- [ ] Create auth server instance
- [ ] Run schema migration
- [ ] Mount API handler
- [ ] Create client instance
- [ ] Implement sign-up/sign-in UI
- [ ] Add session management
- [ ] Set up protected routes
- [ ] Configure email sending
- [ ] Enable rate limiting

## Resources

- Docs: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
- Plugins: https://www.better-auth.com/docs/plugins

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
