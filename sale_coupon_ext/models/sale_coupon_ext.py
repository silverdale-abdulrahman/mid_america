# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import pdb

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang




class SaleOrder(models.Model):
    _inherit = "sale.order"


    def _update_existing_reward_lines(self):
        '''Update values for already applied rewards'''
        def update_line(order, lines, values):
            '''Update the lines and return them if they should be deleted'''
            lines_to_remove = self.env['sale.order.line']
            # Check commit 6bb42904a03 for next if/else
            # Remove reward line if price or qty equal to 0
            if values['product_uom_qty'] and values['price_unit']:
                existing_values = values
                existing_lines_price_unit = lines.price_unit
                existing_lines_order_state = lines.order_id.state

                # pdb.set_trace()
                if line.order_id.state!='sale':
                    # values.update(price_unit=lines.price_unit)
                    lines.write(values)
                previous_discount = 0.0
                for order_line in lines.order_id.order_line.filtered(lambda m: m.product_id==lines.product_id):
                    previous_discount += order_line.price_unit
                if existing_values.get('price_unit') != existing_lines_price_unit and existing_lines_price_unit > existing_values.get('price_unit') and existing_lines_order_state=='sale':
                    new_discount = values.get('price_unit')-previous_discount
                    existing_values.update(price_unit=new_discount)
                    existing_values.update({'order_id': lines.order_id.id,'is_reward_line': True,'do_not_compute':True})
                    sale_order_line = self.env['sale.order.line'].create(existing_values)
            else:
                if program.reward_type != 'free_shipping':
                    # Can't remove the lines directly as we might be in a recordset loop
                    lines_to_remove += lines
                else:
                    values.update(price_unit=0.0)
                    # pdb.set_trace()
                    lines.write(values)
            return lines_to_remove

        self.ensure_one()
        order = self
        applied_programs = order._get_applied_programs_with_rewards_on_current_order()
        for program in applied_programs:
            values = order._get_reward_line_values(program)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id and line.do_not_compute==False)
            if program.reward_type == 'discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(set([v[1] for v in value['tax_id']]))):
                            value_found = True
                            # Working on Case 3.
                            lines_to_remove -= line
                            lines_to_remove += update_line(order, line, value)
                            continue
                    # Case 2.
                    if not value_found:
                        # pdb.set_trace()
                        order.write({'order_line': [(0, False, value)]})
                # Case 3.
                lines_to_remove.unlink()
            else:
                update_line(order, lines, values[0]).unlink()


    def _remove_invalid_reward_lines(self):
        """ Find programs & coupons that are not applicable anymore.
            It will then unlink the related reward order lines.
            It will also unset the order's fields that are storing
            the applied coupons & programs.
            Note: It will also remove a reward line coming from an archive program.
        """
        self.ensure_one()
        order = self

        applied_programs = order._get_applied_programs()
        applicable_programs = self.env['coupon.program']
        if applied_programs:
            applicable_programs = order._get_applicable_programs() + order._get_valid_applied_coupon_program()
            applicable_programs = applicable_programs._keep_only_most_interesting_auto_applied_global_discount_program()
        programs_to_remove = applied_programs - applicable_programs

        reward_product_ids = applied_programs.discount_line_product_id.ids
        # delete reward line coming from an archived coupon (it will never be updated/removed when recomputing the order)
        invalid_lines = order.order_line.filtered(lambda line: line.is_reward_line and line.product_id.id not in reward_product_ids)

        if programs_to_remove:
            product_ids_to_remove = programs_to_remove.discount_line_product_id.ids

            if product_ids_to_remove:
                # Invalid generated coupon for which we are not eligible anymore ('expired' since it is specific to this SO and we may again met the requirements)
                self.generated_coupon_ids.filtered(lambda coupon: coupon.program_id.discount_line_product_id.id in product_ids_to_remove).write({'state': 'expired'})

            # Reset applied coupons for which we are not eligible anymore ('valid' so it can be use on another )
            coupons_to_remove = order.applied_coupon_ids.filtered(lambda coupon: coupon.program_id in programs_to_remove)
            coupons_to_remove.write({'state': 'new'})

            # Unbind promotion and coupon programs which requirements are not met anymore
            order.no_code_promo_program_ids -= programs_to_remove
            order.code_promo_program_id -= programs_to_remove

            if coupons_to_remove:
                order.applied_coupon_ids -= coupons_to_remove

            # Remove their reward lines
            if product_ids_to_remove:
                invalid_lines |= order.order_line.filtered(lambda line: line.product_id.id in product_ids_to_remove)

        #Task T36942
        # User try to add new products by sliverdale module [saleorder_product_smartbutton]
        # When discount level will change odoo removes discount lines and add new one.
        # If promotion program remain same then odoo will add new line instead on delete old one
        # if promotion program will change odoo will remove old promotion line and add new one.
        # But sale order is already in confirm state in confirm state odoo does not allow to remove anyline
        # For that we are changing discount line qty to zero
        # When user create new invoice then in new invoice odoo will adjust old disocunt amount in new inovice
        #  and add new discount amount in new invoice.

        if order.state in ['sale', 'done']:
            invalid_lines.write({'product_uom_qty': 0})
        else:
            invalid_lines.unlink()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    do_not_compute = fields.Boolean(default=False)
