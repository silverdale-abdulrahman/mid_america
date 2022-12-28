# -*- coding: utf-8 -*-
{
    'name': "SME Inventory",

    'summary': "This will help in inventory for enabling features develop by Silverdale.",

    'description': """
        1: Product Category in Stock Report
        
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    'license': 'OPL-1',
    'version': '2208',
    "category": 'Inventory',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sd_base_setup', 'stock'],

    # always loaded
    'data': [
        'views/view_res_config_setting.xml',
        'views/stock_quant_view.xml',
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}
