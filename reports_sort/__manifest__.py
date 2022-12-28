# -*- coding: utf-8 -*-
{
    'name': "Report sort",

    'summary': """
        will sort report Alphabetical """,

    'description': """
        will sort report Alphabetical
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'delivery_slip_with_pricing', 'picklist_report'],

    # always loaded
    'data': [
        'views/report_deliveryslip_sort.xml',
    ],

}
