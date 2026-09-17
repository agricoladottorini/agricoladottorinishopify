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

Supporting files: `snippets/product-card.liquid` (product card with quick add),
`snippets/css-variables.liquid` (tokens), `assets/critical.css` (reset,
buttons, spacing, reveal keyframes), `templates/index.json` (page order).

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
- **Journey arrows** were verified to render and to start disabled on the left,
  but were not click-tested.

## Gotchas

- Liquid does not interpolate `{{ }}` inside filter string arguments. Build the
  value with `assign` first, as the sections do for `object-position`.
- `assets/critical.css` gives every `svg` a `max-width: 100%`, which silently
  caps absolutely positioned SVGs. The hero line overrides it with
  `max-width: none`.
- With `shopify theme dev`, sections must upload before a template that
  references them. A fresh `templates/index.json` referencing a brand new
  section fails until the section syncs; touch the template afterwards.
- Editor edits by the owner are saved to the JSON files on the Shopify theme
  (`templates/*.json`, `sections/*-group.json`, `config/settings_data.json`),
  not to git. Pull those before pushing, or connect the theme to GitHub, or
  push with those paths ignored, otherwise their content gets overwritten.
