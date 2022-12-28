# -*- coding: utf-8 -*-
{
    'name': "Delivery Extended",

    'summary': """
        Customization related to delivery module.
    """,

    'description': """
        T30360
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Delivery',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'delivery'],

    # always loaded
    'data': [
        'wizard/choose_delivery_carrier_views.xml',
    ],
}
