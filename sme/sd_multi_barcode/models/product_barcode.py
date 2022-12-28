from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = 'Product Barcode'
    _order = 'sequence'

    name = fields.Char(
        string='Barcode',
        help='Barcode from which product will be identified',
        required=True)
    barcode_type_id = fields.Many2one(
        comodel_name='product.barcode.type', ondelete='cascade',
        string='Barcode Type',
        help='Select which type of bardode this is.you can have one barcode per type',
        required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        ondelete="cascade",
        string='Product',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        required=False)


class ProductBarcodeType(models.Model):
    _name = 'product.barcode.type'
    _description = 'Product Barcode Type'

    name = fields.Char(
        string='Name',
        required=True)


class Product(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(related='product_variant_ids.barcode_ids', readonly=False)
    old_barcode = fields.Char(related='product_variant_ids.old_barcode')


class ProductVariant(models.Model):
    _inherit = 'product.product'

    barcode_ids = fields.One2many(
        comodel_name='product.barcode',
        inverse_name='product_id',
        string='Barcodes',
        required=False)
    barcode = fields.Char(
        'Barcode', copy=False,
        help="International Article Number used for product identification.", store=True,
        compute='_compute_barcode_from_barcode_ids')
    old_barcode = fields.Char(
        string='Old Barcode',
        required=False)

    _sql_constraints = [
        ('barcode_uniq', 'check(1=1)', 'No error')
    ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('default_code', operator, name),
                      '|', ('barcode', operator, name), ('barcode_ids', operator, name)]
        return self._search(expression.AND([domain, args]),
                            limit=limit, access_rights_uid=name_get_uid)

    @api.constrains('barcode', 'barcode_ids', 'active')
    def _check_unique_barcode(self):
        barcodes_duplicate = []
        for product in self:
            barcode_names = []
            if product.barcode_ids:
                barcode_names = product.mapped('barcode_ids.name')
            # if product.barcode:
            #     barcode_names.append(product.barcode)
            if not barcode_names:
                continue
            # products = self.env['product.product'].search([
            #     ('barcode', 'in', barcode_names),
            #     ('id', '!=', product.id),
            #     ('active', '=', True),
            # ])
            barcode_ids = self.env['product.barcode'].search([
                ('name', 'in', barcode_names),
                ('product_id', '!=', product.id),
                ('product_id.active', '=', True),
            ])
            if len(barcode_names) != len(set(barcode_names)):
                barcodes_multi = set([barcode for barcode in barcode_names if barcode_names.count(barcode) > 1])
                for barcode in barcodes_multi:
                    barcodes_duplicate.append(barcode)
            if barcode_ids:
                barcodes = [barcode.name for barcode in barcode_ids]
                for barcode in barcodes:
                    barcodes_duplicate.append(barcode)
            # if products:
            #     barcodes_product = [product.barcode for product in products]
            #     for barcode in barcodes_product:
            #         barcodes_duplicate.append(barcode)
        if barcodes_duplicate:
            raise UserError(
                _(
                    "The following barcode(s): {0} was found in other active products."
                    "\nNote that product barcodes should not repeat."
                ).format(", ".join(set(barcodes_duplicate)))
            )

    @api.constrains('barcode_ids')
    def _check_unique_barcode_type(self):
        for rec in self:
            exist_barcode_type_list = []
            for barcode_type in rec.barcode_ids:
                if barcode_type.barcode_type_id.id in exist_barcode_type_list:
                    raise UserError(
                        _('There is already a barcode added with the selected type %s') % barcode_type.barcode_type_id.name)
                exist_barcode_type_list.append(barcode_type.barcode_type_id.id)

    @api.depends('barcode_ids', 'barcode_ids.sequence')
    def _compute_barcode_from_barcode_ids(self):
        for rec in self:
            if rec.barcode_ids and len(rec.barcode_ids) > 0:
                rec.barcode = rec.barcode_ids[0].name
            else:
                rec.barcode = False
