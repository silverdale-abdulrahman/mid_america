from odoo import api, fields, models, _


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    def _filter_programs_on_products(self, order):
        """
        To get valid programs according to product list.
        i.e Buy 1 imac + get 1 ipad mini free then check 1 imac is on cart or not
        or  Buy 1 coke + get 1 coke free then check 2 cokes are on cart or not
        Will apply only program that is highest min qty meet .
        """
        order_lines = order.order_line.filtered(lambda line: line.product_id and not line.is_gift) - order._get_reward_lines()
        products = order_lines.mapped('product_id')
        products_qties = dict.fromkeys(products, 0)
        for line in order_lines:
            products_qties[line.product_id] += line.product_uom_qty
        valid_program_ids = list()
        current_min_qty = 0
        for program in self:
            qty_check = current_min_qty
            if not program.rule_products_domain:
                valid_program_ids.append(program.id)
                continue
            valid_products = program._get_valid_products(products)
            if not valid_products:
                # The program can be directly discarded
                continue
            ordered_rule_products_qty = sum(products_qties[product] for product in valid_products)
            # Avoid program if 1 ordered foo on a program '1 foo, 1 free foo'
            if program.promo_applicability == 'on_current_order' and \
                    program.reward_type == 'product' and program._get_valid_products(program.reward_product_id):
                ordered_rule_products_qty -= program.reward_product_quantity
            if ordered_rule_products_qty >= program.rule_min_quantity:
                current_min_qty = program.rule_min_quantity
                if current_min_qty > qty_check:
                    valid_program_ids = []
                    valid_program_ids.append(program.id)
        return self.browse(valid_program_ids)
