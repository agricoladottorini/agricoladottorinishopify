# Design notes

Recap of the design decisions behind the homepage, for future sessions.
Built September 2026 on the Shopify Skeleton theme.

## Brand and brief

Azienda Agricola Dottorini, olive oil from Umbria, sold direct to consumers.
Audience: people who care about clean, healthy food.
Vibe: minimal, light, airy, responsive.
References: skanvi.com, elevaremarket.com.

Explicitly ruled out by the owner:
- the standard hero with text on the left and a photo on the right
- long blocks of text
- generated imagery with campaign backgrounds or generic olive trees
- invented reviews or testimonials

## Design dials

| Dial | Value | Why |
| --- | --- | --- |
| Variance | 6 | "Minimal" keeps it calm, but the banned hero forces uneven, offset layouts |
| Motion | 4 | Restrained: an entrance, scroll reveals, hover feedback. Nothing flashy |
| Density | 2 | Gallery feel: large gaps, big images, very little copy |

## Visual language

**Colors** (theme settings, editable in the editor)

| Token | Value | Use |
| --- | --- | --- |
| `--color-background` | `#F5F6F2` | Page, a cool off-white with a faint green cast |
| `--color-foreground` | `#1E221D` | Text, primary buttons |
| `--color-accent` | `#56622F` | Deep olive. Hover states, eyebrow, cart badge |
| `--color-muted` | `#5B6056` | Secondary text, meets WCAG AA |
| `--color-surface` | `#ECEEE7` | Small product cards, footer |
| `--color-surface-strong` | `#E1E6D5` | Large product card, image placeholders |

Deliberately not the warm beige plus brass palette that artisan food brands
default to. One accent only: the lighter green `#8A9A4B` on the hero line is a
tint of the same olive hue, and the red in the newsletter error is a state
color, not a second accent.

**Type.** Outfit (Shopify font library) at 400 and 500. No serif anywhere.
Headings use weight 500 with tight negative letter spacing. Italic is used for
emphasis inside the same family, never a second font.

**Shape.** One rule, applied everywhere: interactive controls (buttons, inputs)
are full pills, media and cards use `--radius-media` (14px). Nothing else is
rounded.

**Theme.** Light only, by request. The dark hero frame is a photo container,
not a theme switch. The color tokens make dark mode straightforward to add
later if it is ever wanted.

## Motion

- Hero: image settles from a slight scale, then headline, text and buttons
  rise in sequence. Sets reading order.
- Decorative hero line: draws itself once left to right behind a soft-edged
  mask. It does not loop.
- Sections: fade and rise on scroll via CSS scroll-driven animations
  (`animation-timeline: view()`) on the shared `.reveal` class. No scroll
  event listeners anywhere. Firefox does not support this yet and simply shows
  the content, which is an acceptable fallback.
- Journey gallery: arrow buttons scroll by one card; a small custom element
  disables them at the ends using an IntersectionObserver.
- Header wordmark: on scroll the first word collapses its own width and fades
  while the last word slides into its place; scrolling back reverses it. Driven
  by a 1px marker below the sticky header plus an IntersectionObserver, so it
  works in every browser. One knob tunes it: `--brand-collapse` (1.1s) with an
  even easing, deliberately not the page's front-loaded one.
- Quick add: the + morphs into a check (two bars becoming an L, rotated) with a
  small pop, then returns after 1.8s.
- Cart drawer: slides in from the right, backdrop fades.
- Everything collapses to static under `prefers-reduced-motion: reduce`.

## Section layouts

Each section uses a different layout family on purpose. Nothing repeats.

| File | Layout |
| --- | --- |
| `sections/header.liquid` | Sticky 3-column bar, 68px, blurred background. Mobile menu is a native `<details>`, no JavaScript |
| `sections/dottorini-hero.liquid` | Full-bleed framed photo, copy at the bottom over a gradient scrim, plus the decorative line |
| `sections/dottorini-featured-products.liquid` | Asymmetric grid: one large card, two stacked beside it |
| `sections/dottorini-manifesto.liquid` | Editorial statement with one offset portrait image |
| `sections/dottorini-journey.liquid` | Horizontal scroll-snap gallery, staggered card heights |
| `sections/dottorini-origin.liquid` | Offset photo collage next to copy and a short facts list |
| `sections/footer.liquid` | Newsletter and columns above a large decorative wordmark |

## Other pages

| File | What it is |
| --- | --- |
| `sections/collection.liquid` | Catalogo: 3 cards per row desktop, 2 from 700px, 1 on phones, paginated (12 per page) |
| `sections/product.liquid` | Product page: thumbnail rail plus large image left, details right and sticky; quantity stepper beside the add button showing the price; expandable info rows as blocks. On phones the stepper becomes a full width bar above a full width button |
| `sections/cart-drawer.liquid` | Cart as a floating rounded panel inset from the edges, not a page. Rendered on every page from `layout/theme.liquid` and refreshed through the Section Rendering API after each change |

Cart behaviour: the header cart icon opens the drawer (the link still points at
`/cart` so it works without JavaScript), quick add opens it after a successful
add, quantity changes and removals go through `/cart/change.js`, and a refused
change (no stock left) shows an Italian message in place instead of navigating
away. `/cart` itself is still Skeleton's unstyled page and is only reached
without JavaScript.

