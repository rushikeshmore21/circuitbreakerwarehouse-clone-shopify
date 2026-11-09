# Design spec (measured on live, 1440x900, 2026-11-10)

Tokens
- Font: cooper_hewitt (SIL OFL, from the font's name table), weights 500 / 600 / 700 + italics. Body 16px, line-height 1.4286 (22.857px), weight 500.
- Text #484848; navy #080375; red #d42400; blue nav/sidebar title #2185c2; price blue #00009f; sale-label green #00ff01 with #0000ff text; you-save #ff0000 (card computed #c00000 on wrapper, span #ff0000); footer bg #e3e3e3, footer text #5c5c5c, footer bottom text #595959, disclaimer box #f5f5f5; utility bar #f1f1f1; confidence band #e7e6fe; nav dividers #02bb02; input border #c3c3c3; sidebar border #d7d7d7; mailing input border #8a8a8a.
- Container: 1170px >=1200, 970px >=992, 750px >=768, padding 0 15px. Breakpoints 768 / 992 / 1200.

Header
- Top bar: 39px, padding 8px 0, centered 16px text, no background.
- Utility bar: 40px, line-height 40px, bg #f1f1f1. "FREE SHIPPING" 600 navy uppercase + " on All Orders!" #484848; 44px gap; "Call Today! " + phone 600 navy. Flags right, 4 x 34x34 svg.
- Logo row: 130px; logo 366x124 at x150 (container left), vertically centered. Search 291x50 (input border 1px #c3c3c3, 14px, text-indent 10px, placeholder "Search our store..."; red magnifier 21px in 50px square at right). Cart 139x50 red, padding 0 25px, white 16px/50px 700 "CART:0", icon 28x23 with 5px right margin; 20px gap search-cart.
- Nav: 50px bg #2185c2, items table-cell equal width with 1px #02bb02 left/right borders, link white 600 uppercase 16px/50px centered; hover bg #d42400.

Home
- Hero: full-width image 1440x339 (2584x608 art).
- Sidebar col 293px (col-md-3 of 1170) padding 45px 15px 25px; menu title bg #2185c2 white 15px 600 uppercase padding 16px 19px; list bordered 1px #d7d7d7, links 12px padding 8px 10px (33px rows). Promotions centered, 15px top pad: card logos 125x19; "Join our mailing list!" 20px/22px; input 220x42 border #8a8a8a 14px padding 6px 10px; "JOIN NOW" navy 115x42 600 uppercase; SSL seal 100x113; badge 137x58; 10px vertical margins.
- Product card: width 198 (4 cols in 877px), padding 15px 5px, image 150x150 centered, title 14px/20px 400 (3 lines), Our Price 16px blue label bold, Sale Price 16px 700 (label green bg), You Save 14px 700 italic red, free-shipping icon 31x25. Text left-aligned on home, centered on category.
- Confidence band: bg #e7e6fe, padding-top 47px, height 448; content col-md-6 offset 3 (555px at x443); H2 39px navy 500; p 16px/26px; buttons red pill radius 30px, 54px tall, padding 0 30px, 700 uppercase. Right col 263px: 4 items 18px 600 navy uppercase, padding 26px 0, icon ~57x39.
- Brands: grid 3 cols of 282x129 starting x443, logos grey (opacity/grayscale), dividers.
- Emergency: "Outage or Emergency?<br>Call 424-888-CBW8" Arial Black 18pt bold red centered.

Footer
- bg #e3e3e3; section 1 padding-bottom 46px; titles 18px 600 #626262 uppercase padding-top 50px; links 16px/32px #5c5c5c, two CSS columns; social icons 24px navy; disclaimer box #f5f5f5 472px wide, padding 0 40px 50px, at x818.
- Bottom: border-top 1px #c5c5c5, padding 35px 0 34px, copyright 16px/36px #595959; card svgs 34x11ish with 33px gaps; SSL svg 93x36.

Floating
- Back to top: 58x58 circle rgba(8,3,117,.5), padding 15px, white 28px arrow, fixed right ~72px bottom ~30px.
- buySAFE seal: 100x54 fixed left, y ~846 (bottom 0 at 900 viewport), date strip below.
