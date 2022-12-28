import datetime

from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sold_date_from = fields.Datetime(related='company_id.sold_date_from', readonly=False, )


class Company(models.Model):
    _inherit = 'res.company'

    sold_date_from = fields.Datetime(
        string='Sold Date From', )
