import pdb
from odoo import api, fields, models,_


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    substitute_checkbox = fields.Boolean(string='Substitute')
    substitute_note = fields.Text(string='Note')
    payment_delivery_interval = fields.Selection(string='Delivery Interval',related="sale_id.payment_delivery_interval")
    total_count_products = fields.Integer(string='Total Count', compute='_get_total_count_products')

    def _get_total_count_products(self):
        for rec in self:
            total = 0
            for line in self.move_ids_without_package.filtered(lambda c: c.product_id.is_shipment_product == False):
                # if line.price_subtotal > 0:
                total += line.product_uom_qty
            rec.total_count_products = total

    @api.onchange('substitute_checkbox','note')
    def _onchange_substitute_checkbox(self):
        if self.origin:
            so = self.env['sale.order'].search([('name','=',self.origin)])
            if so:
                so.substitute_checkbox = self.substitute_checkbox
                so.substitute_note = self.note
            # so.payment_delivery_interval = self.payment_delivery_interval

    # @api.onchange('note')
    # def _onchange_substitute_note(self):
    #     if self.origin:
    #         so = self.env['sale.order'].search([('name', '=', self.origin)])
    #     if so:
    #         so.substitute_checkbox = self.substitute_checkbox
    #         so.substitute_note = self.note