🚨 MANDATORY: YOU MUST CALL "learn_shopify_api" ONCE WHEN WORKING WITH LIQUID THEMES.

## Theme Architecture

**Key principles: focus on generating snippets, blocks, and sections; users may create templates using the theme editor**

### Directory structure

| Directory | Purpose |
|-----------|---------|
| `assets/` | Static files (CSS, JS, images). Only `critical.css` and global statics — prefer `{% stylesheet %}`/`{% javascript %}` per component |
| `blocks/` | Reusable, nestable, merchant-editable components. Require `{% schema %}` validated against `schemas/theme_block.json` |
| `config/` | `settings_schema.json` (global theme settings, validate against `schemas/theme_settings.json`) + `settings_data.json` |
| `layout/` | Global HTML wrapper (`<head>`, `<body>`, nav, footer). Must include `{{ content_for_header }}` and `{{ content_for_layout }}` |
| `locales/` | Translation JSON files by language code. Validate against `schemas/translations.json` |
| `sections/` | Modular full-width page components. Require `{% schema %}` validated against `schemas/section.json` |
| `snippets/` | Reusable Liquid fragments rendered via `{% render %}`. Not editable in theme editor. Must have `{% doc %}` header |
| `templates/` | JSON files defining which sections/blocks appear on each page type |

**Component selection:**
- Merchant needs to configure it in theme editor → `section` or `block`
- Internal implementation detail, devs only → `snippet`
- Small reusable component inside a section → `block`
- Static code fragment shared across files → `snippet`

### CSS & JavaScript

- `{% stylesheet %}` and `{% javascript %}` are only supported in `snippets/`, `blocks/`, and `sections/`
- One `{% stylesheet %}` and one `{% javascript %}` tag per file maximum

### LiquidDoc

Required on all snippets and statically-rendered blocks:

```liquid
{% doc %}
  Renders a responsive image that might be wrapped in a link.

  @param {image} image - The image to be rendered
  @param {string} [url] - An optional destination URL for the image

  @example
  {% render 'image', image: product.featured_image %}
{% enddoc %}
```

---

## The `{% schema %}` tag

Validate all schema JSON: sections → `schemas/section.json`, blocks → `schemas/theme_block.json`, global settings → `schemas/theme_settings.json`.

### CSS variable vs CSS class pattern

**Single CSS property** → CSS variable:

```liquid
<div class="collection" style="--gap: {{ block.settings.gap }}px">
{% stylesheet %}
  .collection { gap: var(--gap); }
{% endstylesheet %}
{% schema %}
{
  "settings": [{ "type": "range", "id": "gap", "label": "t:labels.gap", "min": 0, "max": 100, "unit": "px", "default": 0 }]
}
{% endschema %}
```

**Multiple CSS properties** → CSS class:

```liquid
<div class="collection {{ block.settings.layout }}">
{% stylesheet %}
  .collection--full-width { /* multiple styles */ }
  .collection--narrow { /* multiple styles */ }
{% endstylesheet %}
{% schema %}
{
  "settings": [{
    "type": "select", "id": "layout", "label": "t:labels.layout",
    "values": [
      { "value": "collection--full-width", "label": "t:options.full" },
      { "value": "collection--narrow", "label": "t:options.narrow" }
    ]
  }]
}
{% endschema %}
```

**Mobile columns** → select input:

```liquid
{% schema %}
{
  "settings": [{
    "type": "select", "id": "columns_mobile", "label": "t:labels.columns_mobile",
    "options": [{ "value": "1", "label": "1" }, { "value": "2", "label": "2" }]
  }]
}
{% endschema %}
```

---

## Liquid

### Delimiters

| Syntax | Purpose |
|--------|---------|
| `{{ value }}` | Output |
| `{{- value -}}` | Output, trim surrounding whitespace |
| `{% tag %}` | Logic — no output |
| `{%- tag -%}` | Logic, trim surrounding whitespace |

### Operators

Comparison: `==` `!=` `>` `<` `>=` `<=`
Logical: `or` `and` `contains` (strings and arrays of strings only — not objects)

**Shopify-specific rules:**
- No parentheses in conditions
- No ternary operators — use `{% if %}`
- ALWAYS nest `{% if %}` for more than two logical operators

### Variables

```liquid
{% assign var = 'value' %}
{% capture var %}content{% endcapture %}
{% increment counter %}   {# increments from 0, independent of assign/capture #}
{% decrement counter %}   {# decrements from -1, shares counter with increment #}
```

> `increment` and `decrement` share their counter with each other but are independent from `assign`/`capture`. Avoid naming variables the same as Liquid global objects.

