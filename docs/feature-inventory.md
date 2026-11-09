# Feature inventory: circuitbreakerwarehouse.com (2026-11-10)

| Area | Feature | Found? | Where | Behavior | Data / service | Target plan (Shopify) | Status |
|---|---|---|---|---|---|---|---|
| Global | Top bar text | yes | all | Static centered line | Volusion article | Section `cbw-top-bar`, text setting | planned |
| Global | Utility bar: free shipping, phone, flags | yes | all, desktop only | Links: shipping article, `tel:`; 4 flag SVGs all link to the free-shipping article (not a language switcher) | static | Part of `cbw-header`, settings for text/phone/link | planned |
| Global | Logo | yes | all | Links home | `header_bg.png` 600x203 | `settings.logo` / header image setting | planned |
| Global | Search box | yes | all | GET `searchresults.php?Search=` | Volusion search | Shopify `/search` form (`routes.search_url`), Dawn predictive search kept | planned |
| Global | Cart button "CART:n" | yes | all | Links to cart, shows count | session cart | `cart.item_count`, Dawn cart bubble updates | planned |
| Global | Main nav (5 links) | yes | desktop | Horizontal bar, full width | Volusion menu | `linklists` menu setting (`main-menu`) | planned |
| Global | Phone menu "Shop Our Categories" | yes | phone | Slide-in panel | menu | Drawer in `cbw-header` (`<details>`), manufacturers + main menu | planned |
| Global | Left sidebar | yes | home, category, search, product | Manufacturers menu, cards image, mailing list, seals | menu, Volusion mailing list | Snippet `cbw-sidebar` driven by theme settings; newsletter via Shopify `customer` form | planned |
| Global | Mailing list signup | yes | sidebar | POST `MailingList_subscribe.php` | Volusion | Shopify `{% form 'customer' %}` (marketing consent) | planned |
| Global | Footer: helpful links, stay connected, disclaimer, copyright, card marks | yes | all | Static | Volusion | `cbw-footer` section: two menus, social links, rich text disclaimer, payment icons | planned |
| Global | Volusion SSL seals / "Ecommerce Software by Volusion" | yes | sidebar, footer | Links to volusion.com verification | Volusion | Owner decision (Round 4) | open |
| Global | buySAFE / Norton Shopping Guarantee seal | yes | all (fixed bottom-left), cart (bar) | Script `seal.buysafe.com` with store hash | buySAFE account | Owner decision (Round 4) | open |
| Global | "Leave a Message / E_MAIL" tab | yes | all (fixed right) | Third-party widget `d10lpsik1i8c69.cloudfront.net/w.js` in an iframe | unknown vendor | Owner decision (Round 4) | open |
| Global | Back-to-top button | yes | all | Smooth scroll to top | none | Small snippet with native `href="#"` | planned |
| Global | GTM, Clarity, Cloudflare insights | yes | all | Tracking | GTM-NXZLRVJ6, Clarity yfsljd2zxq | Not cloned (owner decision) | skipped |
| Home | Hero banner (desktop + mobile art) | yes | home | Static image with srcset | `/v/images/homepage/home-banner-*.jpg` | `cbw-hero` section: desktop + mobile image pickers, link | planned |
| Home | Featured grid 16 products | yes | home | 4x4, selection varies per load | Volusion featured | `cbw-featured-products` with collection picker | planned |
| Home | Shop with Confidence band | yes | home | Text, 2 buttons, 4 guarantees | static | `cbw-confidence` section with blocks | planned |
| Home | Brand logo grid / phone accordion | yes | home | 8 logos linking to categories; collapsible on phone | static | `cbw-brands` section, blocks (image + link), `<details>` on phone | planned |
| Home | Outage/Emergency callout | yes | home | Static red text | static | `cbw-callout` section (rich text) | planned |
| Listing | Breadcrumb | yes | category, search, product | "Circuit Breaker Warehouse > Home > X" | | `cbw-breadcrumb` snippet + BreadcrumbList schema | planned |
| Listing | Sort select + GO | yes | category, search | Price low-high default | | `collection.sort_options`, `sort_by` param; GO submits form | planned |
| Listing | Per-page select (32/50...) | yes | category, search | Changes page size | | Alternate templates via `?view=` (Liquid can't read arbitrary query params) | planned |
| Listing | Page N of M jump + NEXT | yes | category, search | Jump box + next button | | `paginate` object, GET form with `page` | planned |
| Listing | Card prices: Our Price / Sale Price / You Save | yes | all grids | Sale label green highlight | price, sale price | `compare_at_price` = Our Price, `price` = Sale Price | planned |
| Listing | Free shipping icon on card | yes | grids | Small box icon | product flag | Shown for all products (all orders ship free) | planned |
| Listing | "Subject to availability" | yes | category | Static text | | Snippet text | planned |
| Product | Image + "Larger Photo" popup | yes | product | Opens bigger image | photos | Native `<dialog>` with larger image | planned |
| Product | Illustrative-image disclaimer | yes | product | Red italic | static | Locale string | planned |
| Product | 5 Reasons list | yes | product | Static ordered list | static | Block setting (richtext) | planned |
| Product | Spec lines Condition/Type/Pole/Amperage/Voltage | yes | product | Label: value | product fields | Metafields `custom.type`, `custom.poles`, `custom.amperage`, `custom.voltage`; condition from metafield or `New`/`Refurbished` tag | planned |
| Product | Product code | yes | product | Bold italic | SKU | `variant.sku` | planned |
| Product | Qty + Add to cart | yes | product | Server cart | | Dawn `product-form` JS, restyled | planned |
| Product | Add to Wishlist | yes | product | Volusion wishlist (account) | Volusion | No native wishlist in Shopify: owner decision | open |
| Product | Description tab | yes | product | Bordered box | description | `product.description` | planned |
| Product | Related products (8) | yes | product | Same category | | Shopify product recommendations (`related`) | planned |
| Product | Reviews prompt | yes | product | "Be the first to write a review" | Volusion reviews (none seen) | No native reviews: owner decision | open |
| Product | "Browse same category" links | yes | product | Category links | | `product.collections` | planned |
| Product | Recent Items + history off/clear | yes | product | Recently viewed (cookie) | | Small JS with `localStorage`, toggle + clear | planned |
| Product | Microdata Product/Offer | yes | product, grids | | | JSON-LD via `structured_data` filter | planned |
| Content | About, FAQ, Free shipping, Help | yes | pages | Rich text | Volusion articles | `page` template restyle; Help page as link-columns section | planned |
| Content | Contact form | yes | contact | Wufoo embed | Wufoo | Owner decision (Round 4) | open |
| Cart | Cart page (empty state seen) | yes | cart | "Shopping Cart", SHOP FOR MORE ITEMS, buySAFE bar, "Your Cart", empty message | | Dawn cart restyled; filled state needs a reference (Round 4) | open |
| Accounts | Login / My Account | yes | login.php | Email-first login, new customer button | Volusion | Shopify new customer accounts are hosted by Shopify and not theme templates (docs: legacy customer templates deprecated) | platform limit |
| Search | Results grid, sort, per-page, pager | yes | search | Same as category | | `cbw-main-search` | planned |
| Search | Empty results | yes | search | Shows nothing at all | | Show "no results" message (fix) | planned |
| System | 404 | yes | any | Bare server page "The page cannot be found" | | Themed 404 with header/footer and search (fix) | planned |
