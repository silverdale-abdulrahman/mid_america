# -*- coding: utf-8 -*-
{
    'name': "Stock Qty Validation",

    'summary': """
        Name: Inventory mass update buttons,
        Sprint: 2107,
    """,

    'description': """

    """,

    'author': "Silverdale",
    'website': "http://www.silverdale.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
