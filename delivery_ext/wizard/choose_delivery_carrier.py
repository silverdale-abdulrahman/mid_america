# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    remaining_amount = fields.Float(string='Remaining', readonly=True, compute="_compute_remaining_amount")

    @api.depends('display_price', 'order_id')
    def _compute_remaining_amount(self):
        remaining_amount = 0
        if self.display_price and self.order_id:
            remaining_amount = self.display_price - self.order_id.amount_delivery
        self.remaining_amount = remaining_amount

    def action_add_delivery_product(self):
        if self.display_price and self.order_id:
            additional_price = self.display_price - self.order_id.amount_delivery
            values = {'product_id': self.carrier_id.product_id.id,
                      'order_id': self.order_id.id,
                      'price_unit': additional_price,
                      'is_delivery': True,
                      }
            self.env['sale.order.line'].sudo().create(values)
