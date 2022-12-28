# See LICENSE file for full copyright and licensing details.
from datetime import datetime

from odoo import models, fields, api

try:
    # For Python 3.0 and later
    from urllib.parse import urljoin
except ImportError:
    # For Python 2's urllib2
    from urlparse import urljoin


class AcquirerElavonPay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('elavon', 'Elavon')], ondelete={'elavon': 'set default'}
    )
    mid = fields.Char(
        'SSL Merchant ID',
        required_if_provider='elavon'
    )
    user_id = fields.Char(
        'SSL User Id',
        required_if_provider='elavon'
    )
    pin = fields.Char(
        'SSL Pin',
        required_if_provider='elavon'
    )

    def elavon_form_generate_values(self, values):
        elavon_tx_values = dict(values)
        base_url = self.env['ir.config_parameter'].sudo(). \
            get_param('web.base.url')
        elavon_tx_values.update({
            'merchant_id': self.mid,
            'user_id': self.user_id,
            'pin': self.pin,
            'server_type': 'ccsale',
            'amount': values['amount'],
            'invoice_number': values['reference'],
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get(
                'partner_country').code or '',
            'state': values.get('partner_state') and
                     (values.get('partner_state').code or
                      values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'phone': values.get('partner_phone'),
            'txn_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S %p'),
        })
        return elavon_tx_values
