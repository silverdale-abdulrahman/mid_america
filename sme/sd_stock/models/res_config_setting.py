# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sd_stock_status = fields.Boolean(
        string='Delivery Status',
        required=False)
