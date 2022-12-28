# See LICENSE file for full copyright and licensing details.

import logging
import pdb
import pprint
from urllib.parse import urlencode

from odoo.http import request
from odoo import http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
import pycurl, io

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
_logger = logging.getLogger(__name__)


class WebsiteSaleAddress(WebsiteSale):
    def checkout_form_validate(self, mode, all_form_values, data):
        res = super(WebsiteSaleAddress, self). \
            checkout_form_validate(
            mode=mode, all_form_values=all_form_values, data=data)
        error = res[0]
        error_message = res[1]
        zip_code = len(data.get('zip'))
        if zip_code:
            if int(zip_code) > 12:
                error["zip"] = 'error'
                error_message.append(_('Please check your Zip Code'))
        return error, error_message

    @http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
    def payment(self, **post):
        req = super(WebsiteSaleAddress, self).payment(**post)
        return req


class ElavonController(http.Controller):
    _return_url = '/payment_success'
    _decline_url = '/payment_fail'

    @http.route('/payment/elavon_get_sale_order_detail', type='json',
                methods=['GET', 'POST'], auth="public", csrf=False)
    def elavon_get_sale_order_detail(self, **post):
        print(post,'post')
        try:
            if 'sale_order_id' in post:
                sale_order_id = int(post.get('sale_order_id'))
                sale_order = request.env['sale.order'].sudo().search([('id', '=', int(sale_order_id))])
                vales = {
                    'id': sale_order.id,
                    'amount': sale_order.amount_total,
                    'fname': sale_order.partner_id.name,
                    'lname': ''
                }
            else:
                sale_order_id = int(post.get('order_id'))
                sale_order = request.env['sale.order'].sudo().search([('id', '=', int(sale_order_id))])
                vales = {
                    'id': sale_order.id,
                    'amount': sale_order.amount_total,
                    'fname': sale_order.partner_id.name,
                    'lname': ''
                }
        except:
            actual_reference = ''
            if 'reference' in post:
                ref_txt = str(post.get('reference'))

                x = ref_txt.split("-")
                actual_reference = x[0]

            invoice = request.env['account.move'].sudo().search([('name', 'ilike', actual_reference)],limit=1)
            if invoice:
                inv_id = request.env['account.move'].sudo().search([('id', '=', invoice.id)])
                print(inv_id.id,'inv id')
                vales = {
                    'id': inv_id.id,
                    'amount': inv_id.amount_residual,
                    'fname': inv_id.partner_id.name,
                    'lname': ''
                }
            else:
                if 'inv_id' not in post:
                    return False
                    # error_message.append(_('Please check your Zip Code'))
                else:
                    account_invoice_id = int(post.get('inv_id'))
                    inv_id = request.env['account.move'].sudo().search([('id', '=', int(post.get('inv_id')))])
                    vales = {
                        'id': inv_id.id,
                        'amount': inv_id.amount_residual,
                        'fname': inv_id.partner_id.name,
                        'lname': ''
                    }
        return vales

    @http.route('/payment/elavon/create_charge', type='json',
                methods=['GET', 'POST'], auth="public", csrf=False)
    def elavon_success_payment(self, **post):
        post.update({'ssl_invoice_number': post.get('reference')})
        if post:
            request.env['payment.transaction'].sudo(). \
                form_feedback(post, 'elavon')
            return http.local_redirect('/payment/process')
        else:
            return http.local_redirect('/shop/checkout')

        request.env['payment.transaction'].sudo().with_context(
            lang=None).form_feedback(response, 'elavon')

        return True

    @http.route(['/payment/get_env'], type='json', auth='public', website=True)
    def get_env(self):
        elavon_acquirer_obj = request.env['payment.acquirer'].search([('provider', '=', 'elavon')])
        postmark_url = 'https://api.convergepay.com/hosted-payments/PayWithConverge.js'
        if elavon_acquirer_obj.state == 'test':
            postmark_url = 'https://api.demo.convergepay.com/hosted-payments/PayWithConverge.js'

        return postmark_url

    @http.route(['/page/get_token'], type='json', auth='public', website=True)
    def get_token(self, emp_id):
        elavon_acquirer_obj = request.env['payment.acquirer'].search([('provider', '=', 'elavon')])
        postmark_url = 'https://api.convergepay.com/hosted-payments/transaction_token'
        if elavon_acquirer_obj.state == 'test':
            postmark_url = 'https://api.demo.convergepay.com/hosted-payments/transaction_token'

        buffer = io.BytesIO()
        post_data = {
            'ssl_merchant_id': elavon_acquirer_obj.mid,
            'ssl_user_id': elavon_acquirer_obj.user_id,
            'ssl_pin': elavon_acquirer_obj.pin,
            'ssl_transaction_type': 'CCSALE',
            'ssl_first_name': emp_id.get("ssl_first_name"),
            'ssl_last_name': emp_id.get("ssl_last_name"),
            'ssl_get_token': 'Y',
            'ssl_add_token': 'Y',
            'ssl_amount': emp_id.get("ssl_amount"),
        }
        postfields = urlencode(post_data)

        c = pycurl.Curl()
        c.setopt(c.URL, postmark_url)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, postfields)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, False)
        c.setopt(pycurl.VERBOSE, True)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        body = buffer.getvalue()
        c.close()
        return body

    @http.route('/payment_success', type='http', auth="public",
                methods=['GET', 'POST'], csrf=False)
    def payment_elavon_success(self, **post):
        _logger.info(
            'Elavon : entering form_feedback success with post data %s',
            pprint.pformat(post)
        )
        if post:
            request.env['payment.transaction'].sudo(). \
                form_feedback(post, 'elavon')
            return http.local_redirect('/payment/process')
        else:
            return http.local_redirect('/shop/checkout')

    @http.route('/payment_fail', type='http',
                auth="public", methods=['GET', 'POST'], website=True)
    def payment_elavon_fail(self, **post):
        _logger.info(
            'Elavon : entering form_feedback failure with post data %s',
            pprint.pformat(post)
        )
        if post.get('error') == 'server_error':
            msg = "Server Error Please Check Your Configuration"
        elif post.get('error') == 'cancel':
            msg = "Transaction Has Been Cancelled"
        elif post.get('error') == 'declined':
            msg = "Transaction Has Been Declined"
        kwargs = {
            'error': msg,
            'error_code': post.get('error')
        }
        return request.render("payment_elavon_scs.Failed", kwargs)
