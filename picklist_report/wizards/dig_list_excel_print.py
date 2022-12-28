# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io
from odoo.exceptions import ValidationError, UserError
import pdb
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class DigListMain(models.TransientModel):
    _name = 'dig.list.main'
    _description = 'dig_list_main'

    def _get_stock_move_for_gig(self):
        return self.env['stock.move.line'].search([('id', 'in',self._context.get('active_ids'))])

    stock_move_ids = fields.Many2many('stock.move.line',string='Products',default=_get_stock_move_for_gig)
    dig_records_ids = fields.One2many('dig.list.records','dig_list_id',string='dig list records',compute='get_dig_list')

    def get_dig_list(self):
        obj = self.env['dig.list.records']
        obj.unlink()
        list = []
        for line in self.env['stock.move.line'].search([('id', 'in', self._context.get('active_ids'))]):
            if line.state == 'done':
                quantity = int(line.qty_done)
            else:
                quantity = int(line.product_qty)
            for l in range(quantity):
                values = {
                    'picking_id': line.picking_id.id,
                    'move_id': line.move_id.id,
                    'product_id': line.product_id.id,
                    'date': line.date,
                    'product_uom_qty': 1.0,
                    'qty_done': quantity,
                    'result_package_id': line.result_package_id.id,
                    'dig_list_id': self.id,
                }
                sub_obj = obj.create(values)
                print(sub_obj,'sub_obj')
                obj += sub_obj
        self.dig_records_ids = obj.ids or False

    def export_dig_list_records(self):
        y=0
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
        style = xlwt.easyxf('font:bold True;borders:left thin, right thin, top thin, bottom thin;')
        style1 = xlwt.easyxf(num_format_str='MM/DD/YYYY HH:MM:SS')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')
        ws.col(1).width = int(20 * 260)
        ws.col(0).width = int(20 * 260)
        ws.col(2).width = int(20 * 260)
        # ws.col(4).width = int(20 * 260)
        # ws.col(6).width = int(20 * 260)
        # ws.col(7).width = int(20 * 260)

        ws.write(0, 0, 'Delivery Order', style)
        ws.write(0, 1, 'Product Name', style)
        ws.write(0, 2, 'Type of item to share', style)
        # ws.write(0, 3, 'Category', style)
        # ws.write(0, 0, 'Product Category', style)

        # ws.write(0, 2, 'Delivery Order',style)
        # ws.write(0, 3, 'Sale Order',style)
        # ws.write(0, 4, 'Quantity Reserved',style)
        # ws.write(0, 5, 'Quantity Done',style)
        # ws.write(0, 6, 'Destination Package',style)
        # ws.write(0, 7, 'Date', style)
        # ws.write(0, 8, 'Customer', style)
        # ws.write(0, 9, 'Mobile', style)
        # ws.write(0, 10, 'Phone', style)

        i = 1

        stock_move_lines = self.dig_records_ids.filtered(lambda l: l.product_id.categ_id.category_group == 'Introduction').sorted(key=lambda line: (line.product_name))+\
                           self.dig_records_ids.filtered(lambda l: l.product_id.categ_id.category_group == 'Bearded').sorted(key=lambda line: (line.product_name))+\
                           self.dig_records_ids.filtered(lambda l: l.product_id.categ_id.category_group == 'keith keppel').sorted( key=lambda line: (line.product_name))+\
                           self.dig_records_ids.filtered(lambda l: l.product_id.categ_id.category_group == 'Other').sorted(key=lambda line: (line.product_name))

        for line in stock_move_lines:
            ws.write(i, 0, line.reference or '')
            ws.write(i, 1, line.product_id.name or '')
            ws.write(i, 2, line.product_type or '')
            # ws.write(i, 3, line.product_id.categ_id.category_group or '')
            # ws.write(i, 3, line.origin)
            # ws.write(i, 4, line.product_uom_qty)
            # ws.write(i, 5, line.qty_done)
            # ws.write(i, 6, line.result_package_id.name or '')
            # ws.write(i, 7, line.date, style1)
            # ws.write(i, 8, line.partner_id.name or '')
            # ws.write(i, 9, line.mobile or '')
            # ws.write(i, 10, line.phone or '')

            i += 1


        file_data = io.BytesIO()

        wb.save(file_data)

        print(wb,'wb')

        wiz_id = self.env['dig.report.save'].create({
            'data': base64.encodestring(file_data.getvalue()),
            'name': 'dig list report.xls'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Dig List Sheet',
            'res_model': 'dig.report.save',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'target': 'new'
        }


class dig_report_save(models.TransientModel):
    _name = "dig.report.save"
    _description = 'dig report save'

    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)


class DigListRecord(models.TransientModel):
    _name = 'dig.list.records'
    _description = 'dig.list.records'

    picking_id = fields.Many2one('stock.picking', 'Transfer', auto_join=True)
    move_id = fields.Many2one('stock.move', 'Stock Move')
    product_id = fields.Many2one('product.product', 'Product')
    product_name = fields.Char(related='product_id.name')
    date = fields.Datetime('Date', required=True)
    reference = fields.Char(related='move_id.reference', store=True, readonly=False)
    origin = fields.Char(related='move_id.origin', string='Source')
    product_uom_qty = fields.Float('Reserved', default=0.0, digits='Product Unit of Measure', required=True)
    qty_done = fields.Float('Done', default=0.0, digits='Product Unit of Measure')
    result_package_id = fields.Many2one('stock.quant.package', 'Destination Package', required=False)
    product_category_id = fields.Many2one(related='product_id.categ_id',string='Product Category')
    category_name = fields.Char(related='product_category_id.name', string='Product Category')
    dig_list_id = fields.Many2one('dig.list.main',string='Dig list id')
    partner_id = fields.Many2one('res.partner', string='Customer',compute='_get_partner_id')
    phone = fields.Char(related='partner_id.phone', string='Phone')
    mobile = fields.Char(related='partner_id.mobile', string='Mobile')
    product_type = fields.Char(string='Product Type',compute='get_product_type_for_dig')


    def get_product_type_for_dig(self):
        for rec in self:
            if rec.move_id and rec.move_id.sale_line_id:
                if rec.move_id.sale_line_id.price_unit == 0.0:
                    rec.product_type = 'Gift'
                elif rec.move_id.sale_line_id.is_substitute:
                    if rec.move_id.sale_line_id.is_substitute == 'substitute':
                        rec.product_type = 'Substitute' or False
                    elif rec.move_id.sale_line_id.is_substitute == 'gift':
                        rec.product_type = 'Gift' or False
                else:
                    rec.product_type = '' or False
            else:
                rec.product_type = '' or False

    def _get_partner_id(self):
        for rec in self:
            if rec.origin:
                so = self.env['sale.order'].search([('name', '=', rec.origin)],limit=1)
                # po = self.env['purchase.order'].search([('name', '=', rec.origin)],limit=1)
                if so:
                    rec.partner_id = so.partner_id.id
                # elif po:
                #     rec.partner_id = po.partner_id.id
                else:
                    rec.partner_id = False