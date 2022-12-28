from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
# from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSale
import json



class WebsiteSaleWishlistInherit(WebsiteSaleWishlist):

    @http.route(['/shop/wishlist'], type='http', auth="public", website=True, sitemap=False)
    def get_wishlist(self, count=False, **kw):
        values = request.env['product.wishlist'].with_context(display_default_code=False).current()
        # values = values_without_sort.sort(key=lambda m: m.product_id.name)
        # values = values.sorted(key=lambda m: m.product_id.name)
        # values = values.sorted(key=lambda x: [(c.product_id.name.lower()) for c in x])
        values = values.sorted(key=lambda x: (x.product_id.name[0].lower(), x.product_id.name[0].islower(), len(x)))
        if count:
            return request.make_response(json.dumps(values.mapped('product_id').ids))

        if not len(values):
            return request.redirect("/shop")

        return request.render("website_sale_wishlist.product_wishlist", dict(wishes=values))