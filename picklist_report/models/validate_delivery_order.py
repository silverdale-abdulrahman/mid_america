# -*- coding: utf-8 -*-
import pdb

from odoo import models, fields, exceptions, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def validate_delivery_orders(self):
    #     delivery_stock_picking = self.env['stock.picking']
    #     selected_sale_orders = self.env['sale.order'].search([('id', 'in', self._context.get('active_ids'))])
    #     for rec in selected_sale_orders:
    #         if rec.picking_ids:
    #             for transfer in rec.picking_ids.filtered(lambda x: x.state == 'assigned'):
    #                 if transfer.id not in delivery_stock_picking.ids:
    #                     delivery_stock_picking += transfer
    #     if delivery_stock_picking:
    #         res = delivery_stock_picking.button_validate()
    #         if isinstance(res, dict):
    #             # this action is called in current function server action
    #             # action = res
    #             return res


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    category_id = fields.Char(string="Category", related='product_id.categ_id.name')
    sale_order = fields.Char(string="Sale Order", related='origin')
    delivery_interval = fields.Selection(related="picking_id.payment_delivery_interval", store=True)

    def validate_related_delivery_orders(self):
        delivery_stock_picking = self.env['stock.picking']
        # for rec in self:
        # if rec.origin:
        #     so = self.env['sale.order'].search([('name','=',rec.origin)],limit=1)
        #     delivery_stock_picking = self.env['stock.picking'].search(['|',('sale_id','=',so.id),
        #                                                                ('origin','=',rec.origin)],limit=1)
        selected_stock_move_lines = self.env['stock.move.line'].search([('id', 'in', self._context.get('active_ids'))])
        for stock_line in selected_stock_move_lines:
            if stock_line.picking_id.state == 'assigned' and stock_line.picking_id.id not in delivery_stock_picking.ids:
                delivery_stock_picking += stock_line.picking_id

        if delivery_stock_picking:
            res = delivery_stock_picking.button_validate()
            if isinstance(res, dict):
                # this action is called in current function server action
                # action = res
                return res


