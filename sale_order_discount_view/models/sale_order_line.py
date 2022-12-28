# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleorderExt(models.Model):
    _inherit = 'sale.order'
    discount_amount = fields.Monetary(string="Discount",compute='_compute_get_discount_amount')
    # shipping_charge = fields.Monetary(string="Shipping Charge",compute='_compute_get_shipping_charge')
    untaxed_amount_discount = fields.Monetary(string="Untaxed Total Amount",compute="_compute_untaxed_amount")
    @api.onchange('order_line')
    def _compute_get_discount_amount(self):
        for rec in self:
            total = 0
            for line in rec.order_line:
                if not line.is_delivery and line.price_subtotal < 0:
                    total += line.price_subtotal
                
            rec.discount_amount = total
    
    @api.depends('discount_amount','untaxed_amount_discount')
    def _compute_untaxed_amount(self):
        for rec in self:
            rec.untaxed_amount_discount = rec.amount_untaxed - rec.discount_amount - rec.amount_delivery
    # @api.onchange('order_line')
    # def _compute_get_discount_amount(self):
    #     for rec in self:
    #         rec.discount_amount = rec.amount_undiscounted - rec.amount_total
    
    # @api.onchange('order_line')
    # def _compute_get_shipping_charge(self):
    #     for rec in self:
    #         total = 0
    #         for line in rec.order_line:
    #             if line.is_delivery and line.price_subtotal > 0:
    #                 total += line.price_subtotal
                
    #         rec.shipping_charge = total