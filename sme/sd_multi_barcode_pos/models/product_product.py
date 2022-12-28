# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids_list = fields.Char(compute="_compute_barcodes_list")

    @api.depends('barcode_ids')
    def _compute_barcodes_list(self):
        for product in self:
            product.barcode_ids_list = False
            if product.barcode_ids:
                product.barcode_ids_list = str(product.barcode_ids.mapped('name'))
