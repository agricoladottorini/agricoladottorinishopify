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

**Colors** (theme settings, editable in the editor). Recolored September 30,
2026 to the client's palette. The owner kept their own deep olive as the one
accent instead of the client's lighter `#7C8650`.

| Token | Value | Use |
| --- | --- | --- |
| `--color-background` | `#EDE4D1` | Page, a warm sand |
| `--color-foreground` | `#211C14` | Text, primary buttons, the Convivia card |
| `--color-dark` | `#211C14` | Ground of "Dark" sections (the footer) |
| `--color-accent` | `#56622F` | Deep olive, the one accent. Hover fill for dark controls, eyebrow, cart badge |
| `--color-accent-light` | `#CBD6AC` | Light sage. Hover fill for light and ghost controls |
| `--color-muted` | `#625949` | Secondary text, AA on every light ground (4.8:1 on the large card, the lowest) |
| `--color-surface` | `#FBF6EC` | Cream. Small product cards, light panels |
| `--color-surface-strong` | `#E2D6BD` | Darker sand. Large product card, image placeholders |
| `--color-tint` | `#FBF6EC` | "Tinted" section bands (statement, Convivia's band), lighter than the page |

This is the warm beige plus dark-brown family the theme originally avoided;
it is here because the client asked for it by value. The client's palette
also had terracotta `#B05C3A` (gift card, secondary button) and gold
`#B58A2E`. Neither is applied: there is no gift card yet, and a second and
third accent would break the one-accent rule. Add terracotta to one specific
element if the client insists, never as a general accent.

Section grounds are classes on each section's band, picked in the editor:
`d-bg--base` (page), `d-bg--tint` (cream) and `d-bg--dark` (the footer's
default). In `assets/critical.css` each one rescopes the tokens rather than
components restyling themselves. Inside `.d-bg--tint` muted and accent are
mixed toward the foreground and surfaces are derived from the tint. Inside
`.d-bg--dark` text turns cream, the accent lifts to the light olive
`#8A9A4B` (the deep olive is under 3:1 there, the light one 5.5:1),
`--color-background` becomes a slightly raised dark so buttons (cream fill,
dark label) and form fields keep working, and `--color-error` becomes a light
coral. The unscoped values come from `--color-muted-base`,
`--color-accent-base` and `--color-surface-base`, because a custom property
cannot reference itself. Input borders use `--color-field-border`, derived
from the section's own text and ground (3.5:1 on the page, 5:1 in the
footer). Anything that must match the band behind it uses `--section-bg`. Hardcoded translucent creams and
near-blacks (scrims, the hero text, the Museo viewer) use the palette's warm
values `rgb(251 246 236)` and `rgb(33 28 20)` / `rgb(22 18 12)`. Text and light
controls over photography use `--color-on-photo` (`#FDFCF9`, near white, at
the owner's request): the hero heading, text and pill, and the
light pill on the Convivia card. They must not follow the sand page colour.

Section anchors (`#oli`, `#collina`, `#terra`, `#convivia`) sit on each band's
padded inner box. `.section-band > [id]` gives them a negative
`scroll-margin-top` that skips most of the section's top padding, so a menu
jump puts the heading `--anchor-gap` (2rem) under the header instead of up to
9.5rem further down, and the band's top edge scrolls out of view, so no strip
of the band above shows. The padding itself stays symmetric (top and bottom)
on purpose: moving it all to the bottom would glue headings to the top edge of
the coloured bands for anyone scrolling normally. The footer drops its top margin when it follows a
section band (`:has()` in `sections/footer.liquid`), otherwise a strip of page
sand sat between the last band and the dark footer.

**Type.** Three families, chosen by the client (September 2026), replacing
the original Outfit-only system. All three are self-hosted woff2 files from
Google Fonts (SIL Open Font License, latin subset) in `assets/`, declared in
`snippets/css-variables.liquid` as `--font-body--family`,
`--font-heading--family` and `--font-accent--family`. There is no font picker
in the theme editor any more: Hanken Grotesk is not in Shopify's font library,
and the library only has Cormorant, not Cormorant Garamond.

| Family | Role | Files |
| --- | --- | --- |
| Hanken Grotesk 400, 500, italic 400 | Body text and all UI: nav, buttons, prices, labels, forms | `hanken-grotesk.woff2` (variable), `hanken-grotesk-italic.woff2` |
| Marcellus 400 | `h1` to `h4`, the header wordmark, and display lines marked `.type-display` (manifesto statement, fact tiles) | `marcellus-400.woff2` |
| Cormorant Garamond italic 500 | `em` inside headings and `.type-display`, the varieties taglines, the Convivia lede, or anything marked `.type-accent` | `cormorant-garamond-italic.woff2` (variable) |

Marcellus has a single weight and no italic, so headings are always 400 and
`font-synthesis: none` stops the browser faking a bold or slanted Marcellus.
Headings keep only a slight `-0.01em` tracking: the tight negative spacing
tuned for Outfit crowded the serif. Cormorant's x-height is small next to
Marcellus, so emphasis inside a heading runs at `1.12em` and the standalone
italic lines are sized up by hand. Small uppercase labels (footer column
titles, eyebrows) stay in Hanken Grotesk even when they are `h3`. The social
image in `brand/` uses the same set: logo, name in Marcellus, tagline in
Hanken Grotesk with "nato in Umbria." in Cormorant italic, as in the hero.

**Shape.** One rule, applied everywhere: interactive controls (buttons, inputs)
are full pills, media and cards use `--radius-media` (14px). Nothing else is
rounded.

**Hover.** One rule too, and it follows the control's own fill, not the section
behind it: anything dark deepens to `--color-accent`, anything light or ghosted
fills with `--color-accent-light`. That covers the solid pill and the product
page's add button (dark), the light pill, the varieties arrows and every ghost icon control (cart
close, quantity steppers, remove), and the Museo viewer controls, which sit on
the near-black ground and so take the deep olive with cream text (about 6:1).

