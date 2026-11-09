# Platform notes

Quick facts for common source and target platforms: how to get data out, what addresses look like, and the traps. Admin menus move around between releases, so treat menu paths as a starting point and check the platform's current help docs before telling the owner where to click.

## Contents
1. Detecting the platform
2. Source platforms
3. Target platforms
4. Data mapping patterns

---

## 1. Detecting the platform

`scripts/fingerprint.py` checks these signals. Confirm by hand.

| Signal | Points to |
|---|---|
| `/v/vspfiles/` paths, `-p/CODE.htm` and `-s/ID.htm` addresses, `.asp` pages | Volusion |
| `cdn.shopify.com`, `Shopify.theme`, `/products/handle`, `/collections/handle` | Shopify |
| `cdn11.bigcommerce.com`, `stencil` | BigCommerce |
| `wp-content`, `wp-json`, `<meta name="generator" content="WordPress`, `woocommerce` classes | WordPress / WooCommerce |
| `static/version`, `Magento_`, `mage/` | Magento / Adobe Commerce |
| `static.wixstatic.com`, `wix.com` meta | Wix |
| `static1.squarespace.com`, `Squarespace` comments | Squarespace |
| `assets.website-files.com` or `cdn.prod.website-files.com`, `data-wf-site` | Webflow |
| `/sites/default/files`, `Drupal.settings`, `X-Generator: Drupal` | Drupal |
| `/media/jui/`, `Joomla` generator | Joomla |
| `prestashop` in scripts, `/modules/` + `id_product` | PrestaShop |
| `index.php?route=product/` | OpenCart |
| `_next/static`, `__NEXT_DATA__` | Next.js (custom) |
| `x-powered-by` headers, `cf-ray` (Cloudflare), `x-vercel-id`, `x-nf-request-id` (Netlify) | Server / CDN |

## 2. Source platforms

### Volusion
- **Export:** Admin > Inventory > Import/Export (products, categories, product-category links, options, articles, customers, orders, coupons, and more; choose "all fields", CSV). Settings live in admin screens; take screenshots or copy values.
- **Addresses:** products `/{Any-Name}-p/{code}.htm` (the name part is ignored, so any text works), short form `/product-p/{code}.htm`, `ProductDetails.asp?ProductCode=`; categories `/{Name}-s/{id}.htm`, `/category-s/{id}.htm`, `SearchResults.asp?Cat={id}`; articles `Articles.asp?ID=` (and `.php`); system pages `.asp` and `.php` forms both answer.
- **Images:** `/v/vspfiles/photos/{CODE}-{n}{size}.jpg` (e.g. `-2T` thumbnail). Downloadable directly.
- **Traps:** product codes with `-n` style suffixes for variants of condition; demo options and articles left from setup; checkout may be a separate headless app behind Cloudflare; admin quick-edit bar shows on the storefront for logged-in admins; meta keywords boilerplate.

### Shopify
- **Export:** Products CSV (Admin > Products > Export), Customers CSV, Orders CSV, Discounts CSV. Pages, blog posts, navigation, metafields, redirects and theme settings aren't all in CSVs; use the Admin API (read-only custom app token) or a migration app. Theme code can be downloaded from the theme editor.
- **Addresses:** `/products/{handle}`, `/collections/{handle}`, `/collections/{c}/products/{handle}` (duplicate path, canonical points to `/products/`), `/pages/{handle}`, `/blogs/{blog}/{article}`, `/search?q=`, `/cart`, `/account`. Checkout is on Shopify's own checkout pages.
- **Images:** `cdn.shopify.com/s/files/...`; add `_2048x` style suffixes or use the original URL from the API.
- **Traps:** variants (up to the platform limit) with options; metafields hold specs; apps inject scripts that disappear when the app is gone; URL Redirects live under Navigation and export as CSV.

### BigCommerce
- **Export:** Products (Export > Bulk Edit or default template, CSV), customers, orders; API for everything else.
- **Addresses:** customizable, often `/{product-name}/` and `/{category}/`; check the store's URL settings.
- **Traps:** product options vs variants vs modifiers; custom fields; built-in 301 redirects list worth exporting.

### WordPress / WooCommerce
- **Export:** Tools > Export (WXR XML) for posts, pages, menus, custom post types; WooCommerce Products > Export (CSV); a database dump plus `wp-content/uploads` for a full copy. WP-CLI (`wp export`, `wp db export`) if there is shell access.
- **Addresses:** set by permalink settings: `/product/{slug}/`, `/product-category/{slug}/`, `/{page}/`, `/{year}/{month}/{post}/` or `/{post}/`, `?p=ID` and `?page_id=ID` always work.
- **Traps:** page builder shortcodes in content (Elementor, Divi, WPBakery) that are meaningless elsewhere; content stored in plugin tables; serialized data that breaks on naive search-replace (use `wp search-replace`).

