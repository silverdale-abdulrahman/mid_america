import pdb

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # display_type = fields.Boolean(string='')

    # display_type = fields.Boolean(string='')
    def get_delivery_order_lines_sorted(self):
        # print(any(self.move_lines.filtered(lambda line: line.substitute_checkbox == True)))
        lines_obj = self.env['stock.move']
        print(self.move_lines, 'move_lines')

        # if lines have gift section
        section_line = self.move_lines.filtered(
            lambda line: line.sale_line_id.price_unit == 0.0 and not line.product_id.is_discount_product)
        if section_line:
            lines_price_not_zero = self.move_lines.filtered(
                lambda line: line.sale_line_id.price_unit != 0 and not line.product_id.is_discount_product)
            if lines_price_not_zero:
                sorted_lines_not_zero = lines_price_not_zero.sorted(key=lambda l: (l.product_id.name.lower()))
                for r in sorted_lines_not_zero:
                    lines_obj += r

            print(lines_obj, 'lines_obj')
            return lines_obj
        else:
            return self.move_lines.sorted(key=lambda l: (l.product_id.name))

    def get_delivery_order_gift_sorted(self):
        # print(any(self.move_lines.filtered(lambda line: line.substitute_checkbox == True)))
        lines_obj = self.env['stock.move']
        print(self.move_lines, 'move_lines')
        # if lines have gift section
        lines_price_zero = self.move_lines.filtered(
            lambda line: line.sale_line_id.price_unit < 1 and not line.product_id.is_discount_product)
        if lines_price_zero:
            sorted_lines_price_zero = lines_price_zero.sorted(key=lambda l: (l.product_id.name.lower()))
            for r in sorted_lines_price_zero:
                lines_obj += r

            print(lines_obj, 'lines_obj')
            return lines_obj
        else:
            return False

    def get_delivery_order_discount_sorted(self):
        # print(any(self.move_lines.filtered(lambda line: line.substitute_checkbox == True)))
        lines_obj = self.env['stock.move']
        print(self.move_lines, 'move_lines')
        # if lines have Discount section
        lines_discount_product = self.move_lines.filtered(lambda line: line.sale_line_id.product_id.is_discount_product)
        if lines_discount_product:
            sorted_lines_discount_product = lines_discount_product.sorted(key=lambda l: (l.product_id.name.lower()))
            for r in sorted_lines_discount_product:
                lines_obj += r

            return lines_obj
        else:
            return False

    def get_total_amount(self):
        if self.move_lines:
            if self.move_lines[0].sale_line_id:
                sale_id = self.move_lines[0].sale_line_id.order_id
                return sale_id.amount_total


    def _get_total_count_products_rep(self):
        for rec in self:
            total = 0
            for line in self.move_ids_without_package.filtered(lambda c: c.product_id.is_shipment_product == False):
                # if line.price_subtotal > 0:
                total += line.product_uom_qty
            return total
