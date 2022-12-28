# -*- coding: utf-8 -*-
import pdb

from odoo import models, fields, api



class DelivaryReportAbstract(models.AbstractModel):
    _name = 'report.delivery_report_stock_line.delivery_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        delivery_order_ids = data.get('delivery_order_ids')
        delivery_orders = self.env['stock.picking'].search([('id', 'in', delivery_order_ids)])
        docs = delivery_orders

        return {
            # 'doc_ids': self.ids,
            # 'doc_model': self.model,
            'docs': docs,
        }
