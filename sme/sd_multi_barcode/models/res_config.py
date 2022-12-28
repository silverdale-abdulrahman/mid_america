from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    barcode_unique = fields.Boolean(
        string='Ensure Unique Barcode', )
    module_sd_multi_barcode_sale = fields.Boolean(
        string='Sales Multiple Barcode', )
    module_sd_multi_barcode_purchase = fields.Boolean(
        string='Purchase Multiple Barcode', )
    module_sd_multi_barcode_mrp = fields.Boolean(
        string='Manufacturing Multiple Barcode', )
    module_sd_multi_barcode_account = fields.Boolean(
        string='Accounting Multiple Barcode', )
    module_sd_multi_barcode_pos = fields.Boolean(
        string='Point of sale Multiple Barcode', )

    @api.depends('module_sd_multi_barcode')
    @api.onchange('module_sd_multi_barcode')
    def uninstall_submodules(self):
        for rec in self:
            if rec.module_sd_multi_barcode == False:
                if rec.module_sd_multi_barcode_sale:
                    rec.module_sd_multi_barcode_sale = False
                if rec.module_sd_multi_barcode_purchase:
                    rec.module_sd_multi_barcode_purchase = False
                if rec.module_sd_multi_barcode_mrp:
                    rec.module_sd_multi_barcode_mrp = False
                if rec.module_sd_multi_barcode_account:
                    rec.module_sd_multi_barcode_account = False
                if rec.module_sd_multi_barcode_pos:
                    rec.module_sd_multi_barcode_pos = False