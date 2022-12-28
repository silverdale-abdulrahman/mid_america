# -*- coding: utf-8 -*-
{
    'name': "SME Multiple Barcode Scanning",

    'summary': "This application will allow product to have multiple barcodes.",

    'description': """
        1: Sales Multiple Barcode
        2: Purchase Multiple Barcode
        3: Manufacturing Multiple Barcode
        4: Accounting Multiple Barcode
        5: Point of sale Multiple Barcode
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    "category": 'Inventory/Inventory',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_base_setup', 'stock_barcode'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_res_config.xml',
        'views/view_product.xml',
        'views/view_product_barcodes_type.xml',
        'views/view_product_barcodes.xml',
        'views/stock_barcode_templates.xml',
    ],
    # Hooks to avoid data loss upon installation and uninstallation of the module
    'post_init_hook': 'default_barcode',

    'application': True,
    'installable': True,
    'auto_install': False,

}

