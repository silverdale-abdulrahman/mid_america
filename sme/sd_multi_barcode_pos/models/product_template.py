# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids_list = fields.Char(related="product_variant_ids.barcode_ids_list", readonly=False)