**Theme.** Light only, by request. The dark footer is a band that closes the
page and the dark hero frame is a photo container; neither is a theme switch. The color tokens make dark mode straightforward to add
later if it is ever wanted.

## Brand mark

The company mark is the client's logo: an olive ribbon (`#b6b351`, token
`--color-logo` in `assets/critical.css`) running up over the hill, cropped flat
at both ends. The original PNG is `brand/logo/Logo.png`; it was traced with
potrace into one filled path, reused everywhere: `snippets/brand-logo.liquid`
renders it inline in `currentColor`, and every mark container sets
`color: var(--color-logo)`. It sits small above the footer copyright (88px),
in the cart drawer's empty state, on the password page and in the header in
front of the wordmark. The ribbon tapers to nothing at its ends, so the header
draws it at 52-72px wide rather than smaller, or only the hump survives. It is
skipped when a logo is uploaded, because the logo is the mark then, and it sits
outside the wordmark so the tagline fold does not move it.

The favicon (`assets/favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`,
linked from `snippets/meta-tags.liquid`) is the same ribbon in the logo colour
on a dark tile (`#211C14`), running full bleed and stretched vertically 1.9x so
it still reads at 16px. The small sizes (SVG, 16, 32, 48) add a stroke in the
same colour to thicken it; 180 and 512 keep the true taper. The apple touch
icon is a full square because iOS rounds the corners itself.

Sources and exports live in `brand/`, which is in `.shopifyignore`: the logo
as SVG and PNG (`dottorini-logo`, `-chiaro` for dark grounds, `-scuro` for
one-colour print), the icon (`dottorini-icona.svg`, `-512.png`),
`favicon.ico` (16/32/48), and the social image. PNGs from the SVGs can be
re-exported with `sips`, e.g.
`sips -s format png brand/dottorini-logo.svg --out brand/dottorini-logo.png`.

