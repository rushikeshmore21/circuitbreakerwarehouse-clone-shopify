# Lessons from real clones

Problems that came up while cloning a 16,000-product store from Volusion to WordPress/WooCommerce, and how to avoid them. They're specific, but the patterns repeat on every platform.

## Scanning and data

- **The sitemap covers about half the addresses.** It listed one address per product; the platform also answered at a short form for every product, plus hundreds of article IDs and category forms that weren't in it. The redirect map ended at 33,126 rows for a 16,249-row sitemap. Build the map from the export, not the sitemap.
- **The platform ignores parts of the address.** Volusion served a product for any text before `-p/CODE.htm`. Test what the old platform accepts (case, name part, extensions) and handle all of it.
- **Logged-in admin browsers distort everything.** Admin toolbars and scripts loaded on the storefront doubled the request count and slowed every page. Take baselines logged out.
- **The checkout may be a different app.** The old checkout was a separate headless app behind a bot challenge. The owner had to pass the challenge; post-checkout behavior came from an order email they shared.
- **Exports contain years of junk.** Demo product options from 2010, inactive vendors, expired coupons, placeholder articles. Check what's actually used before rebuilding it.
- **Facts on the site conflict.** Three phone numbers and three different free-shipping statements. Ask, and record the answer.
- **Claims about third parties need checking.** An early note said a contact form was blocked; it was actually below a stock photo. Verify before you write it in the report.

## Build

- **Themes win specificity fights.** The pro version of a theme wrote header styles with stronger selectors than the free one, turning the menu bar white after an upgrade. An ID rule in the theme silently beat a class rule, so a sticky header never stuck. Check the winning selector in dev tools before adding `!important`.
- **Admin toolbars move sticky headers.** Logged in, the header slid 32px over the hero. Check every template logged in.
- **Hidden elements still take space.** A visually hidden phone link after the search box gave it a bottom margin, so the search box sat 11px above the cart button. Look at the box model, not just the visible element.
- **Setup scripts must set every flag explicitly.** Rerunning the form setup switched the forms off, because the forms plugin treats a missing "active" flag as inactive. Write every value, and rerun setup scripts in testing to catch this.
- **Defaults change behavior.** The default sort put other brands first on a brand page; related products were hidden on phones by a theme setting. Check theme and store defaults against the live site's behavior.
- **Headings that aren't headings.** Product descriptions had addresses and notes set in heading tags with line breaks. Convert those to paragraphs during import.
- **Payment SDKs load everywhere.** A payment plugin loaded its SDK on every page even while disabled. Dequeue what isn't used on a page.
- **Debug logs inside the web root can be downloaded.** Write them outside it, on every copy (the second copy missed this until the final sync).
- **Two copies drift.** The clean-URL copy missed fixes made to the first copy after the copy was made. Keep one sync script that copies code and reruns every setup script, and diff code folders and key settings before signing off.

## Features

- **Long dropdowns need typing.** A 133-value amperage filter was unusable on phones. A type-to-filter combobox on top of the native select fixed it and kept the no-JavaScript fallback. Then every option on every category was tested: 1,332 requests.
- **Pagination needs to be compact on phones.** The platform's default pager was long; a prev/next plus "page N of M" jump box worked better and matched the old site's style.
- **Popups must avoid key places.** The message tab moved up when the sticky add-to-cart bar showed on phones, and was skipped on contact, cart, checkout and account pages.
- **Empty states count.** An empty cart showed "CART:" with nothing after it. Check zero states (empty cart, no results, no image, no reviews).

## Testing

- **One failure in a thousand is often load.** One filter request out of 1,332 failed, and 13 of 16,249 sitemap checks timed out, all while another test hammered the same local server. Each passed alone in about a second. Rerun failures alone before reporting.
- **Long checks need progress you can read.** A 16,000-URL check that only writes at the end looks stuck for hours. Print progress or count requests in the access log.
- **Test the tools on the target, not just the pages.** A headless `scrollIntoView` failed because the site used smooth scrolling; screenshot tools need `scroll-behavior: auto`.

## Process

- **Ask before building.** Owner decisions (URL strategy, customer data, gateway, affiliate program, dormant features) changed the build. The "blocked on owner" table at the top of the plan kept them visible.
- **Log every fix at the time.** The fixes log reached 147 rows; reconstructing it at the end would have missed half.
- **Be honest in the pitch.** A "what the old platform still wins" section (built-in features, no extension costs) made the rest believable.
- **Files you can't upload, the owner can.** Browser automation couldn't upload files into Google Drive (native file picker). Hand over the files with clear names and let the owner upload.
- **A file open in Word can't be overwritten.** Write a new file name and say which one is current.
