# Memory: circuitbreakerwarehouse.com to Shopify
Last updated: 2026-11-10

## State
- Phase 0 intake: done (`PROJECT.md`).
- Phase 1-2 scan: done (`docs/site-scan.md`, `docs/feature-inventory.md`, live shots in `docs/scan/shots/live/`).
- Phase 4 plan: written (`PLAN.md`), waiting on owner approval and Round 4 answers.
- Build: not started.

## Decisions
| Date | Decision | Why | Who decided |
|---|---|---|---|
| 2026-11-10 | Full-site exact frontend copy on Dawn | Scope from intake | user |
| 2026-11-10 | Collections assumed, data later | User adds data separately | user |
| 2026-11-10 | No tracking/analytics scripts | Intake | user |
| 2026-11-10 | No redirects for now | Intake | user |
| 2026-11-10 | Commit locally, never push | Intake | user |

## Where things live
- Theme code: repo root (Dawn layout: `layout/ sections/ snippets/ blocks/ assets/ templates/ locales/ config/`).
- Local preview: `http://127.0.0.1:9292` (run `npm run dev`, i.e. `shopify theme dev`).
- Clone skill: `.skills/site-clone/` (written for WordPress; adapted for Shopify here).
- Scan output: `docs/scan/`, `docs/site-scan.md`, `docs/feature-inventory.md`.
- Fixes log: `docs/site-fixes.md`.

## Gotchas
- Header menu links in admin currently point at the wrong targets (About Us -> `/`, Contact Us -> `/collections/all`, F.A.Q. -> `/pages/contact`); that's admin data, not theme code.
- Store uses Shopify new customer accounts (`/account/login` redirects to Shopify-hosted login); Dawn copy here has no `templates/customers/`. Login/My Account pages can't be themed.
- `screenshots.mjs` in the skill was patched to accept `"format":"jpeg"` per shot: WebP can't encode full-page phone shots taller than 16,383px.
- zsh globs `?` in unquoted URLs: quote URLs in shell commands.