### Magento / Adobe Commerce
- **Export:** System > Data Transfer > Export (products, customers, addresses, advanced pricing). CMS pages and blocks via API or database.
- **Addresses:** URL rewrites table maps `{key}.html` paths (often with category paths too); export it, it's your redirect source.
- **Traps:** configurable vs simple products; multiple store views (languages); attribute sets.

### Wix
- **Export:** store products CSV export; blog posts limited; no full-site export. Use the site's sitemap, the Wix store export and careful page-by-page transcription for content.
- **Addresses:** `/product-page/{slug}`, `/category/{slug}`, `/post/{slug}`, page slugs.
- **Traps:** content is rendered by JavaScript; read pages in a real browser, not with plain HTTP fetches.

### Squarespace
- **Export:** Settings > Import & Export > Export (WordPress-format XML for pages, blog, galleries, some content); products CSV from Commerce.
- **Addresses:** `/{collection}/{item-slug}`, `/{page}`, `/blog/{post}`, `?format=json` returns page data as JSON on many pages (handy, read-only).
- **Traps:** export skips some page types (product pages and some blocks); check what came out.

### Webflow
- **Export:** CMS collections export to CSV per collection; site code export (HTML/CSS/JS) on plans that allow it. Ecommerce products CSV.
- **Addresses:** `/{collection-slug}/{item-slug}`, static page slugs.
- **Traps:** interactions (animations) live in Webflow's JS; forms post to Webflow.

### Drupal, Joomla, PrestaShop, OpenCart
- Database dump is usually the most complete source. Use the platform's export modules or API where they exist.
- Old address forms (`node/123`, `index.php?option=com_content&id=`, `index.php?id_product=`, `index.php?route=product/product&product_id=`) all need redirect rules.

### Static or custom code
- Download the HTML of every address (slowly) and the assets it references; there's no export. Check the repository if the owner has it.
- Forms post somewhere: find out where (a form service, a script, an email address).

## 3. Target platforms

### WordPress + WooCommerce
- Use a maintained theme that works with the block editor (Blocksy, Kadence, GeneratePress, or a block theme) unless the owner names one. Avoid page builders if the owner asked for the block editor only.
- Custom code in a small site plugin and `mu-plugins`, never in the theme's `functions.php` for things that must survive a theme change.
- Import with WP-CLI commands you write (fast, repeatable) rather than the browser importer for large catalogs. Store the source ID as meta on every item (`_source_id`) so reruns update instead of duplicating.
- Turn on HPOS (high-performance order storage) for new WooCommerce stores.
- Global attributes (`pa_*`) for anything you filter on; brand taxonomy for brands.
- Old addresses can be served directly with rewrite rules plus server routing, or redirected. See `url-redirects.md`.
- Payment: the gateway's official plugin in sandbox mode; a local fake gateway for development.
- Email: SMTP/API plugin to a real sending service in production; Mailpit locally.

### Shopify
- Products import from CSV (one row per variant). Redirects import from CSV under Navigation > URL Redirects. Pages and blogs through the Admin API or an app.
- Theme: Online Store 2.0 theme with sections; avoid editing the theme code where settings can do it.
- Address paths are fixed (`/products/`, `/collections/`, `/pages/`), so a full redirect map is always needed from non-Shopify sources.

### Next.js / headless / static
- Pick the data source first (headless CMS, headless commerce API, markdown files).
- Redirects in `next.config.js` `redirects()`, middleware, or the host's redirect file. Large maps (thousands) belong in the CDN or a middleware lookup, not in a config array.
- Rendering: static generation for catalog pages with incremental revalidation; server rendering for search and cart.
- SEO plumbing (sitemaps, canonical, structured data, robots) is all hand-built; budget for it.

### Same platform, clean rebuild
- Copy the database to a fresh install, then remove what isn't used: plugins/apps, theme leftovers, orphaned media, old revisions, transients. Keep addresses identical.

## 4. Data mapping patterns

Write a mapping table per entity in `PLAN.md`:

| Source field | Target field | Transform | Notes |
|---|---|---|---|
| ProductCode | SKU | upper-case, trim | also store as `_source_code` |
| ProductName | Title | clean HTML, fix typos only if approved | |
| ProductPrice / SalePrice | Regular / Sale price | decimal | sale only if lower than regular |
| Description HTML | Content | strip inline styles, demote extra H1s, convert to native blocks | |
| Custom fields (amps, poles...) | Global attributes | normalize spellings, units | filterable |
| Category IDs | Category terms | keep source ID as term meta | merge duplicates only with approval |
| Photos | Featured + gallery | download originals, convert to WebP/AVIF, alt = name | placeholder when none |
| Meta title / description | SEO fields | generate where empty | |

Rules that save trouble:
- Keep every source ID on the target item. Redirects, reruns and support all need it.
- Never lose a field silently. Anything without a place goes into meta and gets listed in the plan.
- Normalize values (units, case, spacing) before making filters, or "20A", "20 A" and "20 Amp" become three filter options.
- Log rows that fail to import, with the reason, and fix the importer rather than the rows.