---

## Liquid Filters

Filters can be chained: `{{ "hello world" | upcase | split: " " | last }}` → `"WORLD"`

### Array
| Filter | Returns |
|--------|---------|
| `compact` | array |
| `concat: array` | array |
| `find: string, string` | untyped |
| `find_index: string, string` | number |
| `first` | untyped |
| `has: string, string` | boolean |
| `join` | string |
| `last` | untyped |
| `map: string` | array |
| `reject: string, string` | array |
| `reverse` | array |
| `size` | number |
| `sort` | array |
| `sort_natural` | array |
| `sum` | number |
| `uniq` | array |
| `where: string, string` | array |

### Cart
| Filter | Returns |
|--------|---------|
| `item_count_for_variant: {variant_id}` | number |
| `line_items_for: object` | array |

### Collection
| Filter | Returns |
|--------|---------|
| `link_to_type` | string |
| `link_to_vendor` | string |
| `sort_by: string` | string |
| `url_for_type` | string |
| `url_for_vendor` | string |
| `within: collection` | string |
| `highlight_active_tag` | string |

### Color
| Filter | Returns |
|--------|---------|
| `brightness_difference: string` | number |
| `color_brightness` | number |
| `color_contrast: string` | number |
| `color_darken: number` | string |
| `color_desaturate: number` | string |
| `color_difference: string` | number |
| `color_extract: string` | number |
| `color_lighten: number` | string |
| `color_mix: string, number` | string |
| `color_modify: string, number` | string |
| `color_saturate: number` | string |
| `color_to_hex` | string |
| `color_to_hsl` | string |
| `color_to_oklch` | string |
| `color_to_rgb` | string |
| `hex_to_rgba` | string |

### Customer
| Filter | Returns |
|--------|---------|
| `customer_login_link` | string |
| `customer_logout_link` | string |
| `customer_register_link` | string |
| `avatar` | string |
| `login_button` | string |

### Date
| Filter | Returns |
|--------|---------|
| `date: string` | string |

### Default
| Filter | Returns |
|--------|---------|
| `default: variable` | untyped |
| `default_errors` | string |
| `default_pagination` | string |

### Font
| Filter | Returns |
|--------|---------|
| `font_face` | string |
| `font_modify: string, string` | font |
| `font_url` | string |

### Format
| Filter | Returns |
|--------|---------|
| `json` | string |
| `structured_data` | string |
| `unit_price_with_measurement: unit_price_measurement` | string |
| `weight_with_unit` | string |

### Hosted File
| Filter | Returns |
|--------|---------|
| `asset_img_url` | string |
| `asset_url` | string |
| `file_img_url` | string |
| `file_url` | string |
| `global_asset_url` | string |
| `shopify_asset_url` | string |

### HTML
| Filter | Returns |
|--------|---------|
| `class_list` | string |
| `highlight: string` | string |
| `inline_asset_content` | string |
| `link_to: string` | string |
| `placeholder_svg_tag` | string |
| `preload_tag: as: string` | string |
| `script_tag` | string |
| `stylesheet_tag` | string |
| `time_tag: string` | string |

### Localization
| Filter | Returns |
|--------|---------|
| `currency_selector` | string |
| `format_address` | string |
| `t` | string |

### Math
| Filter | Returns |
|--------|---------|
| `abs` | number |
| `at_least` | number |
| `at_most` | number |
| `ceil` | number |
| `divided_by: number` | number |
| `floor` | number |
| `minus: number` | number |
| `modulo: number` | number |
| `plus: number` | number |
| `round` | number |
| `times: number` | number |

### Media
| Filter | Returns |
|--------|---------|
| `external_video_tag` | string |
| `external_video_url: attribute: string` | string |
| `image_tag` | string |
| `image_url: width: number, height: number` | string |
| `media_tag` | string |
| `model_viewer_tag` | string |
| `video_tag` | string |

> Deprecated (avoid): `article_img_url`, `collection_img_url`, `img_tag`, `img_url`, `product_img_url` — use `image_url` + `image_tag` instead.

### Metafield
| Filter | Returns |
|--------|---------|
| `metafield_tag` | string |
| `metafield_text` | string |

### Money
| Filter | Returns |
|--------|---------|
| `money` | string |
| `money_with_currency` | string |
| `money_without_currency` | string |
| `money_without_trailing_zeros` | string |

### Payment
| Filter | Returns |
|--------|---------|
| `payment_button` | string |
| `payment_terms` | string |
| `payment_type_img_url` | string |
| `payment_type_svg_tag` | string |

