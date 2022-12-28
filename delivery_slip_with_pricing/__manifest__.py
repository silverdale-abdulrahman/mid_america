# -*- coding: utf-8 -*-
{
    'name': "Delivery Slip with Pricing",

    'summary': """
        add delivery slip with pricing report and modify delivery slip """,

    'description': """
         H974,T3204,H1980
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock','sale'],

    # always loaded
    'data': [
        'report/report_action.xml',
        'report/report_deliveryslip_with_pricing.xml',
        'report/report_deliveryslip_inherit.xml',
    ],

}
