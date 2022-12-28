# -*- coding: utf-8 -*-
{
    'name': "website_stock_info",

    'summary': """
        To Show Available Stock Information""",

    'description': """
        To Show Available Stock Information
    """,

    'author': "Silverdale",
    'website': "http://www.siverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website_sale_stock'],

    # always loaded
    'data': [
        "views/assets.xml",
        "views/templates.xml",
    ],
 
}
