# -*- coding: utf-8 -*-
import pdb

from odoo import models, fields, exceptions, api, _


class DiglistReport(models.AbstractModel):
    _name = 'report.picklist_report.report_diglist_stock_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        stock_lines = self.env['stock.move.line'].browse(docids)
        sorted_move_lines = stock_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Introduction').sorted(key=lambda line: (line.product_id.name)) +\
                            stock_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Bearded').sorted(key=lambda line: (line.product_id.name)) +\
                            stock_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Tall Bearded').sorted(key=lambda line: (line.product_id.name)) + \
                            stock_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'keith keppel').sorted(key=lambda line: (line.product_id.name)) +\
                            stock_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Other').sorted(key=lambda line: (line.product_id.name))

        sorted_move_lines = sorted_move_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Introduction').sorted(key=lambda line: (line.category_id)) +\
                            sorted_move_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Bearded').sorted(key=lambda line: (line.product_id.name)) + \
                            sorted_move_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Tall Bearded').sorted(key=lambda line: (line.category_id)) + \
                            sorted_move_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'keith keppel').sorted(key=lambda line: (line.category_id)) + \
                            sorted_move_lines.filtered(lambda l: l.product_id.categ_id.category_group == 'Other').sorted(key=lambda line: (line.category_id))

        docs = []
        for line in sorted_move_lines:
            print(line.category_id)
            quantity = 0
            if line.state == 'done':
                quantity = int(line.qty_done)
            else:
                quantity = int(line.product_qty)

            if quantity > 1:
                for i in range(quantity):
                    docs.append(line)
            else:
                docs.append(line)

        return {

            'docs': docs,
        }
