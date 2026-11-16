import csv, re, sys

src, dst = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src, encoding='utf-8-sig')))
head, body = rows[0], rows[1:]

# Theme fields that are not words: anchors, links, file prefixes, images,
# contact data. The machine translation changed several of them (#collina ->
# #hill, photo prefixes -> English), which would break the English site.
TECH = re.compile(
    r'\.(anchor|cultivar_anchor|link|primary_link|nav_\d_href|table_href|shop_href|'
    r'prefix|image|image_main|image_second|image_third|tile_\d|contact_link|email|phone|vat|'
    r'map_query|wordmark|company_name|signature|address|value)$'
)

THEME = {
    # header / footer
    'sections/header-group.json.header.tagline': 'Olive oil from Collazzone',
    'sections/header-group.json.header.nav_1_label': 'The hill',
    'sections/header-group.json.header.nav_2_label': 'The oil',
    'sections/header-group.json.header.nav_4_label': 'Museum',
    'sections/header-group.json.header.nav_6_label': 'Contact',
    'sections/header-group.json.header.cart_label': 'Cart',
    'sections/header-group.json.header.shop_label': 'Shop',
    'sections/footer-group.json.footer.tagline': 'Olive oil from Collazzone',
    'sections/footer-group.json.footer.nav_title': 'Explore',
    'sections/footer-group.json.footer.nav_1_label': 'The hill',
    'sections/footer-group.json.footer.nav_2_label': 'The oil',
    'sections/footer-group.json.footer.nav_3_label': 'Olive varieties',
    'sections/footer-group.json.footer.nav_4_label': 'Contact',
    'sections/footer-group.json.footer.table_title': 'At the table',
    'sections/footer-group.json.footer.newsletter_heading': 'News from the mill, a few times a year.',
    'sections/footer-group.json.footer.helper_text': 'You can unsubscribe at any time.',
    'sections/footer-group.json.footer.success_message': 'Thank you, you are subscribed.',
    'sections/footer-group.json.footer.error_message': 'Please check your email address and try again.',
    'sections/footer-group.json.footer.contact_title': 'Contact',
    'sections/footer-group.json.footer.company_label': 'Company',
    'sections/footer-group.json.footer.address_label': 'Registered office',
    'sections/footer-group.json.footer.policies_label': 'Legal',
    # cart, collection, product, password
    'cart-drawer.items_label': 'items in your cart',
    'cart-drawer.item_label': 'item in your cart',
    'cart-drawer.stock_error': 'There is no more stock of this product.',
    'cart-drawer.generic_error': 'Something went wrong, please try again.',
    'cart-drawer.empty_title': 'Your cart is empty',
    'cart-drawer.empty_link_label': 'See the products',
    'cart-drawer.close_label': 'Close cart',
    'cart.json.main.empty_link_label': 'See the products',
    'collection.json.main.sort_default_label': 'Featured',
    'collection.json.main.sort_price_asc_label': 'Price, low to high',
    'collection.json.main.sort_price_desc_label': 'Price, high to low',
    'password.json.main.message': 'We are getting the online shop ready. If you have the password, come on in.',
    'password.json.main.button_label': 'Enter',
    'product.json.main.error_label': 'Something went wrong, please try again.',
    'product.json.main.stock_error_label': 'There is no more stock of this product.',
    'product.json.main.convivia.eyebrow': 'Taste it where it is made',
    'product.json.main.convivia.text': 'At Convivia, our home restaurant in Collazzone, this oil comes to the table in seasonal dishes.',
    'product.json.main.convivia.link_label': 'Book a dinner',
    'product.json.main.shipping.text': '<p>Shipping across Italy in 2 to 3 working days.</p>',
    'product.json.main.returns.text': "<p>You have 14 days to change your mind. Write to us and we'll tell you how.</p>",
    'product.json.main.storage.title': 'Storage',
    'product.json.main.storage.text': '<p>Keep the bottle away from light and heat.</p>',
    # home
    'index.json.hero.heading': 'Extra virgin olive oil, grown on our hill',
    'index.json.hero.text': '100% Umbrian, cold extracted, our own blend',
    'index.json.hero.primary_label': 'Discover our oil',
    'index.json.strip.text': 'Extra virgin olive oil from the hills of Collazzone, <em>picked by hand</em>.',
    'index.json.statement.label': 'The hill',
    'index.json.statement.statement': '<p>One family, 2,400 olive trees, one hill. Picked by hand, <em>no shortcuts</em>.</p>',
    'index.json.statement.body': "<p>Our farm is in Collazzone, in the green heart of Umbria, where the Belardi Dottorini family grows 2,400 olive trees on the hill that gives our logo its shape. The olives are still picked by hand and cold pressed a few hours after the harvest.</p><p>The result is a superior category extra virgin olive oil, true to its land and to a way of living: made with restraint, meant to be shared.</p>",
    'index.json.statement.note_title': 'The hill',
    'index.json.statement.note_text': 'A single ridge, the same one drawn in our logo.',
    'index.json.metodo.label': 'The method',
    'index.json.metodo.heading': 'From the tree to the table.',
    'index.json.metodo.metodo-cura.title': 'Care',
    'index.json.metodo.metodo-cura.tagline': 'All year round.',
    'index.json.metodo.metodo-cura.text': 'We look after the trees in every season: manure in January, careful and regular pruning, copper to heal the cuts, and foliar feeding.',
    'index.json.metodo.metodo-raccolta.title': 'The harvest',
    'index.json.metodo.metodo-raccolta.tagline': 'While the olives are still green.',
    'index.json.metodo.metodo-raccolta.text': 'We pick early, usually from 10 October, but the season has the last word. The yield is lower; in return the olives are rich in antioxidants, which keep the aroma alive for months.',
    'index.json.metodo.metodo-frantoio.title': 'The mill',
    'index.json.metodo.metodo-frantoio.tagline': 'Within 8 hours.',
    'index.json.metodo.metodo-frantoio.text': 'By the end of the day, usually by 6 pm, the olives are at the mill and pressed straight away. They are never left piled up waiting, or they would ferment.',
    'index.json.metodo.metodo-riposo.title': 'Resting',
    'index.json.metodo.metodo-riposo.tagline': 'In tins, somewhere cool.',
    'index.json.metodo.metodo-riposo.text': 'A few days of rest, then into double tin-plated containers, kept cool and dry between 12 and 18 °C. From there it goes into our bottles and tins.',
    'index.json.metodo.metodo-tavola.title': 'The table',
    'index.json.metodo.metodo-tavola.tagline': 'At Convivia, in our home.',
    'index.json.metodo.metodo-tavola.text': 'The last step is the best one: tasting it in the dishes of Convivia, our home restaurant in Collazzone.',
    'index.json.metodo.metodo-tavola.link_label': 'Book a dinner',
    'index.json.products.label': 'The oil',
    'index.json.products.heading': 'Our extra virgin.',
    'index.json.products.text': 'One blend, three Umbrian olives, each playing its part.',
    'index.json.products.buy_label': 'Buy',
    'index.json.products.error_label': 'Unavailable',
    'index.json.products.promo_heading': 'Convivia gift box',
    'index.json.products.promo_text': 'New season oil and an invitation to dinner at Convivia Home Restaurant: our way of saying welcome.',
    'index.json.products.all_eyebrow': 'Shop',
    'index.json.products.all_label': 'See all products',
    'index.json.products.variety-frantoiano.title': 'Frantoiano',
    'index.json.products.variety-moraiolo.tagline': 'Umbrian character at its purest.',
    'index.json.products.variety-moraiolo.text': 'Intensely fruity, grassy, with bold bitterness and pepper. It gives the blend its backbone.',
    'index.json.products.variety-frantoiano.text': 'Medium fruity, with floral and almond notes. It softens and rounds the blend and brings finesse.',
    'index.json.products.variety-leccino.text': 'Delicately fruity, with clean, sweet notes. It balances the whole and makes it easy to love.',
    'index.json.convivia.eyebrow': 'From the hill to the table',
    'index.json.convivia.lede': 'In our home in Collazzone, the same oil becomes something to enjoy at the table.',
    'index.json.convivia.text': 'A home restaurant where every dish speaks of the land. The truest way to know our oil is to taste it where it is made.',
    'index.json.convivia.link_label': 'Visit Convivia',
    'index.json.museo.label': 'Museum',
    'index.json.museo.eyebrow': 'Small Museum of Rural Life',
    'index.json.museo.heading': 'The tools of the people who worked <em>this land</em>.',
    'index.json.museo.text': 'For more than twenty years Giuseppe Belardi Dottorini has been collecting tools from the fields and the old trades: around 400 pieces, carefully kept and still in working order.',
    'index.json.museo.note': 'The museum is closed to the public for now, but you can browse the collection here.',
    'index.json.museo.link_label': 'Browse the collection',
    # museum page
    'page.museo.json.intro.label': 'Museum',
    'page.museo.json.intro.heading': 'Small Museum of Rural Life',
    'page.museo.json.intro.lede': 'The collection of Giuseppe Belardi Dottorini, in Collazzone.',
    'page.museo.json.intro.story_label': 'About me',
    'page.museo.json.intro.story': "<p>It all began with a love for everything rural life has to tell. More than twenty years ago I started saving my family's old tools; then came gifts from friends and neighbours, and pieces found at trade fairs and local flea markets. The search has never stopped, and I keep at it today with the same enthusiasm.</p><p>So, at my home in the countryside of Collazzone, in green Umbria, I built the museum I had always dreamed of: a wheat threshing machine and around 400 pieces of rural craft, all carefully kept and still in working order.</p><p>The collection tells the whole story of work on the land: from sowing to the wheat and maize harvest, from the grape harvest to winemaking, to raising livestock and everything that went with life in the countryside. Next to the farm tools are those of the old trades: the carpenter, the cobbler, the tailor, the weaver, the blacksmith, the knife grinder, the farrier, the pork butcher and the barber.</p><p>Every object takes you back to a time that still has a lot to say. It still moves me, and everyone who comes to visit leaves amazed.</p>",
    'page.museo.json.intro.link_label': 'See the collection',
    'page.museo.json.intro.fact-anni.label': 'years of collecting',
    'page.museo.json.intro.fact-pezzi.label': 'pieces, roughly',
    'page.museo.json.collezione.heading': 'From the field to the workshop.',
    'page.museo.json.collezione.viewer_label': 'Photos from the collection',
    'page.museo.json.collezione.empty_text': 'Photos of this section are coming soon.',
    'page.museo.json.collezione.gallery-macchine.title': 'Working the fields: machines',
    'page.museo.json.collezione.gallery-utensili-campi.title': 'Working the fields: hand tools',
    'page.museo.json.collezione.gallery-utensili-campi.nav_label': 'Field tools',
    'page.museo.json.collezione.gallery-cereali-uva-olive.title': 'Grain, grapes and olives',
    'page.museo.json.collezione.gallery-cereali-uva-olive.nav_label': 'Grain, grapes, olives',
    'page.museo.json.collezione.gallery-ferro.title': 'Ironwork',
    'page.museo.json.collezione.gallery-artigianato.title': 'Crafts',
    'page.museo.json.collezione.gallery-artigianato.nav_label': 'Crafts',
    'page.museo.json.collezione.gallery-utensili-domestici.nav_label': 'Household',
    'page.museo.json.visita.heading': 'Where to find us',
    'page.museo.json.visita.notice': 'The museum is closed to the public for now.',
    'page.museo.json.visita.place': 'Small Museum of Rural Life',
    'page.museo.json.visita.contact_label': 'Write to us for information',
}

