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
2026 to the client's palette, and again in November 2026 to the client's
proposal: wherever a client colour passes WCAG AA in its role it is used as is,
otherwise a darker variant. The accent is the client's deep olive `#565E37`
(the lighter `#7C8650` fails as text). The values live in the theme settings,
`templates/index.json` and `assets/critical.css`, not in a switch.

| Token | Value | Use |
| --- | --- | --- |
| `--color-background` | `#EDE4D1` | Page, a warm sand |
| `--color-foreground` | `#211C14` | Text, primary buttons, the Convivia card |
| `--color-dark` | `#211C14` | Ground of "Dark" sections (the footer) |
| `--color-accent` | `#565E37` | Oliva profonda, the one accent. Hover fill for dark controls, eyebrow, cart badge |
| `--color-accent-light` | `#C9CDAE` | Light sage. Hover fill for light and ghost controls |
| `--color-muted` | `#625949` | Secondary text, AA on every light ground (4.8:1 on the large card, the lowest) |
| `--color-surface` | `#FBF6EC` | Cream. Small product cards, light panels |
| `--color-surface-strong` | `#E2D6BD` | Darker sand. Large product card, image placeholders |
| `--color-tint` | `#FBF6EC` | "Tinted" section bands (Il metodo, Convivia, the Museo collection), lighter than the page |

This is the warm beige plus dark-brown family the theme originally avoided;
it is here because the client asked for it by value. Beyond the accent, the
client's colours are applied to specific elements, never as general accents:

| Element | Value |
| --- | --- |
| Strip (`dottorini-strip`) | ground `#7C8650`, text `#EAEDDC` (large text only) |
| Gift box card (`promo_color`) | terracotta `#B05C3A` |
| Convivia eyebrow (`line_color`) | light terracotta `#E0966F` |
| Accent and text on dark bands | gold `#C9A24A`, light sand `#D9CEB6` |
| "Acquista" pill | the accent, deepening toward the ink on hover |

Left out: grigio caldo `#9A9080` (about 2.5:1 on the page) and the client's
muted `#6E6553` (about 4:1 on the large card), so muted stays `#625949`.

Section grounds are classes on each section's band, picked in the editor:
`d-bg--base` (page), `d-bg--tint` (cream) and `d-bg--dark` (the footer's
default). In `assets/critical.css` each one rescopes the tokens rather than
components restyling themselves. Inside `.d-bg--tint` muted and accent are
mixed toward the foreground and surfaces are derived from the tint. Inside
`.d-bg--dark` text turns light sand `#D9CEB6`, the accent lifts to the gold
`#C9A24A` (the deep olive is under 3:1 there),
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

