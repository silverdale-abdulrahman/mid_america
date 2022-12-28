# -*- coding: utf-8 -*-
from odoo import models, fields, exceptions, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    category_group = fields.Char(string="Category Group", compute="_get_category_group")

    @api.depends('name')
    def _get_category_group(self):
        for rec in self:
            if rec.name and "INTRODUCTION" in rec.name.upper():
                rec.category_group = 'Introduction'
            elif rec.name and "TALL BEARDED" == rec.name.upper():
                rec.category_group = 'Tall Bearded'
            elif rec.name and "BEARDED" in rec.name.upper() and 'TALL BEARDED' != rec.name.upper():
                rec.category_group = 'Bearded'
            elif rec.name and "KEITH KEPPEL" in rec.name.upper():
                rec.category_group = 'keith keppel'
            else:
                rec.category_group = 'Other'


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    short_name = fields.Char(string='Short Name', size=35)