OTHER = {
    ('PRODUCT', 'title', 'Confezione Convivia'): 'Convivia gift box',
    ('PRODUCT', 'title', 'Bottiglia 0,5 L'): '0.5 L bottle',
    ('PRODUCT', 'title', 'Latta 2 L'): '2 L tin',
    ('PRODUCT', 'title', 'Latta 5 L'): '5 L tin',
    ('PAGE', 'title', 'Museo della Civiltà Contadina'): 'Museum of Rural Life',
    ('PAGE', 'meta_title', 'Piccolo Museo della Civiltà Contadina a Collazzone'): 'Small Museum of Rural Life in Collazzone, Umbria',
    ('PAGE', 'meta_description', None): "Around 400 farm tools and tools of the old trades, collected over more than twenty years by Giuseppe Belardi Dottorini in Collazzone, Umbria. Browse the collection.",
    ('SHOP', 'meta_title', 'Agricola Dottorini'): 'Agricola Dottorini',
    ('SHOP', 'meta_description', None): 'Extra virgin olive oil we grow and press ourselves, from the green heart of Italy.',
    ('METAFIELD', 'value', 'Piccolo Museo della Civiltà Contadina a Collazzone'): 'Small Museum of Rural Life in Collazzone, Umbria',
    ('METAFIELD', 'value', None): "Around 400 farm tools and tools of the old trades, collected over more than twenty years by Giuseppe Belardi Dottorini in Collazzone, Umbria. Browse the collection.",
    ('DELIVERY_METHOD_DEFINITION', 'name', 'Pickup'): 'Pickup',
    ('LINK', 'title', 'Catalogo'): 'Shop',
    ('PAGE', 'body_html', 'museo'): "<p>Tools, skills and stories of the people who worked this land before us, gathered in a small collection in Collazzone.</p>",
}

