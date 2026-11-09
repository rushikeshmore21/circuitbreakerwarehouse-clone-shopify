# Feature inventory: circuitbreakerwarehouse.com (2026-11-10)

| Area | Feature | Found? | Where | Behavior | Data / service | Target plan (Shopify) | Status |
|---|---|---|---|---|---|---|---|
| Global | Top bar text | yes | all | Static centered line | Volusion article | Section `cbw-top-bar`, text setting | built |
| Global | Utility bar: free shipping, phone, flags | yes | all, desktop only | Links: shipping article, `tel:`; 4 flag SVGs all link to the free-shipping article (not a language switcher) | static | Part of `cbw-header`, settings for text/phone/link | built |
| Global | Logo | yes | all | Links home | `header_bg.png` 600x203 | `settings.logo` / header image setting | built |
| Global | Search box | yes | all | GET `searchresults.php?Search=` | Volusion search | Shopify `/search` form (`routes.search_url`), Dawn predictive search kept | built |
| Global | Cart button "CART:n" | yes | all | Links to cart, shows count | session cart | `cart.item_count`, Dawn cart bubble updates | built |
| Global | Main nav (5 links) | yes | desktop | Horizontal bar, full width | Volusion menu | `linklists` menu setting (`main-menu`) | built |
| Global | Phone menu "Shop Our Categories" | yes | phone | Slide-in panel | menu | Drawer in `cbw-header` (`<details>`), manufacturers + main menu | built |
| Global | Left sidebar | yes | home, category, search, product | Manufacturers menu, cards image, mailing list, seals | menu, Volusion mailing list | Snippet `cbw-sidebar` driven by theme settings; newsletter via Shopify `customer` form | built |
| Global | Mailing list signup | yes | sidebar | POST `MailingList_subscribe.php` | Volusion | Shopify `{% form 'customer' %}` (marketing consent) | built |
| Global | Footer: helpful links, stay connected, disclaimer, copyright, card marks | yes | all | Static | Volusion | `cbw-footer` section: two menus, social links, rich text disclaimer, payment icons | built |
| Global | Volusion SSL seals / "Ecommerce Software by Volusion" | yes | sidebar, footer | Links to volusion.com verification | Volusion | Owner decision (Round 4) | built (owner decision) |
| Global | buySAFE / Norton Shopping Guarantee seal | yes | all (fixed bottom-left), cart (bar) | Script `seal.buysafe.com` with store hash | buySAFE account | Owner decision (Round 4) | built (owner decision) |
| Global | "Leave a Message / E_MAIL" tab | yes | all (fixed right) | Third-party widget `d10lpsik1i8c69.cloudfront.net/w.js` in an iframe | Lucky Orange (analytics/chat, cdn d10lpsik1i8c69) | Same-look tab linking to Contact | built (owner decision) |
| Global | Back-to-top button | yes | all | Smooth scroll to top | none | Small snippet with native `href="#"` | built |
| Global | GTM, Clarity, Cloudflare insights | yes | all | Tracking | GTM-NXZLRVJ6, Clarity yfsljd2zxq | Not cloned (owner decision) | skipped |
| Home | Hero banner (desktop + mobile art) | yes | home | Static image with srcset | `/v/images/homepage/home-banner-*.jpg` | `cbw-hero` section: desktop + mobile image pickers, link | built |
| Home | Featured grid 16 products | yes | home | 4x4, selection varies per load | Volusion featured | `cbw-featured-products` with collection picker | built |
| Home | Shop with Confidence band | yes | home | Text, 2 buttons, 4 guarantees | static | `cbw-confidence` section with blocks | built |
| Home | Brand logo grid / phone accordion | yes | home | 8 logos linking to categories; collapsible on phone | static | `cbw-brands` section, blocks (image + link), `<details>` on phone | built |
| Home | Outage/Emergency callout | yes | home | Static red text | static | `cbw-callout` section (rich text) | built |
| Listing | Breadcrumb | yes | category, search, product | "Circuit Breaker Warehouse > Home > X" | | `cbw-breadcrumb` snippet + BreadcrumbList schema | built |
| Listing | Sort select + GO | yes | category, search | Price low-high default | | `collection.sort_options`, `sort_by` param; GO submits form | built |
| Listing | Per-page select (32/50...) | yes | category, search | Changes page size | | Alternate templates via `?view=` (Liquid can't read arbitrary query params) | built |
| Listing | Page N of M jump + NEXT | yes | category, search | Jump box + next button | | `paginate` object, GET form with `page` | built |
| Listing | Card prices: Our Price / Sale Price / You Save | yes | all grids | Sale label green highlight | price, sale price | `compare_at_price` = Our Price, `price` = Sale Price | built |
| Listing | Free shipping icon on card | yes | grids | Small box icon | product flag | Shown for all products (all orders ship free) | built |
| Listing | "Subject to availability" | yes | category | Static text | | Snippet text | built |
| Product | Image + "Larger Photo" popup | yes | product | Opens bigger image | photos | Native `<dialog>` with larger image | built |
| Product | Illustrative-image disclaimer | yes | product | Red italic | static | Locale string | built |
| Product | 5 Reasons list | yes | product | Static ordered list | static | Block setting (richtext) | built |
| Product | Spec lines Condition/Type/Pole/Amperage/Voltage | yes | product | Label: value | product fields | Metafields `custom.type`, `custom.poles`, `custom.amperage`, `custom.voltage`; condition from metafield or `New`/`Refurbished` tag | built |
| Product | Product code | yes | product | Bold italic | SKU | `variant.sku` | built |
| Product | Qty + Add to cart | yes | product | Server cart | | Dawn `product-form` JS, restyled | built |
| Product | Add to Wishlist | yes | product | Volusion wishlist (account) | Volusion | No native wishlist in Shopify: owner decision | built (owner decision) |
| Product | Description tab | yes | product | Bordered box | description | `product.description` | built |
| Product | Related products (8) | yes | product | Same category | | Shopify product recommendations (`related`) | built |
| Product | Reviews prompt | yes | product | "Be the first to write a review" | Volusion reviews (none seen) | No native reviews: owner decision | built (owner decision) |
| Product | "Browse same category" links | yes | product | Category links | | `product.collections` | built |
| Product | Recent Items + history off/clear | yes | product | Recently viewed (cookie) | | Small JS with `localStorage`, toggle + clear | built |
| Product | Microdata Product/Offer | yes | product, grids | | | JSON-LD via `structured_data` filter | built |
| Content | About, FAQ, Free shipping, Help | yes | pages | Rich text | Volusion articles | `page` template restyle; Help page as link-columns section | built |
| Content | Contact form | yes | contact | Wufoo embed | Wufoo | Owner decision (Round 4) | built (owner decision) |
| Cart | Cart page (empty state seen) | yes | cart | "Shopping Cart", SHOP FOR MORE ITEMS, buySAFE bar, "Your Cart", empty message | | Dawn cart restyled; filled state needs a reference (Round 4) | built (owner decision) |
| Accounts | Login / My Account | yes | login.php | Email-first login, new customer button | Volusion | Shopify new customer accounts are hosted by Shopify and not theme templates (docs: legacy customer templates deprecated) | platform limit |
| Search | Results grid, sort, per-page, pager | yes | search | Same as category | | `cbw-main-search` | built |
| Search | Empty results | yes | search | Shows nothing at all | | Show "no results" message (fix) | built |
| System | 404 | yes | any | Bare server page "The page cannot be found" | | Themed 404 with header/footer and search (fix) | built |
