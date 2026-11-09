# Site scan: circuitbreakerwarehouse.com  (2026-11-10, read-only: GET and screenshots only)

## 1. Fingerprint
- Platform: Volusion (`x-powered-by: Volusion`), template `capelec` (`/v/vspfiles/templates/capelec/css/template.css`).
- Server/CDN: Cloudflare (`cf-ray`), HSTS. No bot challenge on GETs at 1 req/s.
- Sitemap: 16,249 URLs in one file: 10,954 `/{name}-p/{code}.htm` (refurbished), 5,267 `/{name}-p/{code}-n.htm` (new), 22 categories, 3 articles, 2 `.asp` system pages, home.
- Old `.asp` addresses 307 to `.php` (e.g. `Articles.asp?ID=243` -> `Articles.php?ID=243`).
- Raw output: `docs/scan/fingerprint.json`, `docs/scan/urls.txt`, `docs/scan/crawl.jsonl`.

## 2. Inventory
| Type | Count | Address pattern | Notes |
|---|---|---|---|
| Home | 1 | `/` | |
| Category | 22 | `/category-s/{id}.htm`, `/{Name}-s/{id}.htm` | 16 manufacturer categories in sidebar + Featured Products (34), Specials (12), sub-categories 42, 73, 74, 78 |
| Product, refurbished | 10,954 | `/{name}-p/{code}.htm` | |
| Product, new | 5,267 | `/{name}-p/{code}-n.htm` | New condition is a separate product with `-N` code suffix |
| Articles | 4 | `Articles.php?ID=` 242 About, 243 Contact, 252 FAQ; `articles.php?ID=57` Free shipping | |
| System | | `help.php`, `myaccount.php` (-> login), `login.php`, `shoppingcart.php`, `searchresults.php?Search=` | |

## 3. Page types

