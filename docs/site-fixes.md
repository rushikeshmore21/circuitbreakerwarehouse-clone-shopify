# Site fixes

Everything that was wrong on the old site, or broke during the build, and what was done. Visual layout matches live; these are code-level improvements or platform differences.

## Navigation and layout
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 1 | Phone menu was a script-moved push panel without a dialog role | Screen readers and keyboard users couldn't tell it opened; focus wasn't kept inside | Native `<dialog>` drawer: Escape closes, focus returns to the menu button, `aria-expanded` kept in sync | Fixed |
| 2 | Search field had no visible label association on phones | Unlabelled field for screen readers | Hidden `<label>` on every search input and the newsletter email field | Fixed |
| 3 | Brand logo accordion on phones used a link with `href="#brands-list"` | Not announced as a toggle | `<button aria-expanded aria-controls>` toggle | Fixed |

## Category and search pages
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 4 | Search with no results showed an empty page | Shoppers saw nothing and didn't know why | "No products found for ..." message announced as a status | Fixed |
| 5 | Category pages had no H1 in the HTML (title drawn later) | Search engines and screen readers missed the page heading | Real `<h1>` with the category title | Fixed |
| 6 | No breadcrumb structured data | Lost breadcrumb rich results | `BreadcrumbList` JSON-LD on category, search and product pages | Fixed |
| 7 | Sort/per-page/page controls needed JavaScript | Broke without JS | Plain GET forms; JS only auto-submits the per-page select | Fixed |

## Product pages
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 11 | Spec label typo "Amprage" and "Availability::" | Looked careless | "Amperage" and "Availability:" | Fixed |
| 12 | "Larger Photo" used the Shadowbox jQuery lightbox | Extra script weight; plugin focus handling | Native `<dialog>` with every product image; Escape and backdrop close it, no plugin | Fixed |
| 13 | Product microdata only | Weaker rich results | Shopify `structured_data` JSON-LD (Product/Offer) plus BreadcrumbList | Fixed |
| 14 | Related products depended on a Volusion setting | n/a | Shopify recommendations; falls back to the product's first collection while the store has no recommendation data | Fixed |

## Content, contact, cart and system pages
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 15 | Contact page had two H1s ("Please fill out..." and "OR") and a third-party Wufoo form | Heading structure; form depended on Wufoo | One H1; Shopify native contact form (owner decision) with labels and error/success messages | Fixed |
| 16 | Missing pages returned a bare server "page cannot be found" screen with no navigation | Visitors from old links hit a dead end | Themed 404 with header, footer, part-number search and a home link | Fixed |
| 17 | Empty cart text was an H1 next to the page heading | Two H1s | Empty text is a paragraph | Fixed |

## Round 2 (2026-11-10, owner notes)
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 18 | Sticky header missing | Live header pins after scrolling | Desktop (992px+) sticky header: logo row collapses with a 0.2s transition, search moves into the grey bar, nav stays; phones scroll normally like live | Fixed |
| 19 | Live sticky header shrinks its placeholder from 220px to 90px, so the page jumps 130px when it pins | Layout shift while scrolling | Placeholder keeps the full header height, so nothing below moves | Fixed |
| 20 | Cart popup sat at the top of the page, off-screen once scrolled | Shoppers didn't see the add-to-cart confirmation | Popup lives inside the header and travels with the sticky header | Fixed |
| 21 | Product Index pager lists every page number (82 links) | Long, hard to scan | Shopify's page list with ellipses ("1 2 3 ... 82"); 200 products per page as on live | Fixed |
| 22 | Category Index is built by Volusion from categories and articles | n/a | Lists every collection plus a chosen menu (default main menu) A to Z in two columns | Fixed |
| 23 | Cart used Dawn's default layout | Didn't match the live cart | Owner approved one test add to the live cart (FHP16080, removed right after). Rebuilt the cart from it: ITEM DESCRIPTION / EACH / QTY / TOTAL table, red remove icon, Empty My Cart, coupon box with Apply, Recalculate, Calculate Shipping (country, state, zip, Get Shipping Options), Tax and Total, red PROCEED TO CHECKOUT pill, express buttons; stacked layout on phones as on live | Fixed |
| 25 | Live Add To Cart reloads into the cart page | n/a | Same: theme cart type set to "page", so Add To Cart goes to the cart (the earlier popup is off) | Matched |
| 26 | Coupon box kept invalid codes on the cart | A bad code could block a later valid one | Apply sends kept valid codes plus the new one to `cart/update.js`; a rejected code is dropped and an error message is announced | Fixed |
| 24 | Dawn analytics page-view event had an empty template name on policy pages (console error) | Error in the console; event dropped | Layout passes `request.page_type` when there's no template name | Fixed |

