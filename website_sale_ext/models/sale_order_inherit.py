import pdb
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    substitute_checkbox = fields.Boolean(string='Substitute')
    substitute_note = fields.Text(string='Note')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.picking_ids:
            line.substitute_checkbox = self.substitute_checkbox or False
            line.note = self.substitute_note or False
            # line.payment_delivery_interval = self.payment_delivery_interval


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    is_substitute = fields.Selection(
        [('gift', 'Gift'),
         ('substitute', 'Substitute'), ], string="Is Substitute")

    # @api.depends('product_id','price_unit')
    # def get_is_subtitute(self):
    #     for rec in self:
    #         if rec.product_id and rec.price_unit == 0.0:
    #             rec.is_substitute = 'gift'
    #         else:
    #             rec.is_substitute = False

    @api.model
    def create(self, vals):
        result = super(SaleOrderLine, self).create(vals)
        if result.product_id and result.price_unit == 0.0:
            result.is_substitute = 'gift'
        else:
            pass
        return result

    # def write(self, vals):
    #     result = super(SaleOrderLine, self).write(vals)
    #     if self.product_id and self.price_unit == 0.0 and self.is_substitute != 'gift':
    #         self.is_substitute = 'gift'
    #     else:
    #         pass
    #     return result
