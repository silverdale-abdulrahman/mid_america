# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, time
from odoo.tools.float_utils import float_round


class SaleOrderLineExt(models.Model):
    _inherit = 'sale.order.line'

    text_note = fields.Char(string="Note")
    sales_count = fields.Float(string='Sold', compute='_compute_sale_count')

    @api.onchange('order_id.state')
    @api.depends('order_id.state')
    def _compute_sale_count(self):
        for record in self:
            r = {}
            record.sales_count = 0
            if not record.user_has_groups('sales_team.group_sale_salesman'):
                return r
                # date_from = fields.Datetime.to_string(fields.datetime.combine(fields.datetime.now() - timedelta(days=365),
                #                                                               time.min))
            date_from = record.order_id.company_id.sold_date_from

            done_states = self.env['sale.report']._get_done_states()

            for rec in self:
                domain = [
                    ('state', 'in', done_states),
                    ('product_id', '=', rec.product_id.ids),
                    ('date', '>=', date_from),
                ]
                for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'],
                                                                ['product_id']):
                    r[group['product_id'][0]] = group['product_uom_qty']
                for line in rec:
                    if not line.product_id:
                        line.sales_count = 0.0
                        continue
                    line.sales_count = float_round(r.get(line.product_id.id, 0),
                                                   precision_rounding=line.product_id.uom_id.rounding)
            return r

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            # self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    def get_total_sale_count(self):
        total = 0
        for rec in self.order_line.filtered(
                lambda line: line.display_type == False and line.is_delivery == False and line.product_id.is_shipment_product == False and line.product_id.is_discount_product == False):
            print(len(self.order_line.filtered(
                lambda
                    line: line.display_type == False and line.is_delivery == False and line.product_id.is_shipment_product == False and line.product_id.is_discount_product == False)))
            # if not rec.display_type or not rec.is_delivery or not rec.product_id.is_shipment_product or not rec.product_id.is_discount_product:
            total += rec.product_uom_qty
            print(rec.display_type)
        return total

    def get_substitute_note(self):
        if any(self.picking_ids.filtered(lambda line: line.substitute_checkbox == True)):
            return 'Yes'
        else:
            return 'No'

    def get_sale_order_lines_sorted(self):
        print(any(self.picking_ids.filtered(lambda line: line.substitute_checkbox == True)))
        lines_obj = self.env['sale.order.line']
        print(self.order_line, 'order_line')
        any_section_line = self.order_line.filtered(lambda line: line.display_type == 'line_section')
        if any_section_line:

            # if lines have gift section
            section_line = self.order_line.filtered(
                lambda line: line.display_type == 'line_section' and line.name == 'Gift Items')
            lines_price_not_zero = self.order_line.filtered(
                lambda
                    line: line.display_type != 'line_section' and line.price_unit > 0 and not line.is_gift and not line.product_id.is_discount_product)
            if lines_price_not_zero:

                sorted_lines_not_zero = lines_price_not_zero.sorted(key=lambda l: (l.product_id.name.lower()))
                for r in sorted_lines_not_zero:
                    lines_obj += r
            if section_line:
                section_line = self.order_line.filtered(
                    lambda line: line.display_type == 'line_section' and line.name == 'Gift Items')
                if section_line:
                    for r in section_line:
                        lines_obj += r
                lines_price_zero = self.order_line.filtered(
                    lambda
                        line: line.display_type != 'line_section' and line.is_gift and not line.product_id.is_discount_product)
                if lines_price_zero:
                    sorted_lines_price_zero = lines_price_zero.sorted(key=lambda l: (l.product_id.name.lower()))
                    for r in sorted_lines_price_zero:
                        lines_obj += r

                # discount
            section_line2 = self.order_line.filtered(
                lambda line: line.display_type == 'line_section' and line.name == 'Discount Items')
            if section_line2:
                for r in section_line2:
                    lines_obj += r
            lines_discount_product = self.order_line.filtered(lambda
                                                                  line: line.product_id.is_discount_product)
            if lines_discount_product:
                sorted_lines_discount_product = lines_discount_product.sorted(key=lambda l: (l.product_id.name.lower()))
                for r in sorted_lines_discount_product:
                    print(r, 'discount product')
                    lines_obj += r

            print(lines_obj, 'lines_obj')
            return lines_obj
        else:
            return self.order_line.sorted(key=lambda l: (l.product_id.name))
