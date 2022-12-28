# See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    elavon_txn = fields.Char('Transaction')
    provider = fields.Selection(related='acquirer_id.provider')

    @api.model
    def _elavon_form_get_tx_from_data(self, data):
        """ Given a data dict coming from elavon,
        verify it and find the related
        transaction record. """
        reference = data.get('ssl_invoice_number').replace(' ', '')

        transaction = self.search([('reference', '=', reference)])
        if not transaction:
            error_msg = (_('Elavon: received data for reference %s; no\
                 order found') % (reference))
            raise ValidationError(error_msg)
        elif len(transaction) > 1:
            error_msg = (_('Elavon: received data for reference %s;\
                 multiple orders found') % (reference))
            raise ValidationError(error_msg)
        return transaction

    def _elavon_form_validate(self, data):

        status = data.get('ssl_result_message')
        txn_dic = {
            'acquirer_reference': data.get('acquirer_reference'),
            'elavon_txn': data.get('acquirer_reference'),
        }
        res = False
        if status == 'APPROVED':
            msg = 'Payment for tx ref: %s, got response [%s], set as done.' % \
                  (self.reference, status)
            _logger.info(msg)
            self.write(txn_dic)
            self._set_transaction_done()
            res = True
        elif status == 'DECLINED':
            msg = 'Payment for tx ref: %s, got response [%s], set as ' \
                  'error.' % (self.reference, status)
            self.write(txn_dic)
            self._set_transaction_error(msg)
        else:
            msg = 'Received unrecognized status for payment ref: %s, got ' \
                  'response [%s], set as error.' % (self.reference, status)
            self.write(data)
            self._set_transaction_cancel()

        return res
