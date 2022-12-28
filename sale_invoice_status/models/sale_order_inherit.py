import pdb
from odoo import api, fields, models,_


class SaleOrderPaymentStatus(models.Model):
    _inherit = "sale.order"

    invoice_payment_status = fields.Selection([
        ('unpaid','Unpaid'),
        ('paid','Paid')
        ],compute="_get_invoice_payment_status",string="Payment Status")
    
    
    @api.depends('invoice_status')
    def _get_invoice_payment_status(self):
        for order in self:
            # Changed algo
            # is_paid = all(inv.payment_state == 'paid' for inv in order.invoice_ids) and len(order.invoice_ids) > 0
            # if is_paid:
            invoices = order.invoice_ids.filtered(lambda x:x.payment_state == 'paid')
            total_amount =  sum(invoices.mapped('amount_total_signed'))
            if total_amount == order.amount_total and len(order.invoice_ids) > 0:
                order.invoice_payment_status = 'paid'
            else:
                order.invoice_payment_status = 'unpaid'
