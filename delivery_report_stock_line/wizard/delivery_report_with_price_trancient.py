# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Kavya Raveendran (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import pdb

from odoo import models, fields,api,_

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def delivery_report_with_price_action(self):
        return {
            'name': _('Print Report Delivery With Price'),
            'res_model': 'delivery.report.price.wizard',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self._context.get('active_ids'),
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

class DeliveryReportPriceWizard(models.TransientModel):
    _name = 'delivery.report.price.wizard'

    def _get_selected_delivery_orders(self):
        delivery_stock_picking = self.env['stock.picking']
        active_stock_line_ids = self.env['stock.move.line'].search([('id', 'in', self._context.get('active_ids'))])
        for stock_line in active_stock_line_ids:
            if stock_line.picking_id.id not in delivery_stock_picking.ids:
                delivery_stock_picking+=stock_line.picking_id
        return delivery_stock_picking

    delivery_order_ids = fields.Many2many('stock.picking',string='Delivery Orders',default=_get_selected_delivery_orders)

    def print_delivery_report_price(self):
        data = {
            'delivery_order_ids': self.delivery_order_ids.ids
        }
        return self.env.ref('delivery_report_stock_line.action_report_print_delivery_report_price').report_action(self, data=data)

