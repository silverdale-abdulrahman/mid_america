import logging

import hashlib
import hmac
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import json

import stripe

_logger = logging.getLogger(__name__)

Error9 = _(
    "stripe_terminal Errors 9: Payment has been received on stripe_terminal end but some error occurred during "
    "processing the order.")


class StripeTerminalController(http.Controller):
#
    @http.route('/fail/payment', type='json', auth='public', csrf=False, website=True)
    def stripe_terminal_payment_failed(self, **kwargs):
        """when transaction failed this end point will call to handle it"""
        transaction = None

        if 'order' in kwargs and kwargs['order_type'] and kwargs['order_type'] == 'invoice':
            order = request.env['account.move'].sudo().search([('id', '=', int(kwargs['order']))])
            if order:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('invoice_ids', '=', order.id), ('amount', '=', order.amount_total)])

        elif 'order' in kwargs and kwargs['order_type'] and kwargs['order_type'] == 'order':
            order = request.env['sale.order'].sudo().search([('id', '=', int(kwargs['order']))])

        if 'acquirer_id' in kwargs:
            acquirere_id = int(kwargs['acquirer_id'])

        acquirere = request.env['payment.acquirer'].sudo().browse(int(acquirere_id))

        if 'order_type' in kwargs and kwargs['order_type'] == 'order':
            vals = {'acquirer_id': int(acquirere.id), 'return_url': '/shop/payment/validate',
                    'sale_order_ids': order.id
                    }
        if 'order_type' in kwargs and kwargs['order_type'] == 'invoice':
            vals = {'acquirer_id': int(acquirere.id), 'return_url': '/shop/payment/validate',
                    'invoice_ids': order.id
                    }

        values = {}
        resp = kwargs

        if not transaction:
            transaction = request.env['payment.transaction'].sudo().search(
                [('sale_order_ids', '=', order.id), ('amount', '=', order.amount_total)])
        if not transaction:
            transaction = order._create_payment_transaction(vals)

        transaction = transaction[0]
        message = None
        if 'message' in kwargs and kwargs['message']:
            message = kwargs['message']
        else:
            message = "Stripe Error"

        transaction.sudo()._set_transaction_error(message)
        # transaction.sudo().state_message = message
        if 'cancel' in kwargs:
            acquirere.sudo().cancel_msg = message
        return True

    @http.route('/connection_token', type="json", user='public', website=True)
    def stripe_connection(self, **kwargs):
        """Get token to connect Odoo POS with Stripe payment terminal"""
        try:

            type = None
            order = None
            refund = None
            acquirere_id = None
            acquirere = None
            data = {}
            charge_id = None

            if 'orderId' in kwargs and kwargs['orderId'] and not isinstance(kwargs['orderId'], int) and not kwargs[
                'invoice']:
                if 'orderId' in kwargs and kwargs['orderId'] and 'orders' in kwargs['orderId']:
                    order_id = [value for value in kwargs['orderId'].split('/') if value.isdigit()]
                    if len(order_id) > 0:
                        order = request.env['sale.order'].sudo().search([('id', '=', int(order_id[0]))])
                    type = 'order'

            elif 'orderId' in kwargs and isinstance(kwargs['orderId'], int):
                order = request.env['sale.order'].sudo().search([('id', '=', int(kwargs['orderId']))])
                type = 'order'

            elif 'invoice' in kwargs and kwargs['invoice']:
                invoice = kwargs['invoice'].split('/')
                if len(invoice) > 2:
                    invoice_id = [value for value in invoice[3].split('?') if value.isdigit()]
                    if len(invoice_id) > 0:
                        order = request.env['account.move'].sudo().search([('id', '=', int(invoice_id[0]))])
                        type = 'invoice'
                        refund = order.reversed_entry_id
                    # else:
                    #     order = request.env['account.move'].search([('id', '=', int(invoice_id[0]))])

            elif 'link_url' in kwargs and kwargs['link_url']:
                invoice = kwargs['link_url'].split('=')
                if invoice and len(invoice) > 1:
                    invoice_id = invoice[1].split('&')[0]
                    if invoice_id:
                        order = request.env['account.move'].sudo().search([('payment_reference', '=', invoice_id)])
                        if order:
                            refund = order.reversed_entry_id
                            type = 'invoice'

                        else:
                            order = request.env['sale.order'].sudo().search([('name', '=', invoice_id)])
                            type = 'order'

            if 'acquirer_id' in kwargs:
                acquirere_id = int(kwargs['acquirer_id'])
            if acquirere_id:
                acquirere = request.env['payment.acquirer'].sudo().browse(int(acquirere_id))
            if refund:
                refunded_tran = request.env['payment.transaction'].search([('invoice_ids','=',refund.id),('acquirer_id.provider','=','stripe_terminal')],limit=1)
                if refunded_tran and refunded_tran.stripe_charge_id:
                    charge_id = refunded_tran.stripe_charge_id
            saleorder = order
            if acquirere and acquirere.id:
                stripe.api_key = str(acquirere.pos_stripe_api_key)
                _logger.info('Authenticating Stripe Credentials....')
                token = stripe.terminal.ConnectionToken.create()
                if token:
                    data['secret']=token.secret
                    data['refund'] = True if refund else False
                    data['charge_id'] = charge_id
                    data['state'] = acquirere.state
                    data['acq_id'] = acquirere.id
                    data['location_id'] = acquirere.location_id
                    data['amount'] = saleorder.amount_total if saleorder else None
                    data['order_id'] = saleorder.id if saleorder else None
                    data['order_type'] = type if type else None
                    data['currency'] = str.upper(saleorder.currency_id.name) if saleorder else None
                    data['time_interval'] = int(acquirere.time_interval * 1000)
                    return json.dumps(data)
        except Exception as ex:
            data = {'error': ex}
            return json.dumps(data)

    @http.route('/payment_intent', type="json", user='public')
    def payment_intent(self, **kwargs):
        """ Initiate the payment with stripe terminal device"""

        payment_method = request.env['payment.acquirer'].search([('id', '=', int(kwargs['acquirer_id']))])
        order = None
        if payment_method.id:
            stripe.api_key = str(payment_method.pos_stripe_api_key)
        if 'order_type' in kwargs and kwargs['order_type'] and kwargs['order_type'] == 'invoice':
            order = request.env['account.move'].search([('id', '=', kwargs['order_id'])])

        else:
            order = request.env['sale.order'].search([('id', '=', kwargs['order_id'])])

        try:
            payment_method_type = ['card_present']
            if str.lower(order.currency_id.name) == 'cad':
                payment_method_type.append('interac_present')


            _logger.info('Calling Stripe Payment Intent SDK....')

            intent = stripe.PaymentIntent.create(
                amount=int(kwargs['amount'] * 100),
                currency=order.currency_id.name,
                payment_method_types=payment_method_type,
                capture_method='manual',
                description=order.name

            )

            if intent:
                order.stripe_terminal_tx_nid = intent.id
                data = {'client_secret': intent.client_secret}
                _logger.info('Successfully called Stripe Payment Intent: {}'.format(intent.client_secret))
                return data

        except Exception as ex:
            data = {'error': ex}
            return data

    @http.route('/capture_payment', type="json", user='public')
    def payment_capture(self, **value):
        """Capture payment  from stripe through Stripe SDK after successful payment through device"""
        _logger.info('Calling Stripe Payment capture....')
        order = None
        transaction = None
        vals = None
        card_detail = {}
        download_url = None

        payment_method = request.env['payment.acquirer'].search([('id', '=', int(value['acquirer_id']))])
        if payment_method.id:
            stripe.api_key = str(payment_method.pos_stripe_api_key)
        try:

            if 'last_4_digit' in value and value['last_4_digit']:
                card_detail['card_number'] = '******' + str(value['last_4_digit'])

            if 'card_holder' in value and value['card_holder']:
                card_detail['card_holder'] = value['card_holder']
            if 'charge_id' in value and value['charge_id']:
                card_detail['charge_id'] = value['charge_id']

            if 'card_type' in value and value['card_type']:
                card_detail['card_type'] = value['card_type']

            if 'order_type' in value and value['order_type'] and value['order_type'] == 'invoice':
                order = request.env['account.move'].search([('id', '=', int(value['order']))])
                if order:
                    if payment_method.auto_download:
                        download_url = order.get_portal_url(report_type='pdf', download=True)
                    vals = {'acquirer_id': int(payment_method.id), 'return_url': '/shop/payment/validate',
                            'invoice_ids': order.id
                            }
            else:
                order = request.env['sale.order'].search([('id', '=', int(value['order']))])

                vals = {'acquirer_id': int(payment_method.id), 'return_url': '/shop/payment/validate',
                        'sale_order_ids': order.id
                        }

            key = value['payment_id']
            key = str(key.replace("'", ""))
            if order:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('invoice_ids', '=', order.id), ('amount', '=', order.amount_total)],limit=1)
            if not transaction:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('sale_order_ids', '=', order.id), ('amount', '=', order.amount_total)],limit=1)
            if not transaction:
                transaction = order._create_payment_transaction(vals)

            transaction = transaction[0] if transaction else None

            if value.get('st_interac_present') and transaction:
                transaction.is_interac = True

            if 'payment_status' in value and value['payment_status'] == 'requires_capture':
                rslt = stripe.PaymentIntent.capture(f'{key}')

            self.payment_process(payment_method, transaction, order, value, vals,card_detail)

            if not download_url and payment_method.auto_download and order.invoice_ids:
                download_url = order.invoice_ids.get_portal_url(report_type='pdf', download=True)
            data = {'download_url':download_url}

            if value['order_type'] != 'invoice' and payment_method.auto_download and not request.env['ir.config_parameter'].sudo().get_param('portal_confirmation_pay'):
                request.env['ir.config_parameter'].sudo().set_param('sale.automatic_invoice', False)

            return data

        except Exception as ex:
            _logger.warning(ex)
            if value.get('st_interac_present') and transaction:
                transaction.is_interac = True
                self.payment_process(payment_method, transaction, order, value, vals,card_detail)
                return True
            else:
                data = {'error': ex}
                _logger.error("Sorry! Could not capture Payment {}".format(ex))
                return data

    @http.route('/refund_payment', type="json", user='public')
    def refund_payment(self, payment_method_id, orderId):
        """Capture payment  from stripe through Stripe SDK after successful payment through device"""
        _logger.info('Calling Stripe Payment refund....')
        payment_method = request.env['pos.payment.method'].search([('id', '=', int(payment_method_id))])
        # pos_payment = request.env['pos.payment'].search([('pos_order_id', '=', int(orderId))])
        pos_payment = request.env['pos.order.line'].search([('id', '=', int(orderId))]).order_id
        if pos_payment:
            for payment in pos_payment.payment_ids:
                if payment.transaction_id:
                    pos_payment = payment
                    break

        data = {}
        if payment_method.id:
            stripe.api_key = str(payment_method.pos_stripe_api_key)
        if pos_payment and pos_payment.transaction_id:
            try:

                rslt = stripe.Refund.create(payment_intent=pos_payment.transaction_id,
                                            amount=int(pos_payment.amount * 100))
                _logger.info('Successfully called capture payment with details {}'.format(rslt))

                data['error'] = False
                data['data'] = rslt
                return data

            except Exception as ex:
                data = {'error': True}
                _logger.error("Sorry! Could not Intent Payment {}".format(ex))
                return data

        else:
            data = {'error': True}
            _logger.info('Sorry the stripe transaction does not exist for this order.')
            return data

    @http.route('/cancel/payment', type="json", user='public', website=True)
    def cancel_payment(self, **kwargs):
        """Capture payment  from stripe through Stripe SDK after successful payment through device"""
        transaction = None
        order = None
        acquirere_id = None

        if 'order' in kwargs and kwargs['order_type'] and kwargs['order_type'] == 'invoice':
            order = request.env['account.move'].sudo().search([('id', '=', int(kwargs['order']))])
            if order:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('invoice_ids', '=', order.id), ('amount', '=', order.amount_total)])

        elif 'order' in kwargs and kwargs['order_type'] and kwargs['order_type'] == 'order':
            order = request.env['sale.order'].sudo().search([('id', '=', int(kwargs['order']))])

        if 'acquirer_id' in kwargs:
            acquirere_id = int(kwargs['acquirer_id'])

        acquirere = request.env['payment.acquirer'].sudo().browse(int(acquirere_id))

        if kwargs['order_type'] == 'order':
            vals = {'acquirer_id': int(acquirere.id), 'return_url': '/shop/payment/validate',
                    'sale_order_ids': order.id
                    }
        if kwargs['order_type'] == 'invoice':
            vals = {'acquirer_id': int(acquirere.id), 'return_url': '/shop/payment/validate',
                    'invoice_ids': order.id
                    }

        values = {}
        resp = kwargs

        if not transaction:
            transaction = request.env['payment.transaction'].sudo().search(
                [('sale_order_ids', '=', order.id), ('amount', '=', order.amount_total)])
        if not transaction:
            transaction = order._create_payment_transaction(vals)

        if order.stripe_terminal_tx_nid and acquirere.pos_stripe_api_key:
            stripe.api_key = acquirere.pos_stripe_api_key
            cancel_payment = stripe.PaymentIntent.cancel(order.stripe_terminal_tx_nid)
        transaction = transaction[0]
        # transaction.sudo()._set_transaction_error('Transaction has been cancelled ')
        transaction.sudo().state_message = 'Transaction has been cancelled'
        transaction.sudo().state = 'cancel'

        return True

    def payment_process(self, payment_method, transaction, order, value, vals,card_detail):
        """Handle payment transaction in odoo"""
        if not transaction:
            if order:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('invoice_ids', '=', order.id), ('amount', '=', order.amount_total)])
            if not transaction:
                transaction = request.env['payment.transaction'].sudo().search(
                    [('sale_order_ids', '=', order.id), ('amount', '=', order.amount_total)])
            if not transaction:
                transaction = order._create_payment_transaction(vals)

        transaction = transaction[0]
        values = {}
        transaction.stripe_terminal_tx_nid = order.stripe_terminal_tx_nid
        transaction.stripe_terminal_tx_currency = order.currency_id.name
        transaction.card_number =  card_detail['card_number']  if 'card_number' in card_detail else None
        transaction.card_holder = card_detail['card_holder'] if 'card_holder' in card_detail else None
        transaction.card_type = card_detail['card_type'] if 'card_type' in card_detail else None
        transaction.stripe_charge_id = card_detail['charge_id'] if 'charge_id' in card_detail else None


        values.update({
            'status': 'done',
            'reference': transaction.reference,
            'amount': transaction.amount,
            'currency': transaction.currency_id.name,
            'tx_msg': 'Payment Successfully received and submitted for settlement.',
            'acquirer_reference': payment_method.name + str(transaction.reference),
            'tx_message': "Payment Successfully received and submitted for settlement.",
            'partner_reference': value

        })

        res = request.env['payment.transaction'].sudo().form_feedback(values, 'stripe_terminal')
        # res = request.env['payment.transaction'].sudo().form_feedback(values, 'cardconnect')
        if not res:
            # transaction.sudo()._set_transaction_error(Error9)
            transaction.sudo().state_message = Error9
        # else:
        #     transaction.sudo().done_msg = 'Your payment has been successfully processed. Thank you'
        #     transaction.sudo().state_message = 'Your payment has been successfully processed. Thank you'
        _logger.info('Successfully called capture payment with details ')
