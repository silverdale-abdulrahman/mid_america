from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PrintPicklistReport(models.TransientModel):
    _name = 'picklist.report.selection'
    _description = "Select Sale Order and print Dig List Report"

    sale_order  = fields.Many2many(comodel_name="sale.order", relation="sale_order_id", column1="col1", column2="col2",  string="Sale Order",  )
    delivery_order_ids = fields.Many2many('stock.picking', string='Delivery Orders',compute='_get_selected_delivery_orders')

    def validate_delivery_orders_wizard(self):
        delivery_stock_picking = self.env['stock.picking']
        selected_sale_orders = self.env['sale.order'].search([('id', 'in', self.sale_order.ids)])
        for rec in selected_sale_orders:
            if rec.picking_ids:
                for transfer in rec.picking_ids.filtered(lambda x: x.state == 'assigned'):
                    if transfer.id not in delivery_stock_picking.ids:
                        delivery_stock_picking += transfer
        if delivery_stock_picking:
            res = delivery_stock_picking.button_validate()
            if isinstance(res, dict):
                # this action is called in current function server action
                # action = res
                return res

    def _get_selected_delivery_orders(self):
        if self.sale_order:
            self.delivery_order_ids = self.env['stock.picking'].search([('state','not in',('done','draft','cancel')),('sale_id', 'in', self.sale_order.ids)])
        else:
            raise ValidationError('Please select Sale Order to print Delivery Report')

    def print_delivery_report_price(self):
        if self.sale_order:
            data = {
                'delivery_order_ids': self.delivery_order_ids.ids
            }
            if self.delivery_order_ids:

                return self.env.ref('delivery_report_stock_line.action_report_print_delivery_report_price').report_action(self, data=data)
            else:
                raise ValidationError('No Delivery order against the selected sale order')
        else:
            raise ValidationError('Please select Sale Order to print Delivery Report')

    def print_delivery_report_without_price(self):
        if self.sale_order:
            data = {
                'delivery_order_ids': self.delivery_order_ids.ids
            }
            return self.env.ref('delivery_report_stock_line.action_report_print_delivery_report').report_action(self, data=data)
        else:
            raise ValidationError('Please select Sale Order to print Delivery Report')

    def print_picklist_report(self):
        """Print picklist Report base on sale order"""
        if self.sale_order:
            moves = self.env['stock.move.line'].search([])
            record_name = [rec.name for rec in self.sale_order]
            sale_order_moves = moves.search([('sale_order', 'in', record_name)])
            if sale_order_moves:
                report = self.env.ref('picklist_report.diglist_pdf_report_action').report_action(sale_order_moves)
                return report
            else:
                raise ValidationError('There is no any picklist item against the selected sale order',)

        else:
            raise ValidationError('Please select Sale Order to print Picklist Report')




