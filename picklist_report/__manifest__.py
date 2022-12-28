# -*- coding: utf-8 -*-
{
    'name': "Pick List Report",

    'summary': " Silverdale module for Pick List Report.",

    'description': """
        1.Functionality to Sort pick list by category and product. 
        2.Functionality to Create Wizard for Sale Order selection to print picklist related to that selected sale order.
        3.Functionality to Add Delivery interval in stock move line with fiter and groupby option.
        4.Functionality to Change breaded category group. Now all breaded category will come in Breaded group.
        5.Functionality to change the sorting sequence of breaded and tall breaded   
        6.Functionality to "Print Delivery Report" & "Print Delivery Report with Price" on the wizard designed for batch sales order selection 
        7.Functionality to change sorting for Breaded (only sorted by product not category)
    """,

    'author': "Silverdale",
    'website': "https://www.silverdaletech.com",
    "license": "Other proprietary",
    'version': '2206',
    # for the full list
    'category': 'Stock',
    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','product','website_sale_ext'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/picklist_report.xml',
        'views/product_template_view.xml',
        'views/picklist_report_pdf.xml',
        'views/validate_delivery_action.xml',
        'wizards/print_picklist_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,

}
