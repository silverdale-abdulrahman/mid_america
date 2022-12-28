# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"
    """
        model 'product.template' is inherited and added two following sequence fields.
    """
    internal_reference = fields.Char(string='Internal Reference', required=True, copy=False,
                                   default=lambda self: self.env['ir.sequence'].next_by_code('product_template.reference'))

    product_barcode = fields.Char(string='Product Barcode', required=True, copy=False,
                                   default=lambda self: self.env['ir.sequence'].next_by_code('product_template.barcode'))

    @api.model
    def default_get(self, fields):
        """
            this odoo standard method will make sure if rule is set for auto creation of
            reference or barcode or both fields during creation of a product.
        """
        res = super(ProductTemplate, self).default_get(fields)
        for rec in self:
            if(rec.env.user.company_id.create_product_internal_reference):
                rec.default_code = rec.internal_reference
            if (rec.env.user.company_id.use_internal_reference_as_barcode):
                rec.default_code = rec.internal_reference
                rec.barcode = rec.internal_reference
            if(rec.env.user.company_id.create_product_barcode):
                rec.barcode = rec.product_barcode
        return res


    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        res = super(ProductTemplate, self).copy(default=default)
        for rec in res:
            if(rec.env.user.company_id.create_product_internal_reference):
                rec.default_code = rec.internal_reference
            if (rec.env.user.company_id.use_internal_reference_as_barcode):
                rec.default_code = rec.internal_reference
                rec.barcode = rec.internal_reference
            if(rec.env.user.company_id.create_product_barcode):
                rec.barcode = rec.product_barcode
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"
    """
        model 'product.product' is inherited and added two following sequence fields.
    """
    internal_reference = fields.Char(string='Internal Reference', required=True, copy=False,
                                   default=lambda self: self.env['ir.sequence'].next_by_code('product_product.reference'))

    product_barcode = fields.Char(string='Product Barcode', required=True, copy=False,
                                   default=lambda self: self.env['ir.sequence'].next_by_code('product_product.barcode'))


    @api.model
    def default_get(self, fields):
        """
            this odoo standard method will make sure if rule is set for auto creation of
            reference or barcode or both fields during creation of a product.
        """
        res = super(ProductProduct, self).default_get(fields)
        for rec in self:
            if(rec.env.user.company_id.create_product_internal_reference):
                rec.default_code = rec.internal_reference
            if (rec.env.user.company_id.use_internal_reference_as_barcode):
                rec.default_code = rec.internal_reference
                rec.barcode = rec.internal_reference
            if(rec.env.user.company_id.create_product_barcode):
                rec.barcode = rec.product_barcode
        return res