### String
| Filter | Returns |
|--------|---------|
| `append: string` | string |
| `base64_decode` | string |
| `base64_encode` | string |
| `base64_url_safe_decode` | string |
| `base64_url_safe_encode` | string |
| `camelize` | string |
| `capitalize` | string |
| `downcase` | string |
| `escape` | string |
| `escape_once` | string |
| `handleize` | string |
| `hmac_sha1: string` | string |
| `hmac_sha256: string` | string |
| `lstrip` | string |
| `md5` | string |
| `newline_to_br` | string |
| `pluralize: string, string` | string |
| `prepend: string` | string |
| `remove: string` | string |
| `remove_first: string` | string |
| `remove_last: string` | string |
| `replace: string, string` | string |
| `replace_first: string, string` | string |
| `replace_last: string, string` | string |
| `rstrip` | string |
| `sha1: string` | string |
| `sha256: string` | string |
| `slice` | string |
| `split: string` | array |
| `strip` | string |
| `strip_html` | string |
| `strip_newlines` | string |
| `truncate: number` | string |
| `truncatewords: number` | string |
| `upcase` | string |
| `url_decode` | string |
| `url_encode` | string |
| `url_escape` | string |
| `url_param_escape` | string |

### Tag
| Filter | Returns |
|--------|---------|
| `link_to_add_tag` | string |
| `link_to_remove_tag` | string |
| `link_to_tag` | string |

---

## Liquid Objects

### Global objects

`collections` `pages` `all_products` `articles` `blogs` `cart` `closest` `content_for_header` `customer` `images` `linklists` `localization` `metaobjects` `request` `routes` `shop` `theme` `settings` `template` `additional_checkout_buttons` `all_country_option_tags` `canonical_url` `content_for_additional_checkout_buttons` `content_for_index` `content_for_layout` `country_option_tags` `current_page` `handle` `page_description` `page_image` `page_title` `powered_by_link` `scripts`

### Page-scoped objects

| Template | Available objects |
|----------|-------------------|
| `/article` | `article` `blog` |
| `/blog` | `blog` `current_tags` |
| `/cart` | `cart` |
| `/checkout` | `checkout` |
| `/collection` | `collection` `current_tags` |
| `/customers/account` | `customer` |
| `/customers/addresses` | `customer` |
| `/customers/order` | `customer` `order` |
| `/gift_card.liquid` | `gift_card` `recipient` |
| `/metaobject` | `metaobject` |
| `/page` | `page` |
| `/product` | `product` |
| `/robots.txt.liquid` | `robots` |
| `/search` | `search` |

---

## Liquid Tags

### `assign`
```liquid
{% assign variable_name = value %}
```

### `break` / `continue`
```liquid
{% break %}
{% continue %}
```

### `capture`
```liquid
{% capture variable %}value{% endcapture %}
```

### `case`
```liquid
{% case variable %}
  {% when value_a %}expression{% when value_b %}expression
  {% else %}expression
{% endcase %}
```

### `comment`
```liquid
{% comment %}not rendered{% endcomment %}
```

### `content_for`
Two modes — `'blocks'` renders all child blocks, `'block'` renders a single static block:
```liquid
{% content_for 'blocks' %}
{% content_for 'block', type: 'slide', id: 'slide-1' %}
```

### `cycle`
Must be inside a `for` loop. Use for alternating classes (odd/even rows, etc.):
```liquid
{% cycle string, string, ... %}
```

### `doc`
LiquidDoc header — required on all snippets and statically-rendered blocks:
```liquid
{% doc %}
  @param {string} foo - Required param
  @param {string} [bar] - Optional param
  @example {% render 'name', foo: 'value' %}
{% enddoc %}
```

### `echo`
Same as `{{ }}` but usable inside `{% liquid %}` tags:
```liquid
{% liquid echo expression %}
```

### `else` / `elsif`
Used inside `if`, `unless`, `case`, and `for`:
```liquid
{% if a %}...{% elsif b %}...{% else %}...{% endif %}
{% for item in array %}...{% else %}Empty state{% endfor %}
```

### `for`
Max 50 iterations per page. Use `{% paginate %}` for larger arrays. Has a `forloop` object available inside:
```liquid
{% for variable in array %}expression{% endfor %}
```

### `form`
Requires a type parameter. Available types:
`activate_customer_password` `cart` `contact` `create_customer` `currency` `customer` `customer_address` `customer_login` `guest_login` `localization` `new_comment` `product` `recover_customer_password` `reset_customer_password` `storefront_password`

