# -*- coding: utf-8 -*-
{
    'name': "SME Sale",

    'summary': "This will help in sales for Enabling Features develop by Silverdale.",

    'description': """
        1: Complete Sale Order
        2: Signed Sale order
        3: Project Description from SO
        4: Sale price change
        5: MRP Status
        6: Delivery Status
        7: Credit Management
        8: Sale Default Analytic Rules
        9: Sale Agreements
        10: Silverdale Sale Commission
        11: Coupons and Promotions
        12: Sales on CRM
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2206',
    "category": 'Sales',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_base_setup', 'sale', 'sale_management'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/view_res_config_setting.xml',
        'views/view_sale_order.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}
