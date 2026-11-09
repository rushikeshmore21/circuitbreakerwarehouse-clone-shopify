# URLs and redirects

Search rankings, ad campaigns, old emails, printed material and other sites all point at the old addresses. A migration that drops them loses traffic for months. The work here is: find every old address, decide where each one goes, make it go there in one step, and prove it.

## Contents
1. Choose a strategy
2. Find every old address
3. Write the rules
4. Build the map
5. Implement
6. Validate
7. Export for production
8. After launch

---

## 1. Choose a strategy

| Strategy | When | Cost |
|---|---|---|
| **Keep every address exactly** (the new site answers at the old paths) | Safest for rankings; good first build; owner is nervous about SEO | Needs routing rules for odd paths (`.asp`, `.htm`, query-string pages); old ugly addresses stay |
| **Clean addresses + 301 from every old one** | Old addresses are meaningless or tied to the old platform | Full redirect map, validation, a short ranking wobble while search engines catch up |
| **Both, compared** | Owner can't decide | Build A (same addresses) and B (clean) from the same data on two ports; show the map and the validation results |

Either way, the new site must have one address per page (canonical), and every other form must 301 to it.

## 2. Find every old address

The sitemap is never enough. It usually lists one address per page while the platform answers to several. Gather from all of these and record the source of each row:

1. **Sitemap(s)**: `scripts/sitemap_urls.py`.
2. **Platform export**: every product code, category ID, article/page ID, which lets you generate each address form the platform supports (long form, short form, `.asp` and `.php`, ID forms).
3. **Alternate forms the platform answers to**: test by hand. Does the name part matter? Case? Trailing slash? `www`? Old extensions?
4. **Search Console**: top pages and pages with impressions (Performance export), plus Links > top linked pages.
5. **Analytics**: landing pages over the last 12-16 months.
6. **Server logs or CDN logs** if available: real requested paths.
7. **Backlink tools** if the owner has one.
8. **Existing redirects** in the old platform (export the list; they need to keep working and must not chain).
9. **Campaign links**: email platform, ad platform final URLs, QR codes, print.
10. **System pages**: cart, checkout, account, login, search, help, terms, privacy, index pages, feeds.

## 3. Write the rules

Write them as a table in `docs/redirect-strategy.md` before coding:

| Old pattern | New target | Example | Notes |
|---|---|---|---|
| `/{any}-p/{code}.htm` | product with that code | ... | name part ignored, case-insensitive |
| `/{any}-s/{id}.htm`, `?page=N` | category, page N | ... | past last page → last page |
| product code not found | search for the code | ... | better than a 404 for a part number |
| `/Articles.asp?ID=n` | the page now holding that text | ... | merged pages go to the merged page |
| `/cart.asp`, `/checkout.asp` | `/cart/` | ... | carts don't carry over; one hop instead of two |
| retired pages, placeholders | closest relevant page | ... | not the home page unless nothing fits |

Principles:
- **One hop.** Old → final page directly. Never old → intermediate → final. Chains waste crawl budget and some clients stop after a few hops.
- **301 for permanent moves.** 302 only for things that really are temporary.
- **Keep campaign parameters** (`utm_*`, `gclid`, `gbraid`, `wbraid`, `msclkid`, `fbclid`, affiliate IDs). Drop session IDs and junk.
- **Closest match, not the home page.** A redirect to the home page for a deleted product is treated like a 404 by search engines and annoys people. Send it to the category, or to search for that code.
- **Don't redirect what still exists.** If the address stays the same, it returns 200 directly.
- **Case and trailing slash** handled once, in the same hop.

## 4. Build the map

`migration/redirects/redirect-map.csv`:

```csv
old_url,old_type,new_url,status,source
https://example.com/Square-D-EDB34125-p/edb34125.htm,product,https://example.com/product/square-d-edb34125/,301,sitemap
https://example.com/product-p/edb34125.htm,product,https://example.com/product/square-d-edb34125/,301,export-short-form
https://example.com/,page,https://example.com/,200,sitemap
```

Generate it from the source export and the target database (the importer stored the source IDs, so the lookup is exact). Check for: duplicate old URLs, targets that are themselves redirected (chains), targets that are 404, and many old URLs to one target (fine, but check it's intended).

## 5. Implement

Two layers work well together:
- **A resolver in the application** that understands the patterns (product code → product) and handles anything not in the static map, including future odd forms. It runs before the 404 handler.
- **A static map at the edge or web server** for speed in production (nginx `map`, Apache `RewriteMap`, Cloudflare Bulk Redirects, Netlify `_redirects`, Vercel `redirects`). It skips the application for the bulk of redirects.

Keep the old→new lookup in the database (source ID meta) so the resolver never needs the CSV.

## 6. Validate

Run every row against the new site (local or staging), not a sample:

```bash
python scripts/check_urls.py migration/redirects/redirect-map.csv --base http://localhost:8081 --workers 6 --out migration/redirects/validation
```

A row passes when: the first response is the expected status (301 or 200), its `Location` equals `new_url` (after mapping the domain), the target responds 200, there's exactly one hop, and the target's canonical points to itself. Look at:
- Failures first, then rerun only the failures (`--only-failed`) before reporting them. Under load, local servers time out; a timeout isn't a broken redirect until it fails alone.
- Chains (more than one hop): fix the rule so it goes directly.
- 404 targets: a mapping bug or a missing import.
- Pages that redirect to themselves (loops).

Also crawl the new site's own pages and check that **no internal link points at an old address** (each one would cost a hop on every click).

## 7. Export for production

From the final CSV, write the format the host needs:

nginx:
```nginx
map $request_uri $redirect_target {
    default "";
    include /etc/nginx/redirects.map;   # lines: "/old/path" "/new/path";
}
server {
    if ($redirect_target) { return 301 $redirect_target; }
}
```

Apache: `RewriteMap redirects txt:/path/redirects.txt` and a `RewriteRule` that looks the path up.

Cloudflare Bulk Redirects: CSV with source URL, target URL, status code, and options (preserve query string, include subdomains).

Shopify: CSV with `Redirect from`, `Redirect to` columns (paths only).

Netlify `_redirects`: `/old /new 301` per line. Vercel: `redirects` array in `vercel.json` (keep large maps in middleware instead).

Hand the owner a spreadsheet version (a sheet each for rules, the full map, validation results, summary) so they can see it without tools.

## 8. After launch

- Submit the new sitemap in Search Console; keep the old property; use the change-of-address tool only if the domain changes.
- Watch the 404 log daily for two weeks, then weekly. Add rules for real requests that 404.
- Watch Search Console coverage and the redirect report for a few months.
- Keep redirects for at least a year, ideally forever. They cost almost nothing.
