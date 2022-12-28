from odoo import api, models, fields


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_hide_promo_website = fields.Boolean(string="Hide Promo Website")