### Global (every page)
Desktop 1440px, top to bottom:
1. **Top bar** (`.ct-aio-bar`, 39px, light grey): centered text "16K+ New, Refurbished & Hard-to-Find Breaker Part Numbers".
2. **Utility bar** (40px, light grey): left "FREE SHIPPING on All Orders!" (link to free-shipping article) + "Call Today! (888) 367-7700" (tel link, number in navy bold); right four flag icons (AU, DE, JP, UK).
3. **Header** (130px, white): logo left (CBW mark + "Circuit Breaker Warehouse"); right: search box "Search our store..." with red magnifier, red "CART:0" button with cart icon.
4. **Nav bar** (50px, blue `#3a8ed0`-ish): About Us, Contact Us, F.A.Q., Help, My Account, uppercase white, divided by vertical lines, items spread across the container.
5. Content area: container ~1170px. Left sidebar (~290px) on home, category and most content pages: "MANUFACTURERS" blue header + bordered list of 16 manufacturer links; payment cards image; "Join our mailing list!" email field + navy "JOIN NOW" button; "Certified Secure Site / SSL" seal; "SSL volusion secure site" badge.
6. **Footer** (grey `#e3e3e3`): "HELPFUL LINKS" in two columns (About Us, Become an Affiliate, Privacy Policy, Contact Us, Bookmark Us, Company Info | Advertising, Product Index, Category Index, Help, Terms of Use, Return / Exchange); "STAY CONNECTED" (Facebook, Google+ with round icons); "DISCLAIMER" panel (lighter box): AK/HI free-shipping note, cut-off time 12:00 (Noon) Pacific, in-stock pricing note, hours Mon-Fri 8:00 AM - 4:00 PM Pacific.
7. **Bottom bar**: "© Copyright 2026 Circuit Breaker Warehouse. All Rights Reserved. Ecommerce Software by Volusion" + payment marks (VISA, AMEX, DISCOVER, MasterCard, PayPal, SSL volusion).
8. Floating: Norton/buySAFE shopping guarantee seal (fixed bottom-left, with today's date), "Leave a Message / E_MAIL: Support@CircuitBreakerWarehouse.com" tab (fixed right, black), scroll-to-top button (fixed bottom-right).

Phone 390px: top bar text wraps to two lines; utility bar hidden; logo centered full width; row of search field + phone icon + cart icon with count + hamburger; nav moves into the hamburger; sidebar hidden; footer stacks centered.

Font: `cooper_hewitt` (500/600/700) self-hosted by the template, body 16px `#484848`. Headings navy `#080375`. Links/accent red `#d42400`. Blue `#00009f` for "Our Price" labels.

### Home
Desktop:
1. Hero banner image full width (~1440x330): "New & Reconditioned", four feature boxes (Free Shipping, Outstanding Customer Service, Competitive Prices, Secure Shopping), phone "+1(310)793-4000", brand strip (SIEMENS, EATON, GE, FEDERAL PIONEER, WESTINGHOUSE, CUTLER-HAMMER, ZINSCO) along the bottom.
2. Two columns: sidebar (see Global) + product grid, 4 columns x 4 rows (16 products, a different selection per load). Card: image, title (2-3 lines, small), "Our Price: $X" (label navy bold), "Sale Price: $Y" (label on bright green highlight), "You Save $Z!" (red bold italic), free-shipping box icon.
3. "Shop with Confidence" band (lavender `#ebebff`-ish background): H2 navy, two paragraphs, red pill buttons READ MORE and CONTACT US; right column four guarantees with navy icons (ID THEFT PROTECTION, PURCHASE GUARANTEE, LOWEST PRICE GUARANTEE, 100% SATISFACTION GUARANTEE).
4. Brand logo grid 3 columns (GE, Siemens, Zinsco, FPE, Cutler-Hammer, ITE, Westinghouse, Eaton), grey logos with thin dividers.
5. "Outage or Emergency? Call 424-888-CBW8" red bold, centered.
6. Footer.

Phone: hero swaps to a short mobile banner; 2-column grid; Shop with Confidence stacks with full-width red buttons and centered guarantees; brand grid becomes a red "Shop Popular Brands +" accordion.

H1 is visually hidden ("Circuit Breaker Warehouse: New & Reconditioned Circuit Breakers").

### Category (e.g. `/category-s/66.htm` Siemens)
Desktop: sidebar left; right column: breadcrumb "Circuit Breaker Warehouse > Home > Siemens Circuit Breakers"; title "Siemens Circuit Breakers" (large, grey); toolbar: "Sort By:" select (Price: Low to High default) + navy GO button; per-page select (32 per page); "Page [1] of 83" jump box + navy NEXT button. Grid 4 columns, 32 per page; card centered: image, title, Our Price / Sale Price / You Save, "Subject to availability". Bottom: NEXT button right.

### Product (e.g. `/Square-D-FHP16080-p/fhp16080.htm`)
Desktop: sidebar left; right column:
1. Breadcrumb "Home > Square D Circuit Breakers >".
2. H1 product name (large, grey, 2 lines).
3. Two columns. Left: main image (~300px), red italic note "* Images are for illustrative purposes only & may differ from the actual product.", "Larger Photo" link with zoom icon (opens popup). Right: "5 Reasons to Shop CBW:" ordered list (Best Customer Service, Price Matching, Free Shipping in USA, 3 year Warranty, 100% Satisfaction Guarantee; 1, 3 and 5 bold); "Our Price: $268.00" (blue bold); "Sale Price: $242.00" (green-highlighted label); "You Save $26.00!" (red); spec lines Condition, Type, Pole, Amperage, Voltage (bold label: value); free-shipping box icon + "This product ships free"; "Availability:: Subject to availability"; "Product Code: FHP16080" (bold italic); "Qty: [1]"; red pill "ADD TO CART"; red "+ Add To Wishlist".
4. "Description" tab (navy tab) over a navy-bordered box: H2 "{code} Product Details and Specifications", bullet list (Manufacturer, Catalog # in red, Type, Poles, Amps, Voltage), "{code} Specifications:" paragraph (upper-case spec text), "Condition:" paragraph.
5. "Related Products..." 4 columns x 2 rows: title, price line, small image under the text.
6. "Share your knowledge of this product with other customers... Be the first to write a review" (red link).
7. "Browse for more products in the same category as this item:" + category links (red).
8. "Recent Items" with "TURN HISTORY OFF" navy pill and "Clear All" (recently viewed products).
Microdata: Product + Offer.

### Content pages (About `ID=242`, FAQ `ID=252`, Free shipping `ID=57`)
Full width, no sidebar. Page title top-left (~32px, grey, "About us" / "FAQ"), then rich text: paragraphs, bold labels, bullet lists, red phone link. FAQ is question (bold) + answer paragraphs. In Shopify these are `page` content edited in admin; the template only provides the title + rich text frame.

### Contact (`ID=243`)
"Contact Us" small bold title; centered stock photo (woman with headset); H1 "Please fill out the form below and click submit"; "OR"; "E-mail To: Support@CircuitBreakerWarehouse.com" (blue italic link); a Wufoo form embed (`wufoo.com`, did not render headless). Footer on this page is boxed inside the container (markup bug on live).
