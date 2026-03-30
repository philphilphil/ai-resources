---
description: 'React and TypeScript conventions. Covers component patterns, hooks, state management, and shared UI systems.'
applyTo: '**/*.tsx,**/*.ts,**/*.jsx,**/*.js'
---

# React & TypeScript Conventions

## Shared UI System

Reusable visual components should live in a shared package (e.g., `packages/ui/`) and be imported across apps from a single source.

### Component Patterns

- **CVA (class-variance-authority)** for variant management — define variants and sizes declaratively
- **Radix UI `Slot`** for `asChild` polymorphism — components can render as any element
- **`cn()` utility** for Tailwind class merging (`clsx` + `tailwind-merge`)
- Export both the component and its variants type (e.g., `Button`, `ButtonProps`, `ButtonVariants`)

### Naming & Structure

```
packages/ui/src/components/
  primitives/    → Button, Badge, Card, Input (visual atoms)
  composed/      → domain-specific display components
```

### Accessibility

- Use `aria-invalid`, `focus-visible:ring` patterns
- Add `data-slot` and `data-variant` attributes for CSS hooks
- Support keyboard navigation on interactive components

## Component Best Practices

- **When to Create a Component:**
  - If a UI pattern is reused more than once
  - If a section is complex or self-contained
  - If it improves readability or testability
- **Naming:**
  - Use `PascalCase` for component files and exports (e.g., `UserCard.tsx`)
  - Use `camelCase` for hooks (e.g., `useUser.ts`)
  - Use `snake_case` or `kebab-case` for static assets
- **Props:**
  - Use TypeScript interfaces for props
  - Prefer explicit prop types and default values
- **Testing:**
  - Co-locate tests with components (e.g., `UserCard.test.tsx`)

## TypeScript Types

- Define shared types in a dedicated package or `types/` directory
- Use explicit interfaces and type aliases — avoid `any`
- Keep type definitions close to where they are used; export to shared packages only when genuinely reused
- Prefer `unknown` over `any` when the type is not yet determined

## Styling

- Use Tailwind CSS with a shared config when applicable
- When using a monorepo, ensure shared component packages are included in each app's Tailwind `content` paths so classes aren't purged
- Use semantic design tokens (colors, spacing) rather than raw values

## Hooks Conventions

- Prefix with `use` (standard React convention)
- Hooks that manage async data (WebSocket, polling, fetch) should handle lifecycle (connect/disconnect/reconnect/cleanup)
- Return stable references — use `useCallback`/`useMemo` for objects and functions passed to children
- Co-locate hooks with the feature they serve; extract to `hooks/` only when shared across multiple components

## State Management

- Prefer local component state for UI concerns (panel open/close, form input)
- Use custom hooks for domain data (data streams, async resources)
- Reach for a global state library (Zustand, Jotai, Redux Toolkit) only when state genuinely spans multiple unrelated subtrees
- Lift state up to the nearest common ancestor before introducing a global store

## Avoid Unnecessary Example Files

Do not create example/demo files in the main codebase unless the user specifically requests a live example, Storybook story, or documentation component. Keep the repository clean and production-focused by default.
