# QA checklist

Test everything, not a sample. Samples hide the one filter value that returns nothing or the one template that breaks on phones. Automate what repeats; click through what needs judgment. Save every result under `docs/qa/` with the date.

## Contents
1. Data parity
2. Page audit (every template)
3. Visual comparison
4. Every control
5. End-to-end flows
6. Logged-in and admin views
7. SEO checks
8. Accessibility checks
9. Speed
10. Redirects and old addresses
11. Security checks
12. Reading results honestly

---

## 1. Data parity

Compare the new site against the export (not against the live pages, which may be cached):
- Counts: products (published, draft), categories, attributes and terms, pages, posts, images, menus, coupons, tax rates, shipping zones.
- Checksums: SKU + price + sale price + stock for every product; titles and content; attribute assignments.
- Ten random products field by field against the live page.
- Products with no image on live should show the placeholder, not a broken image.
- If two copies exist (A/B), compare them to each other the same way.

## 2. Page audit (every template)

List every template and state as a `pages.json`:

```json
[
  {"id": "home", "url": "http://localhost:8080/"},
  {"id": "category", "url": "http://localhost:8080/category/x/"},
  {"id": "category-p2", "url": "http://localhost:8080/category/x/page/2/"},
  {"id": "category-filtered", "url": "http://localhost:8080/category/x/?filter_size=3"},
  {"id": "product", "url": "..."},
  {"id": "product-no-photo", "url": "..."},
  {"id": "search", "url": "..."},
  {"id": "search-none", "url": "..."},
  {"id": "cart-empty", "url": "..."},
  {"id": "checkout", "url": "..."},
  {"id": "account", "url": "..."},
  {"id": "404", "url": "http://localhost:8080/does-not-exist/", "ignore": ["404"]}
]
```

Then `node scripts/page_audit.mjs pages.json both`. It reports, per page and device: JS errors, console errors, failed requests and 4xx/5xx, broken images, images without alt, sideways scroll, links/buttons without names, unlabeled fields, duplicate IDs, H1 count, skipped heading levels, small tap targets on phones, missing `lang` or title.

Expected exceptions (the 404 page returning 404, which shows up as both a request error and a console line, so ignore "404" there; an empty checkout having no H1 because it redirects) go in the `ignore` list with a comment in the QA notes. Everything else gets fixed or explained.

## 3. Visual comparison

`scripts/screenshots.mjs` with the same list of pages on live and new, desktop and phone. Put them side by side (or in a before/after slider for the client). Look at: alignment of header items, spacing, font sizes, colors, card heights, button sizes, what wraps on phones. Half-pixel differences don't matter; a cart button 11px higher than the search box does.

## 4. Every control

Write a script that walks every option, not a few:
- Every filter value on every filterable listing (and combinations if few), every sort, every per-page choice: each must return results (or a correct empty state) and status 200.
- Pagination: first, middle, last, beyond last, the jump box.
- Search: exact code, partial code, lowercase, typo, empty, no results.
- Every form: valid submission, each required field missing, invalid email, spam field filled.
- Every dropdown and custom select: opens, filters as you type, keyboard (arrows, Enter, Escape, Tab), clear button, works with JavaScript off (falls back to native select).
- Menus: hover, click, keyboard, phone menu open/close.
- Popups and tabs: open, close, Escape, focus returns, don't block checkout or sticky buttons.

If one request in a thousand fails, rerun it alone before calling it a bug; local servers time out under parallel load.

## 5. End-to-end flows

With sandbox payment and the local mail catcher:
1. Browse → filter → product → add to cart → cart count updates.
2. Cart: change quantity, remove, coupon (valid, invalid, expired), shipping estimate.
3. Checkout as guest and as a logged-in customer; each payment method in sandbox; free-shipping threshold just below and just above; a region with different rules; a taxed region.
4. Thank-you page content, order number, conversion event fired (check the tag manager preview or network log).
5. Emails: customer confirmation, admin new order, account created, password reset; correct logo, sender, wording, links pointing at the new site.
6. Admin: order visible with all details; status change sends the right email; refund in sandbox.
7. Forms: entry stored, notification received, autoresponder if any.

## 6. Logged-in and admin views

- Every template while logged in as admin: toolbars push sticky headers; check overlap.
- The admin screens the owner will use (dashboard, orders, products, pages, forms, settings): no PHP warnings, no broken layouts, no nagging notices beyond the expected ones (sandbox not live yet).
- Error log empty after a full click-through (warnings from third-party extensions noted, not hidden).

## 7. SEO checks

- Crawl the new site: every page 200 (or intended noindex/redirect), unique titles and descriptions, one H1, canonical to self, no internal links to old addresses, no links to staging/local hosts.
- Structured data valid (Rich Results Test or a schema validator) on each template.
- Sitemaps list only canonical, indexable pages; robots.txt correct for production (and noindex on staging).
- Old sitemap: every address reaches a 200 page (directly or in one 301).

## 8. Accessibility checks

- Page audit results clean.
- Keyboard-only pass on home, listing (filters!), product, cart, checkout, forms, popups.
- Screen reader spot check (NVDA or VoiceOver): page title, headings list, landmarks, form labels, status messages after add-to-cart and filtering.
- Contrast check of brand colors on text and buttons.
- 320px wide: no sideways scroll.

## 9. Speed

Same method as the baseline: logged out, fresh profile, 3+ runs, median, same pages. Report both sites in one table. Be honest about conditions (a local server isn't production; say so, and measure staging on the real host before launch).

## 10. Redirects and old addresses

`scripts/check_urls.py` on every row of the redirect map (see `url-redirects.md`). Report: tested, passed, failed, chains, by type. Rerun failures alone. Keep the CSV.

## 11. Security checks

- Config files, logs, backups, dotfiles not reachable over HTTP.
- Directory listing off; script execution blocked in uploads.
- User enumeration and XML-RPC blocked (WordPress).
- Security headers present.
- Admin accounts have two-factor; no default usernames.
- Local-only tools not present on staging/production.
- Platform file integrity checks clean (`wp core verify-checksums` and plugin checksums for WordPress).

## 12. Reading results honestly

- A check that "passed" because it didn't run is a failure. Confirm counts (1,332 requests made, 1,332 checked).
- When a failure disappears on rerun, say it was a timeout under load and show the rerun.
- When something can't be tested locally (live payments, real email deliverability, production speed), list it as "to verify on staging/production" in the launch checklist instead of claiming it.
