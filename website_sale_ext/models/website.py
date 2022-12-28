from odoo import models, fields, api

from odoo.osv import expression

class Website(models.Model):
    _inherit = 'website'

    domestic_min_order = fields.Float("Domestic minimum order", default=35)
    outside_domestic_min_order = fields.Float("Outside Domestic minimum order", default=200)