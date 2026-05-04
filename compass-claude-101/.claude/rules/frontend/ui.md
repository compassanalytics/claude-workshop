---
paths:
  - "web/src/**/*.tsx"
  - "web/src/**/*.ts"
---

# Frontend UI Rules

Apply when reading or editing files under `web/src/`.

## Imports & exports
- Named exports only. No `export default`. Components: `export function LoginForm() { ... }`.
- Component imports use named form: `import { LoginForm } from "../components/LoginForm"`.
- One component per file. Filename matches the component name (`EventTable.tsx` → `EventTable`).

## Components
- Functional components with hooks. NO class components.
- Props typed with named interfaces above the component:
  ```tsx
  interface EventTableProps { limit?: number; }
  export function EventTable({ limit = 50 }: EventTableProps) { ... }
  ```
- Don't use anonymous inline prop types.

## Data fetching
- All API calls live in hooks under `web/src/hooks/`. Components do NOT call `fetch` or `axios` directly.
- Hooks return EXACTLY this shape:
  ```ts
  { data: T | undefined; isLoading: boolean; error: string | undefined }
  ```
- `error` is a user-readable string, never an `Error` instance, never an HTTP status code.
- The auth hook is `useAuth()` from `web/src/hooks/useAuth.ts`. Don't introduce a parallel auth state.
- The events hook is `useEvents()` from `web/src/hooks/useEvents.ts`.

## Styling
- Tailwind utility classes only. No CSS-in-JS, no separate `.css` files.
- Use the Tailwind scale (`p-2`, `gap-4`). Don't use arbitrary values like `p-[13px]`.

## State
- Local UI state: `useState`.
- Server state: hooks from `web/src/hooks/`.
- No global state library. Lift state up or keep it per-feature.

## Forms
- Controlled inputs only.
- Submit handlers are `async` and disable the form during submission.
