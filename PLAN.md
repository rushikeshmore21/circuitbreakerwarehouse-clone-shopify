# PLAN: circuitbreakerwarehouse.com to Shopify (Dawn base)

Sources: `docs/site-scan.md`, `docs/feature-inventory.md`, live screenshots in `docs/scan/shots/live/`, intake in `PROJECT.md`.

## 0. Blocked on owner
| Need | Why |
|---|---|
| Contact form: Shopify native form or the existing Wufoo embed | Decides where messages go |
| Trust seals: Volusion SSL seals, "Ecommerce Software by Volusion", buySAFE/Norton seal | They certify the old platform/account; shown on Shopify they'd be untrue unless the account moves |
| "Leave a Message" tab behavior | It's a third-party widget in an iframe; vendor unknown |
| Filled cart reference | Seeing it means adding an item to the live server cart (a write) |
| Wishlist and reviews | Volusion built-ins; Shopify has neither natively (apps only) |
| Product data for spec lines | Specs live only in product descriptions today; template reads metafields `custom.type`, `custom.poles`, `custom.amperage`, `custom.voltage`, `custom.condition` once you add them |

## 1. Architecture
- Keep Dawn's working parts: product form + cart JS, cart notification/drawer, predictive search, facets JS, `global.js`, Shopify forms. Replace the visible markup with new `cbw-*` sections and snippets that match the live site.
- Layout: `layout/theme.liquid` keeps `content_for_header` / `content_for_layout`, loads the Cooper Hewitt webfont and one small `assets/cbw-base.css` (tokens, container, buttons: needed on every page). Everything else lives in each section/snippet's `{% stylesheet %}`.
- Header group: `cbw-top-bar`, `cbw-header` (utility bar, logo, search, cart, nav, phone drawer). Footer group: `cbw-footer`. Floating elements (seal, message tab, back-to-top) in a `cbw-floating` section in the footer group.
- Sidebar: Shopify sections stack vertically, so the two-column pages (home grid, collection, search, product) render `snippets/cbw-sidebar.liquid` inside their main section. Its content (manufacturers menu, card image, newsletter, seals) comes from theme settings, so it's edited once for all pages.
- All text through `locales/en.default.json`; schema labels through `en.default.schema.json`.
- Every Liquid file: Shopify docs search before writing, `validate.mjs` after.

## 2. Data mapping (theme reads; admin data is the owner's later phase)
| Live field | Shopify field |
|---|---|
| Our Price | `compare_at_price` when on sale, else `price` |
| Sale Price / You Save | `price` / `compare_at_price - price` (only when on sale) |
| Product Code | `variant.sku` (live shows code without `-N`; store SKUs carry `-N` for new: shown as stored) |
| Condition | metafield `custom.condition`, fallback tag `New` / `Refurbished` |
| Type, Pole, Amperage, Voltage | metafields `custom.type`, `custom.poles`, `custom.amperage`, `custom.voltage` (hidden when empty) |
| Manufacturer category | collection (assumed to exist; sidebar menu built in admin) |
| Articles 242/243/252/57, help | pages `about-us`, `contact`, `faq`, `free-shipping`, `help` |

## 3. URL strategy
No redirects for now (owner decision). Old Volusion URLs will 404 until a redirect CSV is built in the data phase.

## 4. Layout per page type (match first; fixes marked FIX)
| Page | New files | Notes |
|---|---|---|
| All | `sections/cbw-top-bar`, `cbw-header`, `cbw-footer`, `cbw-floating`, `snippets/cbw-sidebar`, `cbw-icon`, `assets/cbw-base.css`, fonts | FIX: skip link, visible focus, labelled search |
| Home | `cbw-hero`, `cbw-featured-products`, `cbw-confidence`, `cbw-brands`, `cbw-callout`, `snippets/cbw-product-card`, `cbw-price` | Featured grid from a collection picker (live randomizes) |
| Collection | `cbw-main-collection`, `snippets/cbw-breadcrumb`, `cbw-listing-toolbar`; `templates/collection.json` + `collection.50.json` etc. for per-page | Sort via `sort_by`; per-page via `?view=`; jump box + NEXT |
| Product | `cbw-main-product` (Dawn product-form inside), `cbw-related-products`, recently viewed JS | Larger Photo in `<dialog>`; JSON-LD |
| Search | `cbw-main-search` | FIX: no-results message |
| Pages | restyled `main-page`; `templates/page.contact.json` (photo + heading + email + form); `page.help.json` with `cbw-link-columns` section | FIX: one H1 per page |
| Cart | restyle `main-cart-items` / `main-cart-footer` | Pending filled-cart reference |
| 404 | restyle `main-404` | FIX: themed page with search |
| Account | none | Shopify-hosted customer accounts; "My Account" links to `routes.account_url` |

## 5. Feature parity
Full list with status in `docs/feature-inventory.md`.

## 6-8. SEO, accessibility, performance targets
- One H1 per page, unique titles, canonical, JSON-LD (Product/Offer, BreadcrumbList, Organization). Live: 32 of 42 sampled pages have H1 count != 1, 26 have no meta description.
- WCAG 2.2 AA defaults from the skill: labels, focus, contrast, tap targets, no sideways scroll at 320px.
- Images through `image_url` + `image_tag` with widths/srcset, lazy below the fold, hero preloaded. No jQuery.

## 9. Phases
1. Foundation: fonts, tokens, header, footer, sidebar, floating. Compare at 1440 and 390.
2. Home sections.
3. Collection + search.
4. Product.
5. Pages, contact, help, cart, 404.
6. QA: page audit script on the local store, side-by-side screenshots, every control, logged fixes in `docs/site-fixes.md`.
Each phase: local git commit (never pushed).

## Definition of done (per page type)
Matches the live screenshot at 1440px and 390px (or the difference is logged as a FIX / platform limit), works with keyboard, no console errors, theme check clean, Liquid validated with the Shopify validator.
