# -*- coding: utf-8 -*-
import pdb

from odoo import models, fields,api,_

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def delivery_report_action(self):
        return {
            'name': _('Print Report Delivery'),
            'res_model': 'delivery.report.wizard',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self._context.get('active_ids'),
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

class DeliveryReportWizard(models.TransientModel):
    _name = 'delivery.report.wizard'

    def _get_selected_delivery_orders(self):
        delivery_stock_picking = self.env['stock.picking']
        active_stock_line_ids = self.env['stock.move.line'].search([('id', 'in', self._context.get('active_ids'))])
        for stock_line in active_stock_line_ids:
            if stock_line.picking_id.id not in delivery_stock_picking.ids:
                delivery_stock_picking+=stock_line.picking_id
        return delivery_stock_picking

    delivery_order_ids = fields.Many2many('stock.picking',string='Delivery Orders',default=_get_selected_delivery_orders)

    def print_delivery_report(self):
        data = {
            'delivery_order_ids': self.delivery_order_ids.ids
        }
        return self.env.ref('delivery_report_stock_line.action_report_print_delivery_report').report_action(self, data=data)

