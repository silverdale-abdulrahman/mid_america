from odoo import api, SUPERUSER_ID
from odoo.http import request


# def set_barcode_in_session(cr):
#     """
#     Pre init function to store existing products barcode in a new field.
#     This will ensure that the data is not lost upon uninstallation of the module
#     """
#     env = api.Environment(cr, SUPERUSER_ID, {})
#     products = env['product.product'].search([])
#     barcodes = []
#     for product in products:
#         if product.barcode:
#             barcodes.append({product.id: product.barcode or ''})
#     request.session['product_barcode'] = barcodes


def default_barcode(cr, registry):
    """
    Post init function to restore barcode data in barcodes
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    default_type = env['product.barcode.type'].create({
        'name': 'Default'
    })
    products = env['product.product'].search([])
    for rec in products:
        if rec.barcode:
            env['product.barcode'].create({
                'product_id': rec.id,
                'name': rec.barcode,
                'barcode_type_id': default_type.id
            })