Section anchors (`#collina`, `#metodo`, `#oli`, `#convivia`) sit on each band's
padded inner box; `#terra` (Cultivar) sits on the cultivar row inside the oils
panel and carries its own `scroll-margin-top`. `.section-band > [id]` gives them a negative
`scroll-margin-top` that skips most of the section's top padding, so a menu
jump puts the heading `--anchor-gap` (2rem) under the header instead of up to
4rem further down. The offset is derived from `--section-space`
(`clamp(2.25rem, 4.5vw, 4rem)`, trimmed from `3rem, 7vw, 6rem` at the owner's request: too much air between sections), so changing the spacing keeps menu jumps correct, and the band's top edge scrolls out of view, so no strip
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
| Marcellus 400 | `h1` to `h4`, the header wordmark, and display lines marked `.type-display` (manifesto statement) | `marcellus-400.woff2` |
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

- Hero: a blurred 40px copy of the photo shows at once, the photo paints over
  it, settles from a slight scale, then headline, text and button rise in
  sequence. Sets reading order.
- Hero logo ribbon: draws itself once left to right behind a soft-edged
  mask. It does not loop.
- Sections: fade and rise on scroll via CSS scroll-driven animations
  (`animation-timeline: view()`) on the shared `.reveal` class. No scroll
  event listeners anywhere. Firefox does not support this yet and simply shows
  the content, which is an acceptable fallback.
- Il metodo (journey section): on phones a scroll-snap gallery. With more than
  three cards (it has five), desktop arrow buttons scroll by one card and a
  small custom element disables them at the ends using an IntersectionObserver.
  All cards sit level, no stagger.
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
- Museo portraits: the photos in the intro frame take turns with a 1.4s
  crossfade and a slow settle out of a slight zoom, every 6s (a setting);
  dots switch by hand. The timer stops off screen, in a hidden tab and under
  reduced motion.
- Museo viewer: the photo fades in with its ground. Arrows, the arrow keys and
  a horizontal swipe step through every photo on the page, crossing from one
  section into the next and wrapping at both ends; the caption names the
  section and the position in it ("Bilance, 3 di 11"). A tap on the photo
  closes it, which the `zoom-out` cursor advertises. The photos either side
  are preloaded. Inside the viewer the focus ring switches to the cream,
  because the page's olive ring has too little contrast on the dark ground.
- Museo section row: the section crossing the upper third of the screen is
  underlined and scrolled into view inside the row.
- Everything collapses to static under `prefers-reduced-motion: reduce`.

## Section layouts

Each section uses a different layout family on purpose. Nothing repeats.

| File | Layout |
| --- | --- |
| `sections/header.liquid` | Sticky 3-column bar, 68px, blurred background. The logo sits in front of the wordmark and its tagline, centred against both. Mobile menu is a native `<details>`, which a small script closes when a link is tapped. Links come from `snippets/header-nav-links.liquid`, shared by the bar and the drawer. They are six label/target pairs in the header's own settings (`nav_1` to `nav_6`), not a Shopify menu, so homepage anchors live in the theme: "La collina" -> `/#collina` (statement), "L'olio" -> `/#metodo` (the owner wants it to open Il metodo), "Museo" -> `/pages/museo`, "Convivia" -> `/#convivia`, "Contatti" -> `#contatti` (footer). Link 3 is left blank: the owner dropped "Cultivar" from the menu because it lands inside L'olio (the `#terra` anchor still works). A blank label hides a link. There is no Home entry: the wordmark links home. Right before the account and cart icons (the bag stays last, the owner's call), a small dark "Acquista" pill (`shop_label`/`shop_href`, default `/collections/all`) opens the products page on every screen size. Below 520px the bar had no room for it (the name ran into the menu icon), so there the logo mark in front of the name is hidden, the icons close up to 0.75rem and the pill shrinks. Arriving on a page with a hash, the header settles on the target once the page has loaded, because the browser's own jump was landing at the top |
| `sections/dottorini-hero.liquid` | Full-bleed framed photo in three bands: heading top left, the logo ribbon across the middle, text at the bottom and one button ("Scopri il nostro olio", singular by the owner's request; a blank label hides it), with a scrim at top and bottom for contrast. The ribbon is in the content flow (not absolutely positioned), centred between heading and text and pulled past the padding to run edge to edge, so it never overlaps the copy; the frame has a `min-height` and grows if the content needs it. Filled path, colour is a section setting (default `#B6B351`). Height capped at `40svh` so it flattens a little on short wide screens; drawn about 1.3x taller under 900px; on phones the frame is about two thirds of the screen high (the owner found it too long). The button opens `/#metodo` (the `primary_link` setting; blank falls back to `#oli`). Photo weight: the source (`Hero.jpg`, 3000px of dense foliage) ran to 1.4 MB as WebP at full width, so the hero uses a `<picture>`: phones get a 600/900px portrait crop (`crop: 'center'`; the frame is taller than wide there), desktops top out at 1920px with `sizes` matching the real frame width, a blurred 40px copy sits under the photo as a placeholder, and there is no preload (a preload cannot follow the picture's media switch and would fetch both) |
| `sections/dottorini-strip.liquid` | Full-bleed olive strip (`#7C8650`, light text `#EAEDDC`) between the hero and the statement, one centred line in Marcellus with an optional Cormorant italic emphasis. Text and both colours are section settings; a blank text hides it |
| `sections/dottorini-featured-products.liquid` | The oils, from an owner reference: one dark rounded panel (`--color-dark`, radius 28px) inside the page column, with the logo ribbon faint behind the head (logo colour at 16%). Head: heading left and an italic Cormorant note right from 1000px. Below, one sideways scroll-snap row on every screen size: two product cards, a terracotta promo card (`#B05C3A`) and a last outlined card "Vai a tutti i prodotti" to `/collections/all`. The row runs to the panel edges (the panel clips it) and snaps to the content edge, so 1 card shows on phones (84% wide), 2 from 700px, 3 from 1000px, and the next one always peeks in from the right; on desktop that is the catalog card. Arrow buttons sit top right, above the head, from 900px. With a mouse the row can also be dragged (`snippets/scroll-gallery.liquid`: pointer events, snap off while dragging, a drag is not a click, grab cursor); touch keeps native swiping. The cards are not `.reveal` (inside a horizontal scroller their view timeline would follow the row, not the page); the whole row reveals instead. Product card: image (4:5, portrait like the 2:3 product photos, which a 6:5 box cut off top and bottom; `cover` by default, `contain` is a setting; `object-position` from the image's focal point set in admin, read from `product.featured_media.presentation`) over a cream body with a small label (product type, plus the format when there are several), title, description cut to 22 words, then price and an olive "Acquista" pill. A single-variant product adds straight to the cart through `quick-add` and the pill reads "Aggiunto" for a moment; with several formats the pill opens the product page. The promo card is the Convivia gift box, which is not a product yet: copy and colour are settings, the button links to a URL (default `/#convivia`) until a product is picked in "Gift box product". Under the head sit the three cultivars (see the Cultivar row below) and the note beside the heading reads "Un solo blend, tre olive umbre: ognuna porta la sua parte." |
| `sections/dottorini-manifesto.liquid` | La collina, from an owner reference. From 900px: the photo on the left (6 of 12 columns, almost square) and the text on the right (columns 8 to 12): section name, large statement, company text, signature. A small dark note box (`--color-dark`, title in Marcellus in the logo colour, one line of text) overlaps the photo's lower right corner and hangs past its edge into the gutter. Phones: text first, then the photo (4:5) with the note box over its foot, aligned right. Note title and text are settings; both blank hides the box. The fact tiles ("Raccolta a mano", "Estratto a freddo") were removed at the owner's request, they repeated the company text |
| `sections/dottorini-journey.liquid` | "Dottorini varietà", text-only cards, no photos (the owner's request): name in Marcellus, italic Cormorant tagline under it, short description pinned to the foot. It was built for the three cultivars, which have since moved into the oils panel; today it renders "Il metodo" (next row). Each card has a "Card color" setting, dark (`--color-dark`), olive (the accent) or light (`--color-tint`; on a tinted band it switches to the sand so it does not vanish). Up to three cards: one row from 900px, all the same height; phones scroll-snap. More than three falls back to the scrolling gallery with arrows, all cards level. File and block type keep the old `journey`/`step` names so editor data survives. A card can carry an optional link at its foot, and a fourth tone, terracotta (`#B05C3A`, the Convivia promo colour), marks a Convivia card |
| `templates/index.json` → `metodo` | "Il metodo", a second instance of the varieties section (anchor `#metodo`, tinted band) between the statement and the oils: four steps from the owner's notes (cura, raccolta, frantoio entro 8 ore, riposo in latta; the filtration step was removed at his request), dark/olive/light in turn, then a fifth terracotta card, "La tavola", linking to Convivia ("Prenota una cena"). Five cards, so it is the scrolling gallery with arrows; all level (the old every-second-card stagger shortened those cards and was dropped), and light cards sit on the sand so they show on the tinted band. Placed before the oils so the price arrives after the reasons. The owner asked for Convivia to show up across the site, not only at the foot of the page |
| Cultivar (in `sections/dottorini-featured-products.liquid`) | The three olives of the blend live inside the oils panel, under the heading, as three columns split by hairlines (stacked on phones): name in Marcellus, italic line in the logo olive, short text. They are the section's `cultivar` blocks and the row carries the `#terra` anchor (no longer in the header menu). Two earlier forms were turned down by the owner: three text cards (a repeat of "Il metodo", the same card rail one section apart) and an intensity scale (one line from "Più intenso" to "Più delicato"). The standalone section was removed; bands now alternate base (statement), tint (metodo), base (oils), tint (Convivia), base (Museo) |
| `sections/dottorini-museo-teaser.liquid` | "Museo" on the homepage, last after Convivia, `#museo`. One card in the page column like the Convivia card above it, but in the accent olive with light text (the owner wanted it boxed like the other sections) and mirrored: photos left, copy right from 900px, phones stack photos over copy. The photos sit inside the card padding on one grid: the main photo (the cart in the hills, `museo-contadino-copertina.jpg`) stretches to the card height and three square object tiles (anvil, plane, pliers) share its edges and gaps. Light pill button. Eyebrow "Piccolo Museo della Civiltà Contadina", heading with an italic `em`, short text, an italic note that the museum is closed for now, and the "Sfoglia la collezione" button to `/pages/museo`. Every photo links there too |
| `sections/dottorini-convivia.liquid` | Convivia, the family's home restaurant, as one large dark card (`--color-foreground`) inside the page column: copy left, full-height photo right, no hill line (removed at the owner's request). Phones stack photo over copy. The card is a photo container like the hero frame, not a theme switch. Adapted from an owner reference that used serif type and brass/terracotta; kept to a light terracotta `#E0966F` instead of brass (the serif came back later with the client's type system). Photo: the garden dinner (`convivia-tavola-in-giardino.jpg`; a plated dish was tried and the owner preferred the atmosphere, since the card has to explain a home restaurant at a glance). The button "Visita Convivia" links to conviviarestaurant.it (the home restaurant's own site; bookings go through Luma from there) and opens in a new tab |
| `sections/footer.liquid` | Dark band (`d-bg--dark`) by default. Top row: the brand as in the header (logo ribbon, name in Marcellus, tagline in Cormorant italic), then "Naviga" (four links, section settings `nav_1` to `nav_4`, not a Shopify menu), "In tavola" (one featured link to Convivia, light terracotta `#E0966F`) and "Contatti". Below: company details, then the copyright and policy row. The newsletter signup is hidden by a setting (`show_newsletter`, off) and, when on, sits under the brand |

## Other pages

Catalogo, product and Museo are standalone pages (not homepage sections), so
each opens directly under the sticky header with nothing above it. They share
one heading (`<h1>`, one per page) and one top spacing value, the
`.section-space--flush-top` utility in `assets/critical.css`
(`padding-top: clamp(1.5rem, 4vw, 2.5rem)`, versus the `2.25-4rem` rhythm between
homepage sections) so the gap from the header to the page's first heading
stays identical across all three. Apply it alongside `section-space` on the
page's outer wrapper; do not duplicate the value locally.

| File | What it is |
| --- | --- |
| `sections/collection.liquid` | Catalogo: 3 cards per row desktop, 2 from 700px, 1 on phones, paginated (12 per page). Heading is a section setting (default "Prodotti"), not `collection.title`, because the nav points at `/collections/all`, Shopify's auto-generated "every product" collection, which has no editable title in admin. Leave the setting blank to fall back to `collection.title` on a real collection. On `/collections/all` (Shopify generates it and cannot order it) the products can be picked in the section settings ("Products on /collections/all, in order", up to 50, no collection needed): they show in that order and the sort menu works in the browser (`?sort_by=` is kept in the URL). Left empty it lists every product automatically. A real collection (`/collections/olio`) always shows its own products in the order set in Shopify admin, with a server-side sort menu from `collection.sort_options`. A setting hides the menu |
| `sections/product.liquid` | Product page: thumbnail rail plus large image left, details right and sticky; quantity stepper beside the add button showing the price; expandable info rows as blocks. On phones the stepper becomes a full width bar above a full width button. A "Convivia" block (one per page) renders a visible terracotta note under the buy button, not a collapsed row, linking to the home restaurant |
| `sections/dottorini-museo-intro.liquid`, `dottorini-museo-collection.liquid`, `dottorini-museo-visit.liquid`, `templates/page.museo.json` | Piccolo Museo della Civiltà Contadina, Giuseppe Belardi Dottorini's collection, on its own page (`/pages/museo`). Three sections. **Intro**: H1, an italic line, Giuseppe's "Chi sono" in the first person with his signature, three figures between hairlines (20+ anni, 400 pezzi, 10 sezioni) and a link down to the collection; beside it the portraits of him among the olive trees taking turns in one 2:3 frame (slow crossfade with a slight settle, dots to switch, paused off screen and for reduced motion; a pair of overlapping photos was tried and turned down), sticky from 900px. The portraits carry the opening because the old site's cover (the orange cart) is only 1260px wide. **Collection**: one gallery per block in order, a sticky row of section names under the header (current one underlined by an IntersectionObserver, sideways scroll on phones), each gallery a masonry of columns (3/2/1) where photos keep their own ratio. Photos are not picked in the editor: a block has a file prefix and a count and the photos are looked up in Files by name (`images['museo-contadino-bilance-01.jpg']`), so 264 photos need no 264 pickers; names missing from Files are skipped. All lazy with the ratio reserved. One `<dialog>` viewer for the whole page: arrows, arrow keys and swipe step across sections, the caption names the section and "3 di 11", a tap closes it, neighbours are preloaded. Alt text is generated ("Bilance, foto 4 di 11 – Piccolo Museo…") unless the file has its own. **Visit**: a dark card like Convivia's, address, a pill notice ("Per ora il museo è chiuso al pubblico.", a setting), Google Maps and contact links, the cart photo beside it. Photo files follow `museo-contadino-<sezione>-NN.jpg`; the mapping from the old names is in `brand/museo/museo-shopify.json`. All 267 files (264 exhibits, the two portraits, the cart) are in Shopify Files; a temporary `museo-foto` branch served them for the bulk upload and can be deleted. Page SEO title "Piccolo Museo della Civiltà Contadina a Collazzone" and meta description are set on the page in admin |
| `sections/cart-drawer.liquid` | Cart as a floating rounded panel inset from the edges, not a page. Rendered on every page from `layout/theme.liquid` and refreshed through the Section Rendering API after each change. Empty, it keeps the same frame as a full cart: the logo and the message centred in the items area, and "Vedi i prodotti" full width at the bottom where "Vai al checkout" sits |
| `sections/cart.liquid` | The `/cart` page: a no-JavaScript fallback, rarely seen since the drawer handles normal use. Line items reuse the drawer's `.cart-item` classes directly (the drawer section renders on every page, so those styles are already loaded globally) rather than duplicating them, so the two can't drift apart. Quantity changes go through a plain number input plus one shared "Aggiorna carrello" submit, since this page has to work with JavaScript off; remove is a plain link to `item.url_to_remove` |

Cart behaviour: the header cart icon opens the drawer (the link still points at
`/cart` so it works without JavaScript), the product page's add button opens it
after a successful add, quantity changes and removals go through `/cart/change.js`, and a refused
change (no stock left) shows an Italian message in place instead of navigating
away.

Supporting files: `snippets/product-card.liquid` (catalog product card, links
to the product page), `snippets/quick-add.liquid` (the `<quick-add>` element that
adds to the cart with fetch, used by the product page and the oils panel, each
styling its own states),
`snippets/section-label.liquid` (the section name above each homepage section),
`snippets/scroll-gallery.liquid` (the `<scroll-gallery>` element: arrow buttons for a scroll-snap row, shared by the varieties gallery and the oils panel; mark the list `data-gallery-track` and the buttons `data-gallery-arrow`, and give the element `display: block`, it is inline by default),
`snippets/consent-inset.liquid` (reserves the height of Shopify's cookie banner
so it cannot cover the end of the footer),
`snippets/css-variables.liquid` (tokens), `assets/critical.css` (reset,
buttons, spacing, reveal keyframes), `templates/index.json` (page order).

## Product cards

Two card markups, kept in step: the homepage oils panel draws its own cards
(`sections/dottorini-featured-products.liquid`, with the "Acquista" pill) and
the catalog uses `snippets/product-card.liquid` (the whole card links to the
product page). Both are 4:5, `cover`, and take `object-position` from the
product image's focal point, so the owner can reframe a photo in admin
(product > photo > Punto focale) without touching the theme.

## Products and prices (admin data, not theme)

| Product | Handle | Price | Photo |
| --- | --- | --- | --- |
| Bottiglia 0,5 L | `bottiglia-500ml` | 15 € | `16A2840.jpg`, focal point low so the bottle sits higher in the card |
| Latta 2 L | `latta-2l` | 45 € | `16A2852.jpg` (the squat tin) |
| Latta 5 L | `latta-5l` (was `latta-3l`, redirected) | 75 € | `16A2854.jpg` (the tall tin) |
| Confezione Convivia | `confezione-convivia` | 100 € | none yet |

Names follow "Bottiglia 0,5 L" / "Latta 2 L": decimal comma, a space before
the unit, capital L. Renaming a handle in admin makes Shopify commit the new
handle into `templates/index.json` and `collection.json` by itself.

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
- Every homepage section except the hero and the strip opens with its name (`snippets/section-label.liquid`: the name in Cormorant italic, sentence case, olive on the light bands, the logo colour in the oils panel). Not a letter-spaced capitals eyebrow with a rule: the owner turned that down, and an eyebrow over every section reads as a template. The name matches the header link that leads there ("La collina", "L'olio", "Museo", "Convivia"; "Il metodo" is reached from "L'olio"), so a visitor arriving from the menu sees where they landed; it is a "Section name" setting on each section. No numbers, by the owner's request. The header backs it up: the menu link of the section crossing the middle of the screen is underlined (`aria-current="location"`, same underline as hover), set by an IntersectionObserver in the header. Links to an anchor on the page take part, and a section can claim a link to another page with `data-nav-match` (the oils panel claims the catalog URL).
- Other small uppercase eyebrows only in the oils panel (product labels, promo, catalog card) and inside the Convivia card.
- No em-dashes or en-dashes anywhere in visible copy. Use a comma, a period or
  a hyphen.
- No invented numbers or specifications.
- Every string lives in section settings so the owner can edit it.

## Still open

- **Photos.** In place: hero (`Hero.jpg`), statement (`DJI_0062.jpg`),
  product photos (2:3 lifestyle shots), Convivia (garden dinner), the Museo.
  Still missing: a photo for the Confezione Convivia product, and a
  higher-resolution copy of the Museo cart (the old cover is 1260px wide, so it
  only appears small, in the visit card).
- **Anchors.** The hero has one button, "Scopri il nostro olio", which opens the method section (`/#metodo`, the owner's request); the statement
  is reached from the header's "La collina" (`#collina`). The header's "Cultivar" points at `#terra`,
  the cultivar row inside the oils panel. Convivia is at `#convivia`. Possible
  next step: a menu link to "Il metodo" (`/#metodo`), or a short
  `/museo` URL redirect to `/pages/museo` for print.
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
- **Gallery arrows** (Il metodo, five cards) render on desktop and start
  disabled on the left; checked visually, not click-tested.
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

- `images['name.jpg']` returns an object for any name, uploaded or not, and
  `image_url` on a missing one prints a Liquid error. Test `.width > 0`
  before using it (the Museo galleries do).
- For product images the admin focal point is on
  `product.featured_media.presentation.focal_point`;
  `product.featured_image.presentation` comes back empty.

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

## Page transitions

Moving between pages uses cross-document View Transitions, CSS only
(`@view-transition { navigation: auto }` in `assets/critical.css`): the old
page fades out lifting 8px in 0.22s, the new one fades in rising from 14px in
0.5s, and the sticky header has its own transition name so it stays still
while the page changes under it. Browsers without support change page as
before; reduced motion turns it off. Anchor links on the same page keep the
smooth scroll.
