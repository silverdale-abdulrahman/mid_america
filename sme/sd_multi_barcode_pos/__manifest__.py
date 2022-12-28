# -*- coding: utf-8 -*-
{
    'name': "SME Multiple Barcode Scanning POS",

    'summary': "Multi-Barcode feature for Point of sales",

    'description': """
            This module will let you search for product in point of sales using multiple barcodes.
        """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    "category": 'Point of Sales',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_multi_barcode', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_assets.xml',
        'views/product_template_views.xml',
    ],
}
