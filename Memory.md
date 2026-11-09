# Memory: circuitbreakerwarehouse.com to Shopify
Last updated: 2026-11-10

## State
- Phase 0 intake: done (`PROJECT.md`).
- Phase 1-2 scan: done (`docs/site-scan.md`, `docs/feature-inventory.md`, live shots in `docs/scan/shots/live/`).
- Phase 4 plan: done; owner answered all Round 4 questions 2026-11-10.
- Phase 6 build: done for every page type (header/footer/sidebar/floating, home, collection, search, product, pages, contact, help, cart, 404). Local commits only.
- Phase 8 QA (first pass): theme check clean on CBW files; page audit desktop clean; phone tap targets fixed; results in `docs/qa/`.
- Waiting on owner data in admin (see "Owner to-do" below).

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

## Owner to-do (admin data the theme expects)
- Sidebar + phone drawer read the `collection-sidebar` menu (owner created it 2026-11-10); its links still point to `#` until collections exist.
- Manufacturer collections; home brand logos link to `/collections/{general-electric|siemens|zinsco|federal-pacific|cutler-hammer|ite|westinghouse}-circuit-breakers`.
- Assign templates in admin: `contact-us` -> `page.contact`, `help` -> `page.help`, `product-index` -> `page.product-index`, `category-index` -> `page.category-index`; menus for each Help group; page `free-shipping`; Privacy Policy footer link is `#`.
- Store name is "Test" (shows in copyright and breadcrumb).
- Product metafields `custom.type`, `custom.poles`, `custom.amperage`, `custom.voltage` (and optional `custom.condition`).
- Collection default sort (live default: price low to high); favicon.

## Commands
- Theme check: `shopify theme check --path . -o json`
- Page audit: `node .skills/site-clone/scripts/page_audit.mjs docs/qa/pages.json both`
- Screenshots: `node .skills/site-clone/scripts/screenshots.mjs docs/qa/shots-clone.json docs/qa/shots/clone`
- Cart: custom `cbw-main-cart` section (Dawn cart sections unused); `settings.cart_type` is "page" to match live. Shipping estimate uses Ajax `cart/prepare_shipping_rates.json` + `cart/async_shipping_rates.json`; coupons use `cart/update.js` `{discount: "A,B"}` (comma-separated; "" clears), verified on the dev store 2026-11-10.
- `sections/cbw-cart-header.liquid` is unused after the cart rebuild; deleting it was blocked by a tool safety check, so the owner can remove it.
- Live cart was inspected once with owner approval (2026-11-10): one item added and removed; live cart confirmed empty afterwards.
