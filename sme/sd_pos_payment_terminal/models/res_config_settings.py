# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    """
        "res.config.settings" model is inherited to add a boolean field module_sd_stripe_payment_terminal in the POS 'Payment Terminals' section
            to install and uninstall the module sd_stripe_payment_terminal
    """
    module_sd_pos_stripe_payment_terminal = fields.Boolean(string="Strip Payment Terminal", help="Here transactions are processed by Strip Cards.")
    # module_pos_testing = fields.Boolean(string="Testing", help="Here transactions are processed by testing.")
