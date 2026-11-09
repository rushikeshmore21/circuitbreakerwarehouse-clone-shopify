# Intake questions

Ask in rounds, not all at once. A wall of 80 questions gets skimmed; four at a time get real answers. Each question below has a default, so the user can say "use the defaults" and you still have an answer to build on. Mark which answers were defaults in `PROJECT.md`, because those are the ones to confirm before launch.

Don't ask what you can see for yourself (the platform, the page count, whether there's a blog). Do ask anything only the owner knows: intent, accounts, money, legal, what's actually in use.

## Contents

1. Round 1: authorization and scope (blocking)
2. Round 2: access and scan limits (before scanning)
3. Round 3: build decisions (before the plan)
4. Round 4: questions the scan raises
5. Same-platform extras
6. `PROJECT.md` template

---

## Round 1: authorization and scope (blocking)

Nothing else happens until these are answered.

| # | Question | Default | Why it matters |
|---|---|---|---|
| 1.1 | Is this your site, or a client's site you're authorized to rebuild? Who is the owner? | none, must answer | A clone of someone else's site copies their content and brand. If it isn't theirs, offer to study its features and build an original site instead. |
| 1.2 | Source URL(s), including subdomains (shop., blog., help.) | the URL given | Subdomains are often separate platforms with their own data. |
| 1.3 | Target platform and stack (e.g. WordPress + WooCommerce + a named theme, Shopify, Next.js, static). Any must-use theme, builder or framework? Any banned ones? | ask; propose one from the intake | Decides every later step. |
| 1.4 | Exact copy, or copy plus fixes? How far can the design change? | exact layout, fix broken/accessibility/SEO/speed problems, log every change | Stops scope arguments later. |
| 1.5 | Must anything stay identical? (URLs, wording, prices, checkout steps, email texts) | URLs and wording stay | Some owners care more about one area than another. |
| 1.6 | Deadline and launch window | none | Sets phase depth; avoid launching in the owner's busy season. |
| 1.7 | Where should it be built: local machine, staging server, both? | local first, staging before launch | |
| 1.8 | Who reviews and approves? Is there a client behind the user? | the user | Reports and pitch materials are written for that person. |

## Round 2: access and scan limits (before scanning)

| # | Question | Default | Why |
|---|---|---|---|
| 2.1 | Can you export data from the admin (products, categories, content, redirects, settings)? Will you run the export, or may I click Export in your admin? | owner exports | Exports are complete; scraping isn't. |
| 2.2 | Is there an API key you can give (read-only scope)? | no | Some platforms export more through the API. Store it in `.env.local` only. |
| 2.3 | Any areas I must not touch, even to look? (admin, member areas, staging) | admin except export | |
| 2.4 | Logged-in areas worth scanning (customer account, wholesale pricing, members)? Can you provide a test customer login? | no | Logged-in features are invisible to a crawler. Use a test account, never a real customer's. |
| 2.5 | Does the site use bot protection (Cloudflare, CAPTCHA)? You'll need to pass any challenge yourself. | ask during scan | I won't solve challenges. |
| 2.6 | Which browser can I use: a built-in browser, your Chrome with an extension, or headless only? Is your Chrome logged into the admin? | built-in or headless | A logged-in admin browser shows edit controls; I'll avoid them. |
| 2.7 | How hard may I scan? (requests per second, time of day) | 1 request per second, sampled pages, off-peak | Protects the live site. |
| 2.8 | Can you share Search Console and analytics exports (top pages, top landing pages, 404s, backlinks)? | if available | Real traffic data finds the addresses and pages that matter most. |

## Round 3: build decisions (before the plan)

Group these by topic and ask only the relevant groups.

### Data
| # | Question | Default |
|---|---|---|
| 3.1 | Products/listings: move all, or skip discontinued or hidden ones? | all published + drafts kept as drafts |
| 3.2 | Variants, options, bundles, kits: in use? | check export; drop unused demo data |
| 3.3 | Customers: move them (without passwords, reset email at launch) or start fresh? | start fresh; don't export |
| 3.4 | Order history: move it, or keep it in the old admin / an archive? | don't move |
| 3.5 | Reviews and ratings | move if present |
| 3.6 | Blog posts, articles, help pages: all, or only live ones? | all real content; skip demo/placeholder text |
| 3.7 | Media: original files available, or download from the site? | download originals from known image paths, slowly |
| 3.8 | Coupons and gift cards still valid? | recreate active ones only |

