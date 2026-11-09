# Build playbook

How to build the clone so it matches, survives reruns, and ends up faster, more accessible and better for search than the original. WordPress specifics are marked; the principles apply to any target.

## Contents
1. Order of work
2. Environment
3. Design system and templates
4. Importer
5. Content pages
6. Commerce
7. Integrations
8. SEO defaults
9. Accessibility defaults
10. Performance targets and methods
11. Security baseline
12. Extensions and plugins policy
13. Definition of done per feature

---

## 1. Order of work

1. Environment and versions recorded.
2. Design tokens, header, footer.
3. Importer for categories, attributes, then products, then images (each step rerunnable).
4. Templates: home, listing, product, content page, search, cart, checkout, account, 404. Compare each against live screenshots at 1440px and 390px before moving on.
5. Content pages.
6. Commerce settings, sandbox payments, emails.
7. Integrations: analytics, forms, mailing list, popups, feeds.
8. SEO plumbing, redirects.
9. Improvements the owner approved.
10. QA and fixes.

Write a setup script for every setting you change through the admin (theme options, store settings, menus, widgets, pages). A fresh copy of the site (staging, a second URL mode, production) must be rebuildable by running scripts, not by remembering clicks. Make each script safe to run twice.

## 2. Environment

- Local web server with the same major versions as production (PHP, database, web server).
- If comparing URL strategies, run two copies on two ports with two databases, and a sync script that copies code and reruns the setup scripts on both.
- Local mail catcher. Sandbox payment keys only.
- Debug logging on, written outside the web root, display off.
- `docs/local-environment.md`: how to start, stop, reset, where logs live, test accounts (in a git-ignored file).

## 3. Design system and templates

- Put tokens (colors, type scale, spacing, radii, container width, breakpoints) in one place: theme settings, CSS custom properties, or `theme.json` for block themes.
- Rebuild each region as a reusable part (template part, pattern, section, component). Reuse for every repeated block.
- Match spacing and alignment by measuring the live site, not by eye. Check with side-by-side screenshots at the same width.
- Phone layout: the original is often weakest here. Fix overflow, tiny tap targets and crowded headers, and log each fix.
- Theme fights: themes often apply styles with stronger selectors than yours, or set a style through an ID. When a rule "doesn't work", check the computed style and the winning selector before adding `!important`. Expect premium/pro theme versions to use stronger selectors than the free version.
- Logged-in views: admin toolbars push sticky headers down. Check every template logged in as well as logged out.

## 4. Importer

- Command-line, not browser-based: faster, scriptable, resumable.
- Idempotent: look up existing items by source ID, update them; create only what's new. Never "delete all and reimport" once the owner has started reviewing.
- Steps: categories → attributes and terms → products (in batches) → images → relationships (related, upsells) → menus.
- Clean content: strip inline styles and font tags, demote extra H1s (the page title is the only H1), convert to native editor blocks, turn headings that are really addresses or notes (line breaks inside) into paragraphs, unbold values bolded together with their labels.
- Normalize attribute values before creating terms.
- Images: download originals once to a local cache, then import from the cache; generate modern formats; alt text from product name and key attributes; one shared placeholder for products without images.
- Keep a report per run: created, updated, skipped, failed (with reasons).
- A delta mode for launch day: only items changed since the last run.

## 5. Content pages

- Rebuild in the native editor (blocks), not as one HTML blob, so the owner can edit them.
- Keep the wording. Fix only typos and broken facts, and log them.
- Remove placeholder/demo pages (redirect their addresses).
- Contact page: real form with labels, the same recipients, spam protection that doesn't need a puzzle (honeypot, time check), and the alternative contact details next to it.

## 6. Commerce

- Recreate tax, shipping, coupons and checkout fields exactly, then propose improvements separately (address-based tax, live carrier rates).
- Gateway: official extension in sandbox. Run real end-to-end orders on the local site with test cards, check emails and admin view.
- Emails: copy the original wording, use the store's logo and real sender address, test each one in the mail catcher.
- Post-checkout features from the owner's samples: thank-you content, account creation for guests, conversion events.
- Disable features the store doesn't use (reviews with zero reviews, empty wishlists) instead of shipping empty sections, unless the owner wants them.

