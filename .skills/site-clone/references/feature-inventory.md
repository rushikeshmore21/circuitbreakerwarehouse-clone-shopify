# Feature inventory checklist

Go through every row during the scan (Phase 2) and again during QA (Phase 8). For each row record: **Found?** (yes / no / unsure) · **Where** (page types) · **How it behaves** · **Data / settings it needs** · **Service behind it** · **Plan on target** · **Status**.

Save the result as `docs/feature-inventory.md` with this header:

```markdown
| Area | Feature | Found? | Where | Behavior | Data / service | Target plan | Status |
|---|---|---|---|---|---|---|---|
```

"Unsure" rows become owner questions. A feature with "no sign of use" (an empty wishlist, an affiliate program with no signups) still gets a row; the owner decides.

## Contents
1. Global layout
2. Navigation and search
3. Catalog listing
4. Product page
5. Cart
6. Checkout
7. After checkout
8. Accounts
9. Content
10. Forms and engagement
11. Marketing and tracking
12. SEO plumbing
13. Accessibility
14. Commerce rules and settings
15. Operations and integrations
16. Admin-side features the owner relies on
17. Legal and trust

---

## 1. Global layout
- Announcement bar (text, links, rotating?, dismissible?)
- Utility bar (phone, hours, shipping message, language/currency switch, login link)
- Header: logo (size, link), search box, cart button (count format, e.g. "CART: 3"), account link
- Main navigation, mega menu, dropdowns, phone menu (off-canvas?)
- Sticky header (what shrinks, at what scroll point)
- Sidebar (which pages, which widgets)
- Footer columns, social links, newsletter, payment marks, seals, copyright
- Floating: back-to-top, chat tab, message tab, popups, cookie banner
- Favicon, app icons, theme color
- Container width, breakpoints, print styles

## 2. Navigation and search
- Breadcrumbs (format, schema)
- Search: box placement, suggestions as you type, exact-code jump to product, partial code, typo tolerance, empty search, no results page
- Category index page, product index page, HTML sitemap
- 404 page content and search box
- Language or region selector

## 3. Catalog listing
- Category page layout: title placement, description (top/bottom), banner, subcategories
- Grid columns per width, card contents (image, name, prices, badges, buttons, stock text)
- Sort options and default sort
- Per-page options
- Pagination style (numbers, next/prev, "page N of M", jump box, load more, infinite)
- Filters / facets (which attributes, multi-select, counts, long lists)
- Featured, specials, new arrivals, best sellers collections
- Brand pages
- Compare products
- Quick view

## 4. Product page
- Title format, SKU/code display, brand
- Images: gallery, zoom, "larger photo" link, placeholder when missing
- Prices: regular, sale, list/MSRP, "you save" amount and percent, tiered/quantity pricing, "call for price"
- Stock: in stock, backorder text, low stock, out of stock behavior, "subject to availability"
- Variants/options and how they change price, SKU, image
- Quantity box, min/max quantity
- Add to cart, buy now, express buttons on product page
- Wishlist, share, print, email-a-friend
- Attributes/specs table, tabs (description, specs, shipping, reviews)
- Selling points block ("5 reasons to buy"), guarantees, shipping message
- Related, upsell, cross-sell products (how many, logic)
- Reviews and ratings, Q&A
- Sticky add-to-cart on phones
- Downloads (datasheets, manuals)
- Structured data (Product, Offer, AggregateRating, Brand)

## 5. Cart
- Cart page vs drawer vs mini-cart
- Line items: image, name, options, unit price, quantity edit, remove, line total
- Empty cart button, continue shopping link
- Coupon field, gift card field
- Shipping estimator (countries, state, ZIP), shown rates
- Tax line, totals
- Free-shipping progress message
- Cross-sells
- Saved cart / abandoned cart recovery
- Cart count in header after add (AJAX or reload)