### Addresses and SEO
| # | Question | Default |
|---|---|---|
| 3.9 | Keep the old addresses exactly, or move to clean addresses with 301 redirects? Or build both and compare? | keep exactly for the first build; offer clean as an option |
| 3.10 | Preferred domain form (www or not, trailing slash) | match the live site |
| 3.11 | SEO plugin or tool preference | lightest one that covers titles, sitemaps and schema |
| 3.12 | Keep the robots.txt policy (e.g. AI crawler blocks)? | keep as is |

### Commerce
| # | Question | Default |
|---|---|---|
| 3.13 | Payment gateway(s) on the new site. Same provider as now? | same provider if the target supports it; sandbox until launch |
| 3.14 | Shipping: carriers, live rates, flat rates, free shipping rules, local pickup | copy current rules exactly |
| 3.15 | Tax: current rule, and do you want address-based tax? | copy current rule; flag compliance risk |
| 3.16 | Currencies and languages; are the language flags real translations? | single currency; check what the flags do |
| 3.17 | Order emails: copy current wording? Sender address? | copy wording; owner's real mailbox as sender |
| 3.18 | Post-purchase features: account creation, review requests, guarantees, upsells, tracking | match current; need an order email screenshot |
| 3.19 | Wholesale, B2B, quote requests, minimum orders | only if in use |

### Integrations and operations
| # | Question | Default |
|---|---|---|
| 3.20 | Analytics and ads tags (GTM, GA4, ads, heatmaps): keep, and do you have access to the accounts? | keep the container ID; owner adds the new site in each account |
| 3.21 | Forms: contact, quote, mailing list provider | match fields and recipients |
| 3.22 | Live chat, popups, review widgets, trust seals | keep what's in use; drop dead ones |
| 3.23 | Third-party feeds (Google Merchant, marketplaces, ERP, accounting, drop-ship vendors) | list them; rebuild feeds |
| 3.24 | Plugin/app policy: free only, paid allowed, budget? | free first, paid options documented with prices |
| 3.25 | Hosting for production; who manages it? | recommend; owner buys |
| 3.26 | Email sending (SMTP/API service), domain DNS access | owner's provider; SPF/DKIM/DMARC checked |
| 3.27 | Who edits the site after launch, and how technical are they? | non-technical; use the native editor only |
| 3.28 | Legal: cookie consent, privacy policy, terms, accessibility statement, regional laws | keep existing pages; add a consent banner if tags need it |

### Design
| # | Question | Default |
|---|---|---|
| 3.29 | Logo files and brand assets in full quality? | extract from the site; ask for originals |
| 3.30 | Fonts: licensed for web use on the new host? | use the same font if licensed, else the nearest free one |
| 3.31 | Container width, phone layout preferences, anything you dislike now | match live; fix phone layout |

## Round 4: questions the scan raises

Typical ones. Ask them in a batch after the scan, with what you found:

- Conflicting facts on the site (three phone numbers, two free-shipping rules, old addresses). Which is current?
- Features with no sign of use (an affiliate program, a wishlist, language flags, an empty blog). Keep, drop, or keep dormant?
- Dead links and dead services (old social networks, discontinued widgets). Remove?
- Placeholder or demo content that is live and indexed. Remove?
- Categories or pages without names or with duplicate names. Merge?
- Prices or stock that look wrong in the export. Which source is right?
- Checkout behavior you couldn't observe. Can you send a recent order confirmation email and a thank-you page screenshot?

## Same-platform extras

- Which extensions are installed, and which are you sure you use? Any you pay for?
- Known problems with the current build (slow pages, errors, things the last developer left)?
- Staging copy available? Database dump and file backup?
- Theme customizations made in the code vs in the editor?

## PROJECT.md template

```markdown
# PROJECT.md: <site> to <target>

Owner: <name, company>   Authorized by: <who, how, date>
Source: <URL(s)>   Platform: <detected>
Target: <platform, theme, hosting>
Mode: exact copy | copy + fixes (approved scope: ...)

## Answers
| # | Question | Answer | Default? | Date |
|---|---|---|---|---|

## Open questions
| # | Question | Asked on | Blocking? |
|---|---|---|---|

## Off-limits
- ...
```