## Motion

- Hero: image settles from a slight scale, then headline, text and buttons
  rise in sequence. Sets reading order.
- Hero logo ribbon: draws itself once left to right behind a soft-edged
  mask. It does not loop.
- Sections: fade and rise on scroll via CSS scroll-driven animations
  (`animation-timeline: view()`) on the shared `.reveal` class. No scroll
  event listeners anywhere. Firefox does not support this yet and simply shows
  the content, which is an acceptable fallback.
- Varieties gallery (journey section): on phones a scroll-snap gallery. With
  more than three cards, desktop arrow buttons scroll by one card and a small
  custom element disables them at the ends using an IntersectionObserver.
- Header wordmark: "Agricola Dottorini" on top in Marcellus, the tagline
  "L'olio di Collazzone" under it in olive Cormorant italic (header setting
  `tagline`, blank hides it). On scroll the tagline folds its row away
  (`grid-template-rows` 1fr to 0fr) and fades, and the name settles to the
  middle of the bar; scrolling back reverses it. The header keeps its 68px, so
  nothing below moves. Driven by a 1px marker below the sticky header plus an
  IntersectionObserver, so it works in every browser. One knob tunes it:
  `--brand-collapse` (0.6s) with an even easing. This replaced the earlier
  animation where "Agricola" collapsed and "Dottorini" slid into its place.
- Add to cart (product page): the button confirms with the "added" label, then
  returns after 1.8s.
- Cart drawer: slides in from the right, backdrop fades.
- Museo spawn: on desktop the heading and the photos already on screen rise and
  fade in one after another, 70ms apart, each photo settling out of a slight
  zoom the way the hero image does. Everything below the fold rides the shared
  `.reveal` scroll animation instead. The order has to be measured, because in
  a multicol layout the DOM runs down each column and says nothing about where
  a photo sits, so a small inline script marks the on-screen parts with their
  reading-order index. It is inline, not in the section's `{% javascript %}`
  bundle, because that bundle is deferred: it would let the photos paint and
  then hide them again to animate them in. Phones keep the plain reveal.
- Museo viewer: the photo fades in with its ground. Arrows and the arrow keys
  step through the collection and wrap at both ends, a counter says where you
  are, and any click outside the controls closes it, which the `zoom-out`
  cursor advertises. Inside the viewer the focus ring switches to the cream,
  because the page's olive ring has too little contrast on the dark ground.
- Everything collapses to static under `prefers-reduced-motion: reduce`.

## Section layouts

Each section uses a different layout family on purpose. Nothing repeats.