BODY = {
    'Olio nuovo e un invito': 'New season oil and an invitation to dinner at Convivia Home Restaurant: our way of saying welcome.',
    'Fruttato medio, sentori': 'Medium fruity, with hints of grass and artichoke and a balanced bitter and peppery finish.',
    'La nostra annata in latta': 'This year’s oil in a tin, for people who use good oil every day.',
}

changed = 0
for r in body:
    typ, ident, field, loc, mkt, status, default, trans = r[:8]
    new = None
    if typ == 'ONLINE_STORE_THEME':
        key = field.split(':')[0]
        key = re.sub(r'^section\.', '', key)
        if TECH.search(key) or default.startswith('shopify://'):
            new = default
        elif key in THEME:
            new = THEME[key]
    elif typ == 'PRODUCT' and field == 'body_html':
        for k, v in BODY.items():
            if k in default:
                new = default.replace(re.search(r'<span>(.*?)</span>', default).group(1), v)
    elif typ in ('PRODUCT', 'COLLECTION', 'PAGE', 'BLOG') and field == 'handle':
        new = default
    else:
        for (t, f, d), v in OTHER.items():
            if t == typ and f == field:
                if d is None and len(default) > 60:
                    new = v
                elif d == 'museo' and 'Attrezzi, gesti' in default:
                    new = v
                elif d == default:
                    new = v
    if new is not None and new != trans:
        r[7] = new
        changed += 1

w = csv.writer(open(dst, 'w', encoding='utf-8', newline=''))
w.writerow(head)
w.writerows(body)
print('changed', changed)
