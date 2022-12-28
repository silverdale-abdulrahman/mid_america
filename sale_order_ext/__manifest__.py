# -*- coding: utf-8 -*-
{
    'name': "Sale Order Ext",

    'summary': "Functionality to  add note and sold quantity in sale order line",

    'description': """
        Functionality to  add note and sold quantity in sale order line.
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'category': 'Sale',
    'version': '2206',
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_line_view.xml',
        'views/sale_order_template.xml',
        'views/view_res_config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