## SEO and speed
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 8 | 32 of 42 sampled pages had H1 count other than 1 | Weak page structure | One H1 per template (home H1 kept visually hidden, as on live) | Fixed |
| 9 | Images without width/height or responsive sizes; jQuery 3.7 + migrate on every page | Layout shift and extra bytes | `image_url` + `image_tag` with widths/sizes, lazy below the fold, hero `fetchpriority=high`; no jQuery | Fixed |
| 10 | Webfont served as EOT/TTF/SVG/WOFF2 sets from the template | Extra requests | WOFF2 only, `font-display: swap`, main weight preloaded | Fixed |

## Platform differences (Shopify can't do it the same way)
| # | Live behavior | Shopify behavior | Status |
|---|---|---|---|
| P1 | Sort by Manufacturer and Availability | Not native sort options; omitted. Other sorts (price, most popular, title, newest, oldest) kept with live labels | Platform limit |
| P2 | 320 per page (categories), 300/500 per page (search) | Shopify paginates at most 250 per page; those options dropped. Per-page uses `?view=` alternate templates | Platform limit |
| P3 | Volusion login / My Account pages | Shopify-hosted customer accounts (legacy theme templates are deprecated); owner chose not to match them | Owner decision |
| P4 | Live home grid shows a random product selection each load | Shopify pages are cached; grid shows the chosen collection in its sort order | Platform limit |
| P6 | Become an Affiliate is a Volusion affiliate login screen | Shopify has no built-in affiliate program; the page uses the normal page template until an affiliate app is chosen | Platform limit |
| P7 | Terms, Privacy, Return / Exchange are Volusion articles | Shopify policy pages (`/policies/...`), styled like the content pages; text comes from Settings > Policies | Platform difference |
| P8 | Cart shows "Tax: $0.00" | Shopify calculates tax at checkout; the cart shows "Calculated at checkout" | Platform difference |
| P9 | PayPal "As low as $x/mo" pay-later line and PayPal button | Express buttons come from Shopify (`content_for_additional_checkout_buttons`) and appear once PayPal or Shop Pay is enabled; no pay-later line | Platform difference |
| P5 | Phone search placeholder reads "Search..." | Same placeholder "Search our store..." at every width | Open (minor) |

## Problems found during the build
| # | What broke | What we did | Status |
|---|---|---|---|
| B1 | Skill's `screenshots.mjs` crashed on tall phone pages (WebP can't encode > 16,383 px) | Added per-shot `"format": "jpeg"` option | Fixed |
| B2 | Shopify Liquid skill's `validate.mjs` needs npm packages that aren't installed | Validated with `shopify theme check` (same theme-check engine, CLI 4.8.3) | Workaround |
| B3 | Search breadcrumb showed `&quot;` | Translation output is already escaped; breadcrumb uses `escape_once` | Fixed |
| B5 | Shopify rejected `templates/product.json` linking spec rows to metafields that have no definition yet | Spec rows take a metafield key (e.g. `custom.type`) and read it directly; rows hide when empty | Fixed |
| B6 | Cart popup had no background | Passed Dawn's `scheme-1` color scheme to the cart notification | Fixed |
| B7 | `shopify theme dev` uploaded `templates/404.json` before its new section file and showed "Failed to Upload" | Re-saved the template after the section uploaded | Fixed |
| B4 | Section CSS isn't loaded on pages that don't render that section (Shopify stylesheet subsetting) | Shared listing grid CSS moved into the `cbw-listing-grid` snippet | Fixed |
