# -*- coding: utf-8 -*-
{
    'name': "Web Product Customization",

    'summary': """
        Hide Product description from mobile view
    """,

    'description': """

    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '14.0.2110',
    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        'views/product_desc.xml',
    ],
   
}
