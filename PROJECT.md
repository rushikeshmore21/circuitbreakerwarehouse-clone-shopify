# PROJECT.md: circuitbreakerwarehouse.com to Shopify

Owner: Circuit Breaker Warehouse (client of Coalition Technologies)   Authorized by: user (Rushikesh More, Coalition Technologies), confirmed in chat 2026-11-10
Source: https://www.circuitbreakerwarehouse.com/   Platform: Volusion (detected from `-s/ID.htm` and `Articles.php?ID=` addresses)
Target: Shopify Online Store 2.0, theme built on Dawn, store `testrushikesh.myshopify.com`, local dev `http://127.0.0.1:9292` (`shopify theme dev`)
Mode: exact copy of the frontend; code built to Shopify theme standards (sections, blocks, snippets, translations, accessibility)

## Answers
| # | Question | Answer | Default? | Date |
|---|---|---|---|---|
| 1.1 | Whose site, authority | Client site, authorized | no | 2026-11-10 |
| 1.3 | Target platform | Shopify, Dawn base in this repo | no | 2026-11-10 |
| 1.4 | Exact copy or copy + fixes | Exact copy on the frontend; anything that makes it better is done in code to standards | no | 2026-11-10 |
| 1.7 | Where built | Local `shopify theme dev` on the test store | no | 2026-11-10 |
| - | Scope | Full site: every page type, including new templates | no | 2026-11-10 |
| 3.1 | Product data | User already added products (16) and menus in admin; data migration is a later phase | no | 2026-11-10 |
| - | Manufacturer collections | Build templates as if the collections exist; user adds collection data later | no | 2026-11-10 |
| 3.20/3.22 | Third-party scripts | Clone every visual widget (buySAFE seal, language flags, etc.); leave out tracking and analytics scripts (GTM, Clarity) | no | 2026-11-10 |
| 3.9 | Redirects | Not required for now | no | 2026-11-10 |
| - | Project docs | In repo, excluded from theme uploads via `.shopifyignore`; local git commits only, never push | no | 2026-11-10 |
| 2.6 | Browser | Built-in browser pane | yes | 2026-11-10 |
| 2.7 | Scan rate | 1 request per second, sampled pages, GET only | yes | 2026-11-10 |

## Open questions
| # | Question | Asked on | Blocking? |
|---|---|---|---|

## Off-limits
- The live site is read-only: no forms, no cart writes, no account actions.
- No `git push`.