Supporting files: `snippets/product-card.liquid` (product card with quick add),
`snippets/quick-add.liquid` (shared quick add styles and the `<quick-add>`
element, rendered by both the card and the product page),
`snippets/consent-inset.liquid` (reserves the height of Shopify's cookie banner
so it cannot cover the end of the footer),
`snippets/css-variables.liquid` (tokens), `assets/critical.css` (reset,
buttons, spacing, reveal keyframes), `templates/index.json` (page order).

## Product card variants

One snippet, three shapes, so the landing page and the catalog stay in step:
`featured` (large, landing only), `split` (image beside the text from 900px,
the two small landing cards) and the plain stacked default (catalog). The add
control is `add_style: 'plus'` everywhere now; `'label'` still renders a text
button if it is ever wanted. Price and + always sit on one row at the bottom.

## Titles and the shop name

`snippets/meta-tags.liquid` builds the tab title as `{{ page_title }} - {{ shop.name }}`,
and the landing page shows `page_title` alone. `shop.name` is the only brand
name Liquid exposes on every page, so it must be right in
**Settings > Store details > Store name**; the Homepage title in Online Store >
Preferences only affects the homepage. No brand name is hardcoded in the theme.

## Copy rules

- Italian, because the storefront locale is Italian.
- Hero: headline max 2 lines, subtext max 20 words. Currently 11.
- Section paragraphs stay under 25 words.
- Only one small uppercase eyebrow on the whole page (origin section).
- No em-dashes or en-dashes anywhere in visible copy. Use a comma, a period or
  a hyphen.
- No invented numbers or specifications.
- Every string lives in section settings so the owner can edit it.

## Still open

- **Photos.** Products have no images and every image slot shows Shopify's
  placeholder. Needed: hero (landscape, 2400px or wider), statement (4:5),
  four journey steps (4:5), origin (3:4 plus a square close-up), product
  packshots. Product cards default to `contain` because bottle packshots look
  better uncropped; switch the section setting to `cover` for lifestyle shots.
- **Unverified copy.** The defaults "spremitura a freddo, poche ore dopo la
  raccolta", "Ottobre, novembre", "vetro scuro" and "curiamo i nostri olivi a
  mano" are placeholders written to fit the brand, not facts confirmed by the
  owner. Confirm before launch.
- **Sample company details.** The Italian company block ships SAMPLE schema
  defaults in `sections/footer.liquid` (P. IVA `01234567890`, REA `PG 123456`,
  the Torgiano address, the phone number, the info email). Replace them with the
  real details before publishing. They live as schema defaults, not in
  `sections/footer-group.json`, because Shopify's GitHub sync lets the theme
  editor's stored JSON win: pushes to section-group JSON are ignored when the
  editor already holds a copy, while .liquid schema defaults always apply to
  settings that have no stored value.
- **Search is switched off.** The header search button is commented out in
  `sections/header.liquid`; the modal markup and its script stay in place and
  are inert until the button is uncommented.
- **Missing policies.** Shopify has privacy and cookies set up. Termini di
  servizio, Politica di rimborso (14 day withdrawal) and Spedizioni still need
  creating in Settings > Policies; the footer links them automatically.
- **Journey arrows** were verified to render and to start disabled on the left,
  but were not click-tested.
- **Store name** is still "Il mio negozio" in Settings > Store details, so every
  tab title outside the homepage, `og:site_name`, the footer copyright and all
  checkout emails still say it. Change it to Agricola Dottorini.
- **Product option pills** (the size-style selector) are written but never
  rendered: every product has a single variant. Treat as unverified.
- **Contact page** still exists at `/pages/contact`; the menu entry is rewritten
  in `sections/header.liquid` to jump to `#contatti` on the footer instead.
- **Footer bottom row on phones** was reported as hard to see. It now stacks the
  policy links with 34px tap targets and keeps 56px of clearance below, but the
  owner had not yet checked it on a real device, and their phone was looking at
  the deployed theme, not these local changes.

## Gotchas

- Liquid does not interpolate `{{ }}` inside filter string arguments. Build the
  value with `assign` first, as the sections do for `object-position`.
- `assets/critical.css` gives every `svg` a `max-width: 100%`, which silently
  caps absolutely positioned SVGs. The hero line overrides it with
  `max-width: none`.
- With `shopify theme dev`, sections must upload before a template that
  references them. A fresh `templates/index.json` referencing a brand new
  section fails until the section syncs; touch the template afterwards.
- `offsetParent` is always null on a fixed element. Measure the rect instead
  when testing whether something like the consent banner is on screen.
- In a column flex container `flex-basis` becomes a height. A button with
  `flex: 1 1 14rem` rendered 224px tall on phones until it was reset.
- Liquid `render` tags take values, not expressions: `split: forloop.first == false`
  is a syntax error. Assign first.
- The browser pane used for testing applies scrolls late and sometimes returns
  blank screenshots or a stale `window.scrollY`. Trust measured geometry from
  `document.scrollingElement`, and re-check rather than believing one reading.
- Editor edits by the owner are saved to the JSON files on the Shopify theme
  (`templates/*.json`, `sections/*-group.json`, `config/settings_data.json`),
  not to git. Pull those before pushing, or connect the theme to GitHub, or
  push with those paths ignored, otherwise their content gets overwritten.