## 6. Checkout
- One page or steps; step names
- Guest checkout, login prompt, account creation option
- Fields (required/optional), company, apartment line, phone, address lookup/autocomplete, country and state lists (military states?)
- Ship to different address
- Shipping methods: live carrier rates, flat, free threshold, excluded regions, local pickup, delivery dates
- Payment: cards (gateway, iframe vault), PayPal, pay later, Apple/Google Pay, purchase orders, net terms, check/COD
- Promo code, gift card, store credit
- Order notes, gift message, gift wrap, "is a gift" flag
- Terms checkbox, newsletter opt-in
- Fraud tools, CAPTCHA on checkout
- Distraction-free layout (logo only)
- Tax calculation display

## 7. After checkout
- Thank-you page content, order number format
- Order confirmation email (wording, logo, sender)
- Account creation offer for guests
- Shipping confirmation with tracking, delivery email
- Review request emails, follow-ups, guarantees enrolment (e.g. purchase protection services)
- Conversion tracking events (ads, analytics purchase event)
- Drop-ship vendor notification
- Invoices/packing slips

## 8. Accounts
- Register, login, logout, password reset (email wording)
- Dashboard, order history, order detail, re-order
- Addresses, saved cards (tokenized only)
- Wishlist
- Affiliate area, wholesale tier, reward points
- Newsletter preferences
- Account deletion / data request

## 9. Content
- About, contact, FAQ, help center, returns, shipping, terms, privacy, accessibility statement
- Blog list, posts, categories, tags, authors, comments
- Landing pages, campaign pages
- Placeholder or demo content still live (flag for removal)
- Embedded media: video, maps, PDFs

## 10. Forms and engagement
- Contact form (fields, recipients, autoresponder, spam protection)
- Quote request, RMA/return request
- Mailing list signup (provider, double opt-in, where shown)
- Popups (trigger, frequency, content)
- Live chat or "leave a message" widget
- Back-in-stock alerts, price drop alerts
- Surveys, polls

## 11. Marketing and tracking
- Tag manager container, analytics property, ads conversion IDs, remarketing
- Heatmaps / session recording
- Affiliate tracking parameters
- Product feeds (Google Merchant, Bing, marketplaces)
- UTM handling (kept across redirects?)
- Coupons and promotions schedule
- Email platform integrations

## 12. SEO plumbing
- Title and meta description patterns per page type
- Canonical tags, Open Graph, Twitter cards
- Structured data per page type (Organization/LocalBusiness, WebSite + SearchAction, BreadcrumbList, Product, FAQPage, Article)
- XML sitemaps (split, image sitemap), robots.txt rules (including AI crawler policy)
- noindex on search, cart, account, thin pages
- hreflang, pagination tags
- Existing redirects the platform already does
- Verification meta tags (Search Console, Bing, Pinterest, domain verification)

## 13. Accessibility
- Skip link, landmarks, heading order, one H1
- Labels on every field, error messages tied to fields
- Keyboard use of menus, filters, popups, galleries
- Visible focus, contrast, reduced motion
- Tap targets 24px minimum on phones, no sideways scroll
- Alt text, link names, language attribute

## 14. Commerce rules and settings
- Tax rules and rates, tax-exempt customers
- Shipping zones, rates, carriers, packaging, weights and dimensions
- Currency, rounding, price display (incl./excl. tax)
- Inventory tracking, backorders, stock thresholds
- Coupons: active ones, limits, expiry
- Order statuses and the workflow staff follows
- Returns policy, restocking fees, RMA process

## 15. Operations and integrations
- Accounting (QuickBooks, Xero), ERP, POS, warehouse
- Shipping label tools
- Vendor/drop-ship rules, purchase orders
- Customer service tools (helpdesk, chat)
- Email sending service, sender domain
- Backups, uptime monitoring
- Staff accounts and roles

## 16. Admin-side features the owner relies on
- Reports they check weekly
- Bulk edit and import routines
- Order search, printing, exports
- Abandoned cart lists
- Anything they'd be upset to lose. Ask directly.

## 17. Legal and trust
- Cookie consent and which tags wait for consent
- Privacy policy, terms, refund policy, shipping policy
- Trust seals (SSL badge, guarantee programs), payment marks
- Business address, phone, hours (consistent everywhere?)
- Regional rules (GDPR, CCPA, accessibility laws, sales tax nexus)
