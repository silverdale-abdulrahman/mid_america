from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    def _default_domestic_min_order(self):
        try:
            return self.website_id.domestic_min_order
        except ValueError:
            return 30
    
    def _default_outside_domestic_min_order(self):
        try:
            return self.website_id.outside_domestic_min_order
        except ValueError:
            return 200
    domestic_min_order = fields.Float("Domestic minimum order", help="The minimum order of products without the shipping on domestic orders.",
                                        related='website_id.domestic_min_order', readonly=False)
    outside_domestic_min_order = fields.Float("Outside Domestic minimum order", help="The minimum on all orders outside the domestic without the shipping.",
     related='website_id.outside_domestic_min_order', readonly=False)
