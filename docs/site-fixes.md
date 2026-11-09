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
