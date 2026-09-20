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
| `--color-tint` | `#EDE4D1` | Warm sand for "Tinted" section bands (manifesto by default) |

Deliberately not the warm beige plus brass palette that artisan food brands
default to. The sand tint is the one warm note, and it stays out of the shopping
areas: it only colors story sections (the manifesto), never cards,
buttons or accents, and there is no brass or gold anywhere. One accent only: the
lighter green `#8A9A4B` on the hero line is a tint of the same olive hue, and
the red in the newsletter error is a state color, not a second accent.

Inside `.d-bg--tint` (`assets/critical.css`) the tokens are scoped: muted and
accent are mixed toward the foreground so they keep WCAG AA on the darker sand
(the base muted `#5B6056` only reaches about 3.8:1 there), and both surfaces are
derived from the tint so placeholders and rules stay warm rather than the page's
cool greens. The unscoped values come from `--color-muted-base` and
`--color-accent-base`, because a custom property cannot reference itself.
Anything that must match the band behind it (e.g. the origin close-up's frame) uses
`--section-bg`.

**Type.** Outfit (Shopify font library) at 400 and 500. No serif anywhere.
Headings use weight 500 with tight negative letter spacing. Italic is used for
emphasis inside the same family, never a second font.

**Shape.** One rule, applied everywhere: interactive controls (buttons, inputs)
are full pills, media and cards use `--radius-media` (14px). Nothing else is
rounded.

**Theme.** Light only, by request. The dark hero frame is a photo container,
not a theme switch. The color tokens make dark mode straightforward to add
later if it is ever wanted.

## Brand mark

The hill line from the hero is the company mark. One path, reused everywhere:
`snippets/brand-line.liquid` renders it inline in `currentColor` (deep olive),
shown small above the footer copyright. The
favicon (`assets/favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, linked
from `snippets/meta-tags.liquid`) is the same line in cream on an olive tile,
vertically exaggerated so it still reads at 16px. The apple touch icon is a
full square because iOS rounds the corners itself.

Sources and exports (SVG, PNG, JPEG, `favicon.ico`) live in `brand/`, which is
in `.shopifyignore`. Re-export with `sips`, e.g.
`sips -s format png -Z 2000 brand/dottorini-linea.svg --out brand/dottorini-linea.png`.
Not in the header on purpose: the animated wordmark is already the logo there.

## Motion

- Hero: image settles from a slight scale, then headline, text and buttons
  rise in sequence. Sets reading order.
- Decorative hero line: draws itself once left to right behind a soft-edged
  mask. It does not loop.
- Sections: fade and rise on scroll via CSS scroll-driven animations
  (`animation-timeline: view()`) on the shared `.reveal` class. No scroll
  event listeners anywhere. Firefox does not support this yet and simply shows
  the content, which is an acceptable fallback.
- Varieties gallery (journey section): on phones a scroll-snap gallery. With
  more than three cards, desktop arrow buttons scroll by one card and a small
  custom element disables them at the ends using an IntersectionObserver.
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
| `sections/header.liquid` | Sticky 3-column bar, 68px, blurred background. Mobile menu is a native `<details>`, which a small script closes when a link is tapped. Links come from `snippets/header-nav-links.liquid`, shared by the bar and the drawer: contact entries go to `#contatti`, and up to two theme-setting links ("Convivia" -> `/#convivia`, a homepage anchor, "Museo" -> `/pages/museo`, its own page, neither a Shopify menu item) sit just before them, in that order. Arriving on a page with a hash, the header settles on the target once the page has loaded, because the browser's own jump was landing at the top |
| `sections/dottorini-hero.liquid` | Full-bleed framed photo, copy at the bottom over a gradient scrim, plus the decorative line |
| `sections/dottorini-featured-products.liquid` | Asymmetric grid: one large card, two stacked beside it |
| `sections/dottorini-manifesto.liquid` | Editorial statement, then the company text, up to three fact tiles (blocks: a big claim like "Raccolta a mano" with a small olive detail like "Ottobre-novembre") and the signature, beside one offset portrait image. From 900px the statement is limited to 7 columns because the image rises 8rem into its row. Fact tiles are light (`--color-background`) on the sand band, 14px radius like other cards, and stack on phones under ~400px so the detail never breaks at its hyphen |
| `sections/dottorini-journey.liquid` | "Dottorini varietà": the three olives in the blend (Moraiolo, Frantoiano, Leccino), each with photo, name, italic tagline and a short description. Up to three cards: one row from 900px with the middle card dropped; phones scroll-snap. More than three falls back to the scrolling gallery with arrows. File and block type keep the old `journey`/`step` names so editor data survives |
| `sections/dottorini-convivia.liquid` | Convivia, the family's home restaurant, as one large dark card (`--color-foreground`) inside the page column: copy left, full-height photo right, no hill line (removed at the owner's request). Phones stack photo over copy. The card is a photo container like the hero frame, not a theme switch. Adapted from an owner reference that used serif type and brass/terracotta; kept to Outfit and the olive tint `#8A9A4B` instead. The button links to the SumUp booking page and opens in a new tab |
| `sections/dottorini-origin.liquid` | No longer on the homepage (replaced by Convivia). Offset photo collage plus a facts list, kept so editor data that still references it does not break |
| `sections/footer.liquid` | Newsletter and columns, company details, then the copyright and policy row |

## Other pages

Catalogo, product and Museo are standalone pages (not homepage sections), so
each opens directly under the sticky header with nothing above it. They share
one heading (`<h1>`, one per page) and one top spacing value, the
`.section-space--flush-top` utility in `assets/critical.css`
(`padding-top: clamp(2rem, 6vw, 4rem)`, versus the `~5-9.5rem` rhythm between
homepage sections) so the gap from the header to the page's first heading
stays identical across all three. Apply it alongside `section-space` on the
page's outer wrapper; do not duplicate the value locally.

| File | What it is |
| --- | --- |
| `sections/collection.liquid` | Catalogo: 3 cards per row desktop, 2 from 700px, 1 on phones, paginated (12 per page). Heading is a section setting (default "Prodotti"), not `collection.title`, because the nav points at `/collections/all`, Shopify's auto-generated "every product" collection, which has no editable title in admin. Leave the setting blank to fall back to `collection.title` on a real collection |
| `sections/product.liquid` | Product page: thumbnail rail plus large image left, details right and sticky; quantity stepper beside the add button showing the price; expandable info rows as blocks. On phones the stepper becomes a full width bar above a full width button |
| `sections/dottorini-museo.liquid`, `templates/page.museo.json` | Museo della Civiltà Contadina, a photo showroom for the family's small collection of rural life exhibits, on its own page (`/pages/museo`, template `page.museo`), not the homepage. Short heading and intro, then a bento grid of photo blocks (no captions, images carry it). The first block anchors a 2x2 tile, the rest are uniform 1x1 tiles placed by `grid-auto-flow: dense`, which works for any block count without leaving a gap, though the layout is designed for 5. Phones stack single column with per-position aspect ratios for rhythm. Optional button, hidden unless both a label and a link are set |
| `sections/cart-drawer.liquid` | Cart as a floating rounded panel inset from the edges, not a page. Rendered on every page from `layout/theme.liquid` and refreshed through the Section Rendering API after each change |
| `sections/cart.liquid` | The `/cart` page: a no-JavaScript fallback, rarely seen since the drawer handles normal use. Line items reuse the drawer's `.cart-item` classes directly (the drawer section renders on every page, so those styles are already loaded globally) rather than duplicating them, so the two can't drift apart. Quantity changes go through a plain number input plus one shared "Aggiorna carrello" submit, since this page has to work with JavaScript off; remove is a plain link to `item.url_to_remove` |

Cart behaviour: the header cart icon opens the drawer (the link still points at
`/cart` so it works without JavaScript), quick add opens it after a successful
add, quantity changes and removals go through `/cart/change.js`, and a refused
change (no stock left) shows an Italian message in place instead of navigating
away.

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
- Section paragraphs stay under 25 words. Exception: the company text in the statement section is the owner's own (about 70 words) and stays as written.
- Only one small uppercase eyebrow on the whole page (Convivia section).
- No em-dashes or en-dashes anywhere in visible copy. Use a comma, a period or
  a hyphen.
- No invented numbers or specifications.
- Every string lives in section settings so the owner can edit it.

## Still open

- **Photos.** Products have no images and every image slot shows Shopify's
  placeholder. Needed: hero (landscape, 2400px or wider), statement (4:5),
  three olive varieties (4:5, e.g. the olives or the trees of each), Convivia (a table or a dish, 1600px or wider), product
  packshots, five Museo exhibit photos (any orientation, the first block reads
  larger so pick the strongest one for it). Product cards default to `contain`
  because bottle packshots look better uncropped; switch the section setting
  to `cover` for lifestyle shots.
- **Anchors.** The hero's second button ("La nostra terra") points at `#terra`,
  which now lives on the varieties section (it used to be the origin section).
  Convivia is at `#convivia`.
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
- **Varieties gallery arrows** only appear with more than three cards. They
  were verified to render and to start disabled on the left, but were not
  click-tested.
- **Store name** is still "Il mio negozio" in Settings > Store details, so every
  tab title outside the homepage, `og:site_name`, the footer copyright and all
  checkout emails still say it. Change it to Agricola Dottorini.
- **Product option pills** (the size-style selector) are written but never
  rendered: every product has a single variant. Treat as unverified.
- **Contact page** still exists at `/pages/contact`; the menu entry is rewritten
  in `sections/header.liquid` to jump to `#contatti` on the footer instead.
- **Footer bottom row on phones** was reported as hard to see. Copyright and
  policy links now flow inline and wrap only when they do not fit (at 375px:
  copyright on one line, both policy links side by side below), with 34px tap
  targets and 56px of clearance below, but the
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