```liquid
{% form 'form_type' %}content{% endform %}
```

### `if` / `unless`
```liquid
{% if condition %}expression{% endif %}
{% unless condition %}expression{% endunless %}
```

### `javascript`
One per file. Liquid is NOT rendered inside — do not use Liquid variables:
```liquid
{% javascript %}javascript_code{% endjavascript %}
```

### `layout`
```liquid
{% layout name %}
```

### `liquid`
Each tag must be on its own line. Use `echo` to output values:
```liquid
{% liquid
  assign x = 'value'
  echo x
%}
```

### `paginate`
Required for arrays over 50 items. Max 25,000 items. Paginatable arrays:
`all_products` `article.comments` `blog.articles` `collections` `collection.products` `customer.addresses` `customer.orders` `pages` `product.variants` `search.results` `collection_list settings` `product_list settings`

```liquid
{% paginate array by page_size %}
  {% for item in array %}content{% endfor %}
{% endpaginate %}
```

### `raw`
```liquid
{% raw %}not parsed as Liquid{% endraw %}
```

### `render`
Snippets are scope-isolated — cannot access variables created outside. Can access global objects and template-context objects (e.g. `product` on product template). Pass outside variables explicitly as parameters:
```liquid
{% render 'filename' %}
{% render 'filename', param: value %}
```

### `section` / `sections`
`section` renders statically. `sections` renders a section group in layout:
```liquid
{% section 'name' %}
{% sections 'name' %}
```

### `style`
Unlike `{% stylesheet %}`, inline `{% style %}` output updates live in the theme editor when color settings change — no page refresh needed:
```liquid
{% style %}CSS_rules{% endstyle %}
```

### `stylesheet`
One per file. Liquid is NOT rendered inside:
```liquid
{% stylesheet %}css_styles{% endstylesheet %}
```

### `tablerow`
Must be wrapped in `<table>` tags. Has a `tablerowloop` object:
```liquid
<table>{% tablerow variable in array %}expression{% endtablerow %}</table>
```

---

## Translation & Localization

### Rules
- Every user-facing string MUST use `{{ 'key' | t }}` — no hardcoded English in templates
- Always update `locales/en.default.json` with new keys
- Schema strings go in `locales/en.default.schema.json`
- Use sentence case for all UI text (`Add to cart` not `Add To Cart`)
- Keys: snake_case, hierarchical, max 3 levels deep

### Usage

```liquid
<!-- Good -->
<button>{{ 'products.add_to_cart' | t }}</button>
<p>{{ 'products.price_range' | t: min: product.price_min | money, max: product.price_max | money }}</p>

<!-- Bad -->
<button>Add to cart</button>
```

### Key organization

```json
{
  "general": {
    "accessibility": { "skip_to_content": "Skip to content", "close": "Close" }
  },
  "products": {
    "add_to_cart": "Add to cart",
    "price": { "regular": "Regular price", "sale": "Sale price" }
  },
  "labels": { "gap": "Gap", "layout": "Layout" },
  "options": {
    "direction": { "horizontal": "Horizontal", "vertical": "Vertical" }
  }
}
```

### File structure

```
locales/
├── en.default.json         # Template translations (required)
├── en.default.schema.json  # Theme editor label translations (required)
├── es.json / es.schema.json
├── fr.json / fr.schema.json
└── pt-BR.json / pt-BR.schema.json
```

---

## Examples

### `snippet`

```liquid
{% doc %}
  Renders a responsive image optionally wrapped in a link.

  @param {image} image - The image to render
  @param {string} [url] - Optional link destination
  @param {string} [css_class] - Optional class on the wrapper
  @param {number} [width] - Max render width
  @param {number} [height] - Max render height
  @param {string} [crop] - Crop position

  @example
  {% render 'image', image: product.featured_image %}
  {% render 'image', image: product.featured_image, url: product.url %}
  {% render 'image', css_class: 'product__image', image: product.featured_image, url: product.url, width: 1200, height: 800, crop: 'center' %}
{% enddoc %}

{% liquid
  unless height
    assign width = width | default: image.width
  endunless
  if url
    assign wrapper = 'a'
  else
    assign wrapper = 'div'
  endif
%}

<{{ wrapper }}
  class="image {{ css_class }}"
  {% if url %}href="{{ url }}"{% endif %}
>
  {{ image | image_url: width: width, height: height, crop: crop | image_tag }}
</{{ wrapper }}>

{% stylesheet %}
  .image { display: block; position: relative; overflow: hidden; width: 100%; height: auto; }
  .image > img { width: 100%; height: auto; }
{% endstylesheet %}

{% javascript %}
  function doSomething() { /* example */ }
  doSomething()
{% endjavascript %}
```