| File | Layout |
| --- | --- |
| `sections/header.liquid` | Sticky 3-column bar, 68px, blurred background. The logo sits in front of the wordmark and its tagline, centred against both. Mobile menu is a native `<details>`, which a small script closes when a link is tapped. Links come from `snippets/header-nav-links.liquid`, shared by the bar and the drawer. They are six label/target pairs in the header's own settings (`nav_1` to `nav_6`), not a Shopify menu, so homepage anchors live in the theme: "La collina" -> `/#collina` (statement), "L'olio" -> `/collections/all`, "Cultivar" -> `/#terra` (varieties), "Museo" -> `/pages/museo`, "Convivia" -> `/#convivia`, "Contatti" -> `#contatti` (footer). A blank label hides a link. There is no Home entry: the wordmark links home. Arriving on a page with a hash, the header settles on the target once the page has loaded, because the browser's own jump was landing at the top |
| `sections/dottorini-hero.liquid` | Full-bleed framed photo in three bands: heading top left, the logo ribbon across the middle, text and one button ("Scopri gli oli") at the bottom, with a scrim at top and bottom for contrast. The ribbon is in the content flow (not absolutely positioned), centred between heading and text and pulled past the padding to run edge to edge, so it never overlaps the copy; the frame has a `min-height` and grows if the content needs it. Filled path, colour is a section setting (default `#B6B351`). Height capped at `40svh` so it flattens a little on short wide screens; drawn 1.5x taller under 900px |
| `sections/dottorini-strip.liquid` | Full-bleed olive strip (`#56622F`, cream text) between the hero and the statement, one centred line in Marcellus with an optional Cormorant italic emphasis. Text and both colours are section settings; a blank text hides it |
| `sections/dottorini-featured-products.liquid` | Asymmetric grid: one large card, two stacked beside it |
| `sections/dottorini-manifesto.liquid` | Editorial statement, then the company text, up to three fact tiles (blocks: a big claim like "Raccolta a mano" with a small olive detail like "Ottobre-novembre") and the signature, beside one offset portrait image. From 900px the statement is limited to 7 columns because the image rises 8rem into its row. The section sits on the sand band (`d-bg--base`), straight after the hero and before the products, so the fact tiles are cream (`--color-tint`) to stand off it; on a tint band they fall back to the sand `--color-background`, 14px radius like other cards. They stay side by side on phones too (one per row left the band half empty), with tighter padding under 560px so a detail like "Ottobre-novembre" stays on one line from 360px up; titles may wrap to two lines there. Only under ~350px do they stack |
| `sections/dottorini-journey.liquid` | "Dottorini varietà": the three olives in the blend (Moraiolo, Frantoiano, Leccino), each with photo, name, italic tagline and a short description. Up to three cards: one row from 900px with the middle card dropped; phones scroll-snap. More than three falls back to the scrolling gallery with arrows. File and block type keep the old `journey`/`step` names so editor data survives |
| `sections/dottorini-convivia.liquid` | Convivia, the family's home restaurant, as one large dark card (`--color-foreground`) inside the page column: copy left, full-height photo right, no hill line (removed at the owner's request). Phones stack photo over copy. The card is a photo container like the hero frame, not a theme switch. Adapted from an owner reference that used serif type and brass/terracotta; kept to the olive tint `#8A9A4B` instead of brass (the serif came back later with the client's type system). The button links to the SumUp booking page and opens in a new tab |
| `sections/footer.liquid` | Dark band (`d-bg--dark`) by default: newsletter and columns, company details, then the copyright and policy row |

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
| `sections/dottorini-museo.liquid`, `templates/page.museo.json` | Museo della Civiltà Contadina, a photo showroom for the family's small collection of rural life exhibits, on its own page (`/pages/museo`, template `page.museo`), not the homepage. Short heading and intro, then one masonry archive. No photo is featured over the others (the owner turned down a large opening plate): the collection is a set of peers and the varied heights carry the rhythm. The archive is CSS `columns`, 3 from 1100px, 2 from 560px, 1 on phones, and each photo keeps its own `aspect_ratio` rather than being cropped into a tile: a scythe or a yoke is the wrong shape for a square. Column gaps come from `column-gap`, row gaps from the item margin, and a negative bottom margin cancels the trailing one. No captions, images carry it. Clicking a photo opens it in a viewer, a native `<dialog>` so Escape, focus return and inertness are the browser's job. The layout holds any block count, from 5 to the 30 the schema allows; the template ships 20 empty slots. Optional button, hidden unless both a label and a link are set |
| `sections/cart-drawer.liquid` | Cart as a floating rounded panel inset from the edges, not a page. Rendered on every page from `layout/theme.liquid` and refreshed through the Section Rendering API after each change. Empty, it keeps the same frame as a full cart: the logo and the message centred in the items area, and "Vedi i prodotti" full width at the bottom where "Vai al checkout" sits |
| `sections/cart.liquid` | The `/cart` page: a no-JavaScript fallback, rarely seen since the drawer handles normal use. Line items reuse the drawer's `.cart-item` classes directly (the drawer section renders on every page, so those styles are already loaded globally) rather than duplicating them, so the two can't drift apart. Quantity changes go through a plain number input plus one shared "Aggiorna carrello" submit, since this page has to work with JavaScript off; remove is a plain link to `item.url_to_remove` |

Cart behaviour: the header cart icon opens the drawer (the link still points at
`/cart` so it works without JavaScript), the product page's add button opens it
after a successful add, quantity changes and removals go through `/cart/change.js`, and a refused
change (no stock left) shows an Italian message in place instead of navigating
away.

Supporting files: `snippets/product-card.liquid` (product card, links to the
product page), `snippets/quick-add.liquid` (the `<quick-add>` element that adds
to the cart with fetch, used by the product page, which styles its states),
`snippets/consent-inset.liquid` (reserves the height of Shopify's cookie banner
so it cannot cover the end of the footer),
`snippets/css-variables.liquid` (tokens), `assets/critical.css` (reset,
buttons, spacing, reveal keyframes), `templates/index.json` (page order).

## Product card variants

One snippet, three shapes, so the landing page and the catalog stay in step:
`featured` (large, landing only), `split` (image beside the text from 900px,
the two small landing cards) and the plain stacked default (catalog). Cards have
no buy control: the whole card links to the product page, where the add button
lives. Title on top, price at the bottom.

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
  packshots, about 20 Museo exhibit photos (any orientation, nothing is cropped,
  every photo keeps its own shape). Product cards default to `contain`
  because bottle packshots look better uncropped; switch the section setting
  to `cover` for lifestyle shots.
- **Anchors.** The hero has one button, "Scopri gli oli" (`#oli`); the statement
  is reached from the header's "La collina" (`#collina`). The header's "Cultivar" points at `#terra`,
  which lives on the varieties section. Convivia is at `#convivia`.
- **Company details.** The real details (ragione sociale, P. IVA, Collazzone
  address, phone, email) are stored in the theme editor. The schema defaults in
  `sections/footer.liquid` are still SAMPLE values (P. IVA `01234567890`, a
  Torgiano address) and only show if the stored values are ever cleared.
  Shopify's GitHub sync lets the editor's stored JSON win over pushes to
  `sections/footer-group.json`, so edit these in the editor.
- **No header search.** The header search button and its popup were removed
  (October 2026). The `/search` results page still works. To bring search back,
  add a button and popup to `sections/header.liquid` (git history before
  October 2026 has the old version).
- **Missing policies.** Shopify has privacy and cookies set up. Termini di
  servizio, Politica di rimborso (14 day withdrawal) and Spedizioni still need
  creating in Settings > Policies; the footer links them automatically.
- **Varieties gallery arrows** only appear with more than three cards. They
  were verified to render and to start disabled on the left, but were not
  click-tested.
- **Product vendor** is still "Il mio negozio" (the old store name) on the
  products, and the product page shows it as the eyebrow. Change it in admin.
- **Product option pills** (the size-style selector) are written but never
  rendered: every product has a single variant. Treat as unverified.
- **Contact page** still exists at `/pages/contact`, but nothing links to it:
  the header's "Contatti" jumps to `#contatti` on the footer. The Shopify
  `main-menu` is no longer read by the header either.
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
  caps SVGs that are meant to run wider than their box. The hero ribbon, which
  is pulled past the content padding, overrides it with `max-width: none`.
- With `shopify theme dev`, sections must upload before a template that
  references them. A fresh `templates/index.json` referencing a brand new
  section fails until the section syncs; touch the template afterwards.
- `offsetParent` is always null on a fixed element. Measure the rect instead
  when testing whether something like the consent banner is on screen.
- A `1fr` grid track never shrinks below its content's minimum width. The
  statement section's facts grid (`auto-fit, minmax(11rem, 1fr)`) pushed the
  text, tiles and image 37px past the right edge on phones, and the footer's
  `1fr` top grid did the same by 27px at 320px. Use `minmax(0, 1fr)` for
  single-column tracks and `minmax(min(<size>, 100%), 1fr)` for auto-fit tiles.
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
