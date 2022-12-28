# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sd_website_slides_video = fields.Boolean(
        string='eLearning Document Videos')
