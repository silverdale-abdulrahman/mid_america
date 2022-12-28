# -*- coding: utf-8 -*-
{
    'name': "Sale Order Discount View",

    'summary': """
    """,

    'description': """
	SP2111 (T2937),
    SP2112 (T3020)
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '14.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','website_sale_delivery'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/sale_order_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
