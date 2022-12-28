# coding: utf-8
import logging
import pprint
import json
from odoo import fields, http
from odoo.http import request
import stripe
import json

_logger = logging.getLogger(__name__)


class StripePaymentTerminal(http.Controller):

    @http.route('/pos_connection_token', type="json", user='public')
    def stripe_connection(self, payment_method_id):
        """Get token to connect Odoo POS with Stripe payment terminal"""

        print('connected token********************************')
        try:
            payment_method = request.env['pos.payment.method'].search([('id', '=', int(payment_method_id))])
            if payment_method.id:
                stripe.api_key = str(payment_method.pos_stripe_api_key)
                _logger.info('Authenticating Stripe Credentials....')
                token = stripe.terminal.ConnectionToken.create()
                print('hello token')
                data = None
                if token:
                    data = {'secret': token.secret}
                    return json.dumps(data)
        except Exception as ex:
            data = {'error': ex}
            return json.dumps(data)

    @http.route('/pos_payment_intent', type="json", user='public')
    def payment_intent(self, amount, payment_method_id,currency):
        """ Initiate the payment with stripe terminal device"""

        payment_method = request.env['pos.payment.method'].search([('id', '=', int(payment_method_id))])
        payment_method_type = ['card_present']
        if currency and str.lower(currency)=='cad':
            payment_method_type.append('interac_present')

        if payment_method.id:
            stripe.api_key = str(payment_method.pos_stripe_api_key)

        try:
            _logger.info('Calling Stripe Payment Intent SDK....')
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency=currency,
                payment_method_types=payment_method_type,
                capture_method='manual',
            )
            if intent:
                data = {'client_secret': intent.client_secret}
                _logger.info('Successfully called Stripe Payment Intent : {}'.format(intent.client_secret))
                return data

        except Exception as ex:
            data = {'error': ex}
            return data

    @http.route('/pos_capture_payment', type="json", user='public')
    def payment_capture(self, **value):
        """Capture payment  from stripe through Stripe SDK after successful payment through device"""
        _logger.info('Calling Stripe Payment capture....')
        payment_method = request.env['pos.payment.method'].search([('id', '=', int(value['payment_method_id']))])
        if payment_method.id:
            stripe.api_key = str(payment_method.pos_stripe_api_key)
        try:
            key = value['payment_id']
            key = str(key.replace("'", ""))
            if 'payment_status' in value and value['payment_status'] == 'requires_capture':
                rslt = stripe.PaymentIntent.capture(f'{key}')
                _logger.info('Successfully called capture payment with details {}'.format(rslt))
                return rslt
            else:
                return True

        except Exception as ex:
            if value.get('st_interac_present',False):
                return True

            data = {'error': ex}
            _logger.error("Sorry! Could not Intent Payment", ex)
            return data