### `block` — Text

```liquid
{% doc %}
  Renders a text block.
  @example {% content_for 'block', type: 'text', id: 'text' %}
{% enddoc %}

<div
  class="text {{ block.settings.text_style }}"
  style="--text-align: {{ block.settings.alignment }}"
  {{ block.shopify_attributes }}
>
  {{ block.settings.text }}
</div>

{% stylesheet %}
  .text { text-align: var(--text-align); }
  .text--title { font-size: 2rem; font-weight: 700; }
  .text--subtitle { font-size: 1.5rem; }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.text",
  "settings": [
    { "type": "text", "id": "text", "label": "t:labels.text", "default": "Text" },
    {
      "type": "select", "id": "text_style", "label": "t:labels.text_style",
      "options": [
        { "value": "text--title", "label": "t:options.text_style.title" },
        { "value": "text--subtitle", "label": "t:options.text_style.subtitle" },
        { "value": "text--normal", "label": "t:options.text_style.normal" }
      ],
      "default": "text--title"
    },
    { "type": "text_alignment", "id": "alignment", "label": "t:labels.alignment", "default": "left" }
  ],
  "presets": [{ "name": "t:general.text" }]
}
{% endschema %}
```

### `block` — Group

```liquid
{% doc %}
  Renders a group of blocks with configurable layout direction, alignment, and padding.
  @example {% content_for 'block', type: 'group', id: 'group' %}
{% enddoc %}

<div
  class="group {{ block.settings.layout_direction }}"
  style="--padding: {{ block.settings.padding }}px; --alignment: {{ block.settings.alignment }};"
  {{ block.shopify_attributes }}
>
  {% content_for 'blocks' %}
</div>

{% stylesheet %}
  .group { display: flex; flex-wrap: nowrap; overflow: hidden; width: 100%; }
  .group--horizontal { flex-direction: row; justify-content: space-between; align-items: center; padding: 0 var(--padding); }
  .group--vertical { flex-direction: column; align-items: var(--alignment); padding: var(--padding) 0; }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.group",
  "blocks": [{ "type": "@theme" }],
  "settings": [
    {
      "type": "select", "id": "layout_direction", "label": "t:labels.layout_direction",
      "default": "group--vertical",
      "options": [
        { "value": "group--horizontal", "label": "t:options.direction.horizontal" },
        { "value": "group--vertical", "label": "t:options.direction.vertical" }
      ]
    },
    {
      "visible_if": "{{ block.settings.layout_direction == 'group--vertical' }}",
      "type": "select", "id": "alignment", "label": "t:labels.alignment",
      "default": "flex-start",
      "options": [
        { "value": "flex-start", "label": "t:options.alignment.left" },
        { "value": "center", "label": "t:options.alignment.center" },
        { "value": "flex-end", "label": "t:options.alignment.right" }
      ]
    },
    { "type": "range", "id": "padding", "label": "t:labels.padding", "default": 0, "min": 0, "max": 200, "step": 2, "unit": "px" }
  ],
  "presets": [
    { "name": "t:general.column", "category": "t:general.layout", "settings": { "layout_direction": "group--vertical", "alignment": "flex-start", "padding": 0 } },
    { "name": "t:general.row", "category": "t:general.layout", "settings": { "layout_direction": "group--horizontal", "padding": 0 } }
  ]
}
{% endschema %}
```

### `section`

```liquid
<div class="example-section full-width">
  {% if section.settings.background_image %}
    <div class="example-section__background">
      {{ section.settings.background_image | image_url: width: 2000 | image_tag }}
    </div>
  {% endif %}

  <div class="example-section__content">
    {% content_for 'blocks' %}
  </div>
</div>

{% stylesheet %}
  .example-section { position: relative; overflow: hidden; width: 100%; }
  .example-section__background { position: absolute; width: 100%; height: 100%; z-index: -1; overflow: hidden; }
  .example-section__background img { position: absolute; width: 100%; height: auto; top: 50%; left: 50%; transform: translate(-50%, -50%); }
  .example-section__content { display: grid; grid-template-columns: var(--content-grid); }
  .example-section__content > * { grid-column: 2; }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.custom_section",
  "blocks": [{ "type": "@theme" }],
  "settings": [
    { "type": "image_picker", "id": "background_image", "label": "t:labels.background" }
  ],
  "presets": [{ "name": "t:general.custom_section" }]
}
{% endschema %}
```