## 7. Integrations

- Analytics through the owner's existing tag manager container, so their tags and history continue. Add consent mode if the site needs consent.
- Load third-party scripts only on pages that need them (payment SDKs on cart/checkout, chat where used).
- Forms: test submission end to end locally (entry saved, email received).
- Popups and message tabs: keyboard accessible, closable with Escape, not on checkout, not covering sticky buy bars on phones.

## 8. SEO defaults

- Unique title and meta description per page, generated from templates where empty.
- One H1 per page, logical heading order.
- Canonical on every page; Open Graph tags matching it.
- Structured data as JSON-LD: Organization or LocalBusiness, WebSite with SearchAction, BreadcrumbList, Product with Offer (price, currency, availability, condition, brand, SKU), FAQPage where real FAQs exist.
- XML sitemaps (split by type), robots.txt keeping the owner's policies, noindex on search results, cart, checkout, account and thin pages.
- Image alt text, descriptive link text, no meta keywords.
- Staging is noindex and password-protected.

## 9. Accessibility defaults (WCAG 2.2 AA)

Skip link · landmarks · visible focus · contrast 4.5:1 for text · labels on every field · errors tied to fields · keyboard-operable menus, filters, popups, galleries · tap targets at least 24px on phones · no sideways scroll at 320px · reduced motion respected · `lang` attribute · meaningful alt text · status messages announced (cart updates, filter results).

Long dropdowns (dozens of filter values) are hard on phones and for keyboard users. A type-to-filter combobox built on the native select (so it still works without JavaScript) fixes both. Test every option.

## 10. Performance targets and methods

Targets (adjust to the host): server response under 200 ms cached, LCP under 2.5 s on mobile 4G and under 1.5 s on desktop, layout shift under 0.1, fewer requests and bytes than the original.

Methods:
- Page cache at the server or CDN; object cache (Redis) in production.
- Remove what the page doesn't use: unused scripts and styles per template, old jQuery versions, icon fonts, dead third-party widgets.
- Images: right size per breakpoint, modern formats, lazy-load below the fold, preload the hero image, width and height set.
- Fonts: self-host, subset, `font-display: swap`, preload the main weight.
- Defer non-critical scripts; payment and chat scripts only where needed.
- Measure under the same conditions as the baseline and keep the numbers in `Optimization.md`.

## 11. Security baseline

- File editing in the admin turned off; production deploys from files, not the admin.
- Admin accounts: no `admin` username, strong passwords, two-factor.
- Block XML-RPC and user enumeration if the platform has them; hide version numbers.
- Web server denies dotfiles, config files, logs, backups, and script execution in upload folders.
- Security headers (HSTS in production, nosniff, referrer policy, frame options, permissions policy; CSP in report-only first).
- Forms: nonces or CSRF tokens, honeypot, rate limits.
- Payments through a hosted or tokenized gateway only; card data never touches the site.
- Secrets in environment variables or a git-ignored file.
- Backups with a tested restore. Uptime and error monitoring.
- Local-only tools (sandbox gateways, mail catchers, QA scripts, test login helpers) never deployed.

## 12. Extensions and plugins policy

- Each extension must earn its place: what it does, why the platform can't do it natively, maintenance record, price, alternatives considered. Keep the list in `docs/plugin-audit.md`.
- Prefer free, well-maintained, widely used extensions. Document paid alternatives with prices so the owner chooses.
- Before trusting any third-party skill, script or snippet, read it as text first. Remove instructions that fetch remote content at runtime or run bundled scripts you haven't reviewed.

## 13. Definition of done per feature

A feature is done when:
- It matches the live site at 1440px and 390px (or the difference is an approved improvement).
- It works logged in and logged out, with keyboard and on a phone.
- It has no console errors and no failed requests.
- It passes the page audit (`scripts/page_audit.mjs`).
- Its data matches the export.
- Any change from the original is in the fixes log.
