# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplateInheritNew(models.Model):
    _inherit = 'product.template'

    is_sold_out = fields.Boolean('Sold Out')
    availability_store = fields.Char('Availability Value', help="Technical field to store the information of inventory availability.")

    @api.onchange('is_sold_out')
    def _hide_visibility(self):
        if self.is_sold_out:
            self.availability_store = self.inventory_availability
            self.inventory_availability = False
        else:
            self.inventory_availability = self.availability_store